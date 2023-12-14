# libsql数据库交互类
import os
from utils import time_util, base64_util
import libsql_client
from libsql_client import ResultSet, ClientSync, Statement
from libsql import sql_scripts
from core.alidrive import Alidrive
from aligo.error import AligoRefreshFailed
import logging
from trakt.movies import Movie
from trakt.tv import TVShow, TVSeason, TVEpisode
from core import tmdb

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


# 数据库地址
TURSO_DB_URL = os.environ['TURSO_DB_URL']
# 数据库认证token
TURSO_DB_AUTH_TOKEN = os.environ['TURSO_DB_AUTH_TOKEN']


def get_client():
    """获取数据库客户端

    Returns:
        [type]: [description]
    """
    return libsql_client.create_client_sync(
        url=TURSO_DB_URL, auth_token=TURSO_DB_AUTH_TOKEN)


def init_db(client: ClientSync):
    """初始化数据库

    Args:
        client (ClientSync): 客户端对象
    """
    # 如果索引表不存在，则创建索引表
    if len(client.execute(sql_scripts.TABLE_LOCAL_SEARCH_EXISTS).rows) == 0:
        logger.info('索引表不存在,创建索引表...')
        client.execute(sql_scripts.CREATE_TABLE_LOCAL_SEARCH)
        logger.info('创建索引表成功!')
    # 如果刮削记录表不存在，则创建刮削记录表
    if len(client.execute(sql_scripts.TABLE_SCRAPING_RECORD_EXISTS).rows) == 0:
        logger.info('刮削记录表不存在,创建刮削记录表...')
        client.execute(sql_scripts.CREATE_TABLE_SCRAPING_RECORD)
        logger.info('创建刮削记录表成功!')
    # 如果电影表不存在，则创建电影表
    if len(client.execute(sql_scripts.TABLE_MOVIE_EXISTS).rows) == 0:
        logger.info('电影表不存在,创建电影表...')
        client.execute(sql_scripts.CREATE_TABLE_MOVIE)
        # 创建索引
        client.execute(sql_scripts.CREATE_INDEX_MOVIE)
        logger.info('创建电影表成功!')
    # 如果剧集表不存在，则创建剧集表
    # if len(client.execute(sql_scripts.TABLE_SHOW_EXISTS).rows) == 0:
    #     logger.info('剧集表不存在,创建剧集表...')
    #     client.execute(sql_scripts.CREATE_TABLE_SHOW)
    #     # 创建索引
    #     client.execute(sql_scripts.CREATE_INDEX_SHOW)
    #     logger.info('创建剧集表成功!')
    # 如果季(剧集)表不存在，则创建季(剧集)表
    # if len(client.execute(sql_scripts.TABLE_SEASON_EXISTS).rows) == 0:
    #     logger.info('季(剧集)表不存在,创建季(剧集)表...')
    #     client.execute(sql_scripts.CREATE_TABLE_SEASON)
    #     logger.info('创建季(剧集)表成功!')


client = get_client()
init_db(client)


def update_movies(watched_movies: list[Movie]):
    """更新电影观看进度

    Args:
        watched_movies (list): _description_
    """
    logger.info('更新电影观看进度...')
    #  新增的电影
    statements: list[Statement] = []
    # 死链 需要更新
    dead_links_statements: list[Statement] = []
    skip_dead_link_check = False
    try:
        alidrive = Alidrive()
    except AligoRefreshFailed:
        logger.info('alidrive服务的token过期了,跳过死链检测...')
        skip_dead_link_check = True
    # 查询数据库所有的电影
    movies_res: ResultSet = client.execute(sql_scripts.SELECT_ALL_MOVIE)
    #  获取数据库中所有的电影ID
    movie_ids = [movie_row[0] for movie_row in movies_res.rows]
    for movie in watched_movies:
        if str(movie.tmdb) in movie_ids:
            movie_ids.remove(str(movie.tmdb))
        # 转为中文
        country_name = tmdb.convert2zh(movie)
        movie_res = client.execute(
            sql_scripts.SELECT_MOVIE_BY_ID, [movie.tmdb])
        # 如果电影已存在
        if len(movies_res.rows) > 0:
            # 死链检测 如果链接已死 则更新链接为''(只支持阿里云盘) 如果死链检测抛出异常 说明alidrive服务的token过期了  跳过
            try:
                # 根据id查询share_link
                share_link = movie_res.rows[0][0]
                if share_link != '' and not skip_dead_link_check and not alidrive.check_link(share_link):
                    # 检测未通过
                    dead_links_statements.append(
                        Statement(sql_scripts.UPDATE_MOVIE_LINK_BY_ID, ['', movie.tmdb]))
            except Exception as e:
                logger.info(f'aligo服务异常:{e}')
            continue
        # 创建InStatement集合  需切换为中文
        statements.append(Statement(sql_scripts.INSERT_TABLE_MOVIE_STATEMENT, [movie.tmdb,
                          movie.title, movie.overview, movie.year, movie.poster, country_name, movie.rating, '', movie.plays, time_util.convert(movie.last_watched_at)]))
    client.batch(statements)
    # 删除数据库中trakt已标记未观看的电影 保持与trakt同步
    delete_statements = []
    for movie_id in movie_ids:
        delete_statements.append(
            Statement(sql_scripts.DELETE_MOVIE_BY_ID, [movie_id]))
    client.batch(delete_statements)
    # 更新死链
    client.batch(dead_links_statements)
    index_data = base64_util.index(watched_movies=watched_movies)
    # 如果索引表中不存在电影索引，则新增电影索引
    if len(client.execute(sql_scripts.SELECT_LOCAL_SEARCH_BY_TYPE, ['movie']).rows) == 0:
        logger.info('索引表中不存在电影索引,新增电影索引...')
        client.execute(sql_scripts.INSERT_TABLE_LOCAL_SEARCH_STATEMENT, [
                       'movie', index_data])
        logger.info('新增电影索引成功!')
    else:
        # 如果索引表中存在电影索引，则更新电影索引
        logger.info('索引表中存在电影索引,更新电影索引...')
        client.execute(sql_scripts.UPDATE_TABLE_LOCAL_SEARCH_STATEMENT, [
                       index_data, 'movie'])
        logger.info('更新电影索引成功!')
    logger.info('更新电影观看进度成功!')


def update_shows(watched_shows: list[TVShow]):
    """更新剧集观看进度

    Args:
        watched_shows (list): _description_
    """
    print('更新剧集观看进度...')
