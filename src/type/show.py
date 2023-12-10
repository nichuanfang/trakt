# 剧集类

class Show:

    def __init__(self, name, season, episode, path, size, time, subtitle, magnet, torrent):
        self.name = name
        self.season = season
        self.episode = episode
        self.path = path
        self.size = size
        self.time = time
        self.subtitle = subtitle
        self.magnet = magnet
        self.torrent = torrent

    def __str__(self):
        return self.name + ' ' + self.season + ' ' + self.episode + ' ' + self.path + ' ' + self.size + ' ' + self.time + ' ' + self.subtitle + ' ' + self.magnet + ' ' + self.torrent
