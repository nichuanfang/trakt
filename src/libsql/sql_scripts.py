# 判断电影表是否存在
TABLE_MOVIE_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='movie'"
# 初始化电影表
CREATE_TABLE_MOVIE = "CREATE TABLE movie ( movie_id TEXT PRIMARY KEY, movie_name TEXT, mvie_description TEXT, release_year TEXT, cover_image_url TEXT, area TEXT ,rating TEXT, share_link TEXT, plays INTEGER , last_watched_at TEXT)"
# 创建电影表索引
CREATE_INDEX_MOVIE = "CREATE INDEX idx_movie_name ON movie (movie_name)"
# 插入电影表数据
INSERT_TABLE_MOVIE_STATEMENT = "INSERT INTO movie (movie_id, movie_name, movie_description, release_year, cover_image_url, area ,rating, share_link, plays , last_watched_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
# 根据id查询电影
SELECT_MOVIE_BY_ID = "SELECT * FROM movie WHERE movie_id = ?"


# 判断剧集表是否存在
TABLE_SHOW_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='show'"
# 创建剧集表
CREATE_TABLE_SHOW = "CREATE TABLE  show ( show_id TEXT PRIMARY KEY, show_name TEXT, show_description TEXT, release_year TEXT, cover_image_url TEXT, area TEXT ,rating TEXT, share_link TEXT, plays INTEGER, last_watched_at TEXT)"
# 创建剧集表索引
CREATE_INDEX_SHOW = "CREATE INDEX  idx_show_name ON show (show_name)"
# 插入剧集表数据
INSERT_TABLE_SHOW_STATEMENT = "INSERT INTO show (show_id, show_name, show_description, release_year, cover_image_url, area ,rating, share_link, plays, last_watched_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"


# 判断季(剧集)表是否存在
TABLE_SEASON_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='season'"
#  创建季(剧集)表
CREATE_TABLE_SEASON = "CREATE TABLE  season ( season_id TEXT PRIMARY KEY, show_id TEXT, season_number TEXT, season_description TEXT, release_year TEXT, rating TEXT, FOREIGN KEY (show_id) REFERENCES show (show_id) )"
# 插入季(剧集)表数据
INSERT_TABLE_SEASON_STATEMENT = "INSERT INTO season (season_id, show_id, season_number, season_description, release_year, rating) VALUES (?, ?, ?, ?, ?, ?)"
