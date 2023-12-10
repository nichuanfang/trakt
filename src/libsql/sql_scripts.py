# 判断电影表是否存在
TABLE_MOVIE_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='movie'"
# 初始化电影表
CREATE_TABLE_MOVIE = "CREATE TABLE movie ( movie_id TEXT PRIMARY KEY, movie_name TEXT, movie_description TEXT, release_year TEXT, cover_image_url TEXT, rating TEXT, share_link TEXT )"
# 创建电影表索引
CREATE_INDEX_MOVIE = "CREATE INDEX idx_movie_name ON movie (movie_name)"


# 判断剧集表是否存在
TABLE_SHOW_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='show'"
# 创建剧集表
CREATE_TABLE_SHOW = "CREATE TABLE  show ( show_id TEXT PRIMARY KEY, show_name TEXT, show_description TEXT, release_year TEXT, cover_image_url TEXT, rating TEXT, share_link TEXT )"
# 创建剧集表索引
CREATE_INDEX_SHOW = "CREATE INDEX  idx_show_name ON show (show_name)"


# 判断季(剧集)表是否存在
TABLE_SEASON_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='season'"
#  创建季(剧集)表
CREATE_TABLE_SEASON = "CREATE TABLE  season ( season_id TEXT PRIMARY KEY, show_id TEXT, season_number TEXT, season_description TEXT, release_year TEXT, rating TEXT, FOREIGN KEY (show_id) REFERENCES show (show_id) )"
