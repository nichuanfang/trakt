import os

from tmdbv3api import Movie as TMDB_Movie
from tmdbv3api import TMDb
from tmdbv3api import TV as TMDB_TV
from trakt.movies import Movie
from trakt.tv import TVShow

from utils import area_util

# 初始化tmdb
tmdb = TMDb()
#  设置tmdb api key
tmdb.api_key = os.environ.get('TMDB_API_KEY')
# 设置tmdb的语言为中文
tmdb.language = 'zh-CN'
#  初始化电影和剧集对象
tmdb_movie = TMDB_Movie()
tmdb_tv = TMDB_TV()


def convert2zh_movie(movie: Movie):
	"""
	将电影的元信息转为中文
	@param movie:  电影对象
	@return: 处理好的国家名称
	"""
	details = tmdb_movie.details(movie_id=movie.tmdb)
	# 标题
	movie.title = details.title
	# 剧情简介
	movie.overview = details.overview
	# 评分
	movie.rating = details.vote_average
	# 封面图片
	movie.poster = details.poster_path
	# 获取iso_3166_1国家地区代码
	country_code = details.production_countries[0]['iso_3166_1']
	# 根据iso_3166_1国家代码获取国家名称
	country_name = area_util.get_country_name_by_code(country_code)
	return country_name


def convert2zh_show(show: TVShow):
	"""
	将剧集的元信息转为中文
	@param show:  剧集对象
	@return: 处理好的国家名称
	"""
	details = tmdb_tv.details(tv_id=show.tmdb)
	# 标题
	show.title = details.name
	# 剧情简介
	show.overview = details.overview
	# 评分
	show.rating = details.vote_average
	# 封面图片
	show.poster = details.poster_path
	# 获取iso_3166_1国家地区代码
	country_code = details.production_countries[0]['iso_3166_1']
	# 根据iso_3166_1国家代码获取国家名称
	country_name = area_util.get_country_name_by_code(country_code)
	is_ended = 0
	if details.status == 'Ended':
		is_ended = 1
	# 总季数
	seasons_from_tmdb = details.seasons
	return (country_name, is_ended, seasons_from_tmdb)
