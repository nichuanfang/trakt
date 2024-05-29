# 创建刮削记录表 用于记录已刮削的电影和剧集 字段有 tmdb_id(主键), type(电影/剧集), name(中文名称), last_updated_at(更新时间)
# TABLE_SCRAPING_RECORD_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='scraping_record'"
#  创建刮削记录表  tmdb_id(主键), type(电影/剧集), name(中文名称), share_link(分享链接), last_updated_at(更新时间)
# CREATE_TABLE_SCRAPING_RECORD = "CREATE TABLE scraping_record ( tmdb_id TEXT PRIMARY KEY, type TEXT, name TEXT, share_link TEXT ,last_updated_at TEXT )"
# 根据tmdb_id查询刮削记录 用于判断是否存在已刮削好的链接
# SELECT_SCRAPING_RECORD_BY_ID = "SELECT * FROM scraping_record WHERE tmdb_id = ?"

# 下面两个是api模块的sql语句
# 插入刮削记录
# INSERT_TABLE_SCRAPING_RECORD_STATEMENT = "INSERT INTO scraping_record (tmdb_id, type, name, last_updated_at) VALUES (?, ?, ?, ?)"
# 更新刮削记录
# UPDATE_TABLE_SCRAPING_RECORD_STATEMENT = "UPDATE scraping_record SET type = ?, name = ?, last_updated_at = ? WHERE tmdb_id = ?"


# 判断电影表是否存在
TABLE_MOVIE_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='movie'"
# 初始化电影表
CREATE_TABLE_MOVIE = "CREATE TABLE movie ( movie_id TEXT PRIMARY KEY, movie_name TEXT, movie_description TEXT, release_year TEXT, cover_image_url TEXT, area TEXT ,rating TEXT, share_link TEXT, plays INTEGER , last_watched_at TEXT)"
# 创建电影表索引
CREATE_INDEX_MOVIE = "CREATE INDEX idx_movie_name ON movie (movie_name)"
# 插入电影表数据
INSERT_TABLE_MOVIE_STATEMENT = "INSERT INTO movie (movie_id, movie_name, movie_description, release_year, cover_image_url, area ,rating, share_link, plays , last_watched_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
# 根据id查询电影
SELECT_MOVIE_BY_ID = "SELECT share_link FROM movie WHERE movie_id = ?"
# 查询所有的电影ID
SELECT_ALL_MOVIE = "SELECT movie_id FROM movie"
#  根据id删除电影
DELETE_MOVIE_BY_ID = "DELETE FROM movie WHERE movie_id = ?"
#  根据id更新电影链接
UPDATE_MOVIE_LINK_BY_ID = "UPDATE movie SET share_link = ? WHERE movie_id = ?"


# 判断剧集表是否存在
TABLE_SHOW_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='show'"
# 创建剧集表
CREATE_TABLE_SHOW = "CREATE TABLE  show ( show_id TEXT PRIMARY KEY, show_name TEXT, show_description TEXT, release_year TEXT, cover_image_url TEXT,season_progress TEXT,episode_progress TEXT, area TEXT ,rating TEXT, share_link TEXT, plays INTEGER, last_watched_at TEXT)"
# 创建剧集表索引
CREATE_INDEX_SHOW = "CREATE INDEX  idx_show_name ON show (show_name)"
# 插入剧集表数据
INSERT_TABLE_SHOW_STATEMENT = "INSERT INTO show (show_id, show_name, show_description, release_year, cover_image_url,season_progress,episode_progress,area ,rating, share_link, plays, last_watched_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

# 判断索引表是否存在
TABLE_LOCAL_SEARCH_EXISTS = "SELECT name FROM sqlite_master WHERE type='table' AND name='local_search'"
# 创建hexo-blog的索引表LOCAL_SEARCH   type: movie, show
CREATE_TABLE_LOCAL_SEARCH = "CREATE TABLE local_search ( id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, b64_index TEXT );"
#  根据类型查询索引表数据
SELECT_LOCAL_SEARCH_BY_TYPE = "SELECT * FROM local_search WHERE type = ?"
# 插入索引表数据
INSERT_TABLE_LOCAL_SEARCH_STATEMENT = "INSERT INTO local_search (type, b64_index) VALUES (?, ?)"
# 更新索引表的b64_index
UPDATE_TABLE_LOCAL_SEARCH_STATEMENT = "UPDATE local_search SET b64_index = ? WHERE type = ?"
