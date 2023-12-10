# 判断电影表是否存在
TABLE_MOVIE_EXISTS = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='movie';"
# 初始化电影表
CREATE_TABLE_MOVIE = "CREATE TABLE movie ( id INTEGER PRIMARY KEY AUTOINCREMENT, movie_id INTEGER NOT NULL, name TEXT NOT NULL, duration INTEGER NOT NULL, type TEXT NOT NULL, FOREIGN KEY (movie_id) REFERENCES movie (id) );"
# 判断剧集表是否存在
TABLE_SHOW_EXISTS = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='show';"
# 创建剧集表
CREATE_TABLE_SHOW = "CREATE TABLE show ( id INTEGER PRIMARY KEY AUTOINCREMENT, show_id INTEGER NOT NULL, start_time TEXT NOT NULL, FOREIGN KEY (movie_id) REFERENCES movie (id) );"
