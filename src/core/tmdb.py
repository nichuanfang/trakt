import os
from trakt.movies import Movie
from trakt.tv import TVShow, TVSeason, TVEpisode
from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import TV

# 初始化tmdb
tmdb = TMDb()
#  设置tmdb api key
tmdb.api_key = os.environ.get('TMDB_API_KEY')
# 设置tmdb的语言为中文
tmdb.language = 'zh-CN'
#  初始化电影和剧集对象
tmdb_movie = Movie()
tmdb_tv = TV()


def convert2zh(movie: Movie):
    details = tmdb_movie.details(movie_id=movie.tmdb)
    # 标题
    movie.title = details.title
    # 剧情简介
    movie.overview = details.overview
    # 评分
    movie.rating = details.vote_average
    # 封面图片
    movie.poster = details.poster_path
