# libsql数据库交互类
import os
from venv import logger
import libsql_client
from libsql_client import ResultSet, ClientSync
from libsql import sql_scripts
import logging

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
    # 如果电影表不存在，则创建电影表
    if len(client.execute(sql_scripts.TABLE_MOVIE_EXISTS).rows) == 0:
        logger.info('电影表不存在,创建电影表...')
        client.execute(sql_scripts.CREATE_TABLE_MOVIE)
        # 创建索引
        client.execute(sql_scripts.CREATE_INDEX_MOVIE)
        logger.info('创建电影表成功!')
    # 如果剧集表不存在，则创建剧集表
    if len(client.execute(sql_scripts.TABLE_SHOW_EXISTS).rows) == 0:
        logger.info('剧集表不存在,创建剧集表...')
        client.execute(sql_scripts.CREATE_TABLE_SHOW)
        # 创建索引
        client.execute(sql_scripts.CREATE_INDEX_SHOW)
        logger.info('创建剧集表成功!')
    # 如果季(剧集)表不存在，则创建季(剧集)表
    if len(client.execute(sql_scripts.TABLE_SEASON_EXISTS).rows) == 0:
        logger.info('季(剧集)表不存在,创建季(剧集)表...')
        client.execute(sql_scripts.CREATE_TABLE_SEASON)
        logger.info('创建季(剧集)表成功!')


client = get_client()
init_db(client)


def update_movies(watched_movies: list):
    """更新电影观看进度

    Args:
        watched_movies (list): _description_
    """
    print('更新电影观看进度...')


def update_shows(watched_shows: list):
    """更新剧集观看进度

    Args:
        watched_shows (list): _description_
    """
    print('更新剧集观看进度...')
