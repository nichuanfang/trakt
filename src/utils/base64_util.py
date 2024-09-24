import base64
import json

from trakt.movies import Movie
from trakt.tv import TVShow


def index_movies(watched_movies: list[Movie] = None):
	"""生成电影base64形式的索引

	Returns:
		[type]: 索引
	"""
	movie_data = []
	for movie in watched_movies:
		print(f'电影详情 {movie.__dict__} \n\n')
		movie_data.append(
			{
				'title': movie.title,
				'content': movie.overview,
				'url': f'/culture/movies/detail/?tmdb_id={movie.tmdb}'
			}
		)
	# 将movie_data转为json字符串  然后转为base64
	return base64.b64encode(json.dumps(movie_data).encode('utf-8')).decode('utf-8')


def index_shows(watched_shows: list[TVShow] = None):
	"""生成剧集的base64形式的索引

	Returns:
		[type]: 索引
	"""
	show_data = []
	for show in watched_shows:
		print(f'剧集详情 {movie.__dict__} \n\n')
		show_data.append(
			{
				'title': show.title,
				'content': show.overview,
				'url': f'/culture/shows/detail/?tmdb_id={show.tmdb}'
			}
		)
	# 将movie_data转为json字符串  然后转为base64
	return base64.b64encode(json.dumps(show_data).encode('utf-8')).decode('utf-8')
