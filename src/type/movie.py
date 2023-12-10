# 电影类

class Movie:
    def __init__(self, name, url, img, score, director, actor, category, area, year, language, release_time, length, introduction):
        """_summary_

        Args:
            name (_type_): _description_
            url (_type_): _description_
            img (_type_): _description_
            score (_type_): _description_
            director (_type_): _description_
            actor (_type_): _description_
            category (_type_): _description_
            area (_type_): _description_
            year (_type_): _description_
            language (_type_): _description_
            release_time (_type_): _description_
            length (_type_): _description_
            introduction (_type_): _description_
        """

        self.name = name
        self.url = url
        self.ali_url = None
        self.img = img
        self.score = score
        self.category = category
        self.area = area
        self.year = year
        self.language = language
        self.release_time = release_time
        self.introduction = introduction

    def __str__(self):
        return 'Movie: name = %s, url = %s, img = %s, score = %s, director = %s, actor = %s, category = %s, area = %s, year = %s, language = %s, release_time = %s, length = %s, introduction = %s' % (self.name, self.url, self.img, self.score, self.director, self.actor, self.category, self.area, self.year, self.language, self.release_time, self.length, self.introduction)

    def __repr__(self):
        return self.__str__()
