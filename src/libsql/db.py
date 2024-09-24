# libsql数据库交互类
import logging
import os

import libsql_client
from libsql_client import ResultSet, ClientSync, Statement
from trakt.movies import Movie
from trakt.tv import TVShow

from core import tmdb
from libsql import sql_scripts
from utils import time_util, base64_util

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
	# 查询数据库所有的电影
	movies_res: ResultSet = client.execute(sql_scripts.SELECT_ALL_MOVIE)
	#  获取数据库中所有的电影ID
	movie_ids = [movie_row[0] for movie_row in movies_res.rows]
	for movie in watched_movies:
		if str(movie.tmdb) in movie_ids:
			movie_ids.remove(str(movie.tmdb))
			continue
		# 转为中文
		country_name = tmdb.convert2zh_movie(movie)
		# 创建InStatement集合  需切换为中文
		statements.append(Statement(sql_scripts.INSERT_TABLE_MOVIE_STATEMENT, [movie.tmdb,
		                                                                       movie.title, movie.overview, movie.year,
		                                                                       movie.poster, country_name, movie.rating,
		                                                                       '', movie.plays, time_util.convert(
				movie.last_watched_at)]))
	client.batch(statements)
	# 删除数据库中trakt已标记未观看的电影 保持与trakt同步
	delete_statements = []
	for movie_id in movie_ids:
		delete_statements.append(
			Statement(sql_scripts.DELETE_MOVIE_BY_ID, [movie_id]))
	client.batch(delete_statements)
	index_data = base64_util.index_movies(watched_movies=watched_movies)
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
	# 只要有新增或者删除 则返回True 表示需要刷新缓存
	return len(statements) != 0 or len(delete_statements) != 0


def update_shows(watched_shows: list[TVShow]):
	"""更新剧集观看进度   只要剧集看完过一集 那么就存到数据库中  同时新增两个字段  剧进度和集进度   1.season_progress   例如: 01/05    2.episode_progress    例如: 01/13

	Args:
		watched_shows (list): _description_
	"""
	print('更新剧集观看进度...')
	#  新增的剧集
	statements: list[Statement] = []
	
	# 需要更新进度或者完结状态的
	status_update_statements = []
	
	# 查询数据库所有的剧集
	shows_res: ResultSet = client.execute(sql_scripts.SELECT_ALL_SHOW)
	# 如果剧集未完结 还要持续更新剧集的播出情况 比如总剧集数 是否完结
	show_entry = {}
	for show_row in shows_res.rows:
		# id 进度 是否完结
		show_entry[show_row[0]] = (show_row[1], show_row[2])
	show_ids = list(show_entry.keys())
	removed_ids = []
	for show in watched_shows:
		if str(show.tmdb) in show_ids:
			show_ids.remove(str(show.tmdb))
			removed_ids.append(str(show.tmdb))
		# 转为中文
		convert_result = tmdb.convert2zh_show(show)
		# 从tmdb查询出剧集是否完结   0: 未完结  1:完结
		is_ended = convert_result[1]
		# 从tmdb查询出剧集总剧数
		seasons_from_tmdb = convert_result[2]
		# 剧观看进度
		season_progress = f'第{len(show.seasons)}季/共{len(seasons_from_tmdb)}季'
		if str(show.tmdb) not in removed_ids:
			# 创建InStatement集合  需切换为中文
			statements.append(Statement(sql_scripts.INSERT_TABLE_SHOW_STATEMENT, [show.tmdb,
			                                                                      show.title, show.overview, show.year,
			                                                                      show.poster, season_progress,
			                                                                      convert_result[0], show.rating,
			                                                                      '', show.plays, time_util.convert(
					show.last_watched_at), is_ended]))
		# 创建更新语句 主要用于更新剧集的完结状态 以及进度
		# 	如果进度是未完结 需要创建更新语句 如果季有更新 或者 完结状态有更新 则需要同步
		if len(show_entry) != 0 and (str(show.tmdb) in show_entry):
			old_max_season = int(show_entry[str(show.tmdb)][0].split('/')[1][:-1][1:])
			# 旧的状态
			old_status = show_entry[str(show.tmdb)][1]
			
			if old_max_season != len(seasons_from_tmdb) and old_status == is_ended:
				# 最大季有更新 但是完结状态没变
				status_update_statements.append(Statement(sql_scripts.UPDATE_SHOW_SEASON_PROGRESS_BY_ID, season_progress ,show.tmdb))
			elif old_max_season == len(seasons_from_tmdb) and old_status != is_ended:
				# 最大季无更新 可能是集更新完毕 剧集完结
				status_update_statements.append(Statement(sql_scripts.UPDATE_SHOW_IS_ENDED_BY_ID, is_ended ,show.tmdb))
			elif old_max_season != len(seasons_from_tmdb) and old_status != is_ended:
				# 最大季和完结状态都有更新
				status_update_statements.append(Statement(sql_scripts.UPDATE_SHOW_SEASON_PROGRESS_IS_ENDED_BY_ID,season_progress, is_ended , show.tmdb))
	
	client.batch(statements)
	# 删除数据库中trakt已标记未观看的电影 保持与trakt同步
	delete_statements = []
	for show_id in show_ids:
		delete_statements.append(
			Statement(sql_scripts.DELETE_SHOW_BY_ID, [show_id]))
	client.batch(delete_statements)
	# 更新剧集状态
	client.batch(status_update_statements)
	index_data = base64_util.index_shows(watched_shows=watched_shows)
	# 如果索引表中不存在剧集索引，则新增剧集索引
	if len(client.execute(sql_scripts.SELECT_LOCAL_SEARCH_BY_TYPE, ['show']).rows) == 0:
		logger.info('索引表中不存在剧集索引,新增剧集索引...')
		client.execute(sql_scripts.INSERT_TABLE_LOCAL_SEARCH_STATEMENT, [
			'show', index_data])
		logger.info('新增剧集索引成功!')
	else:
		# 如果索引表中存在电影索引，则更新电影索引
		logger.info('索引表中存在剧集索引,更新剧集索引...')
		client.execute(sql_scripts.UPDATE_TABLE_LOCAL_SEARCH_STATEMENT, [
			index_data, 'show'])
		logger.info('更新剧集索引成功!')
	logger.info('更新剧集观看进度成功!')
	# 只要有新增或者删除或者死链更新 则返回True 表示需要刷新缓存
	return len(statements) != 0 or len(delete_statements) != 0 or len(dead_links_statements) != 0
