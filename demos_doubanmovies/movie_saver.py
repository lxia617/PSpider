# _*_ coding: utf-8 _*_

import spider
import pymongo
import pymysql

class MovieSaver(spider.Saver):
    key_names = ["m_url","m_name","m_year","m_imgurl","m_director","m_writer","m_actors",
                 "m_genre","m_country","m_language","m_release","m_season","m_jishu","m_length","m_alias","m_website","m_dbsite",
                 "m_score", "m_ratingsum", "m_summary","m_likes", "m_tags", "m_doulist"]

    def __init__(self, start_year, end_year):
        spider.Saver.__init__(self)
        connection = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = connection['douban']
        self.collection = db['movie' + str(end_year) + '_' + str(start_year)]
        return

    def item_save(self, url, keys, item):
        '''
        self.cursor.execute("insert into t_doubanmovies (m_url, m_name, m_year, m_imgurl, m_director, m_writer, m_actors, "
                            "m_genre, m_country, m_language, m_release, m_season, m_jishu, m_length, m_alias, m_website, m_dbsite, "
                            "m_imdb, m_score, m_comment, m_starpercent)"
                            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                            [i.strip() if i is not None else "" for i in item])
        '''
        movie = {}

        for i in range(len(MovieSaver.key_names)):
          movie[self.key_names[i]] = item[i].strip()

        if self.collection.find(movie).count() == 0:
            #print(movie, "exist")
            self.collection.insert_one(movie).inserted_id
        return True
