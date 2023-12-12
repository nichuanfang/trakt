import base64
import json
from trakt.movies import Movie
from trakt.tv import TVShow, TVSeason, TVEpisode


def index(watched_movies: list[Movie] = None, watched_shows: list[TVShow] = None):
    """生成电影或剧集的base64形式的索引

    Returns:
        [type]: 索引
    """
    movie_data = []
    for movie in watched_movies:
        movie_data.append(
            {
                'title': movie.title,
                'content': movie.overview,
                'url': f'/culture/movies/{movie.tmdb}'
            }
        )
    # 将movie_data转为json字符串  然后转为base64
    return base64.b64encode(json.dumps(movie_data).encode('utf-8')).decode('utf-8')
