# _*_ coding: utf-8 _*_

"""
test_demos.py by xianhu
"""

import re
import spider
import pymongo
import logging
import requests
import json
from bs4 import BeautifulSoup
from demos_doubanmovies import MovieFetcher, MovieParser, MovieSaver
from demos_dangdang import BookFetcher, BookParser, BookSaver

class DoubanMovieFetcher():
    #初始化时候读取爬过的detail urls
    def __init__(self):
        #决定初始年份和结束年份
        self.end_year = 1950
        self.start_year = 1900
        connection = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = connection['douban']
        self.detail_urls = set()
        self.movie_collection = db['movie']
        for doc in self.movie_collection.find():
            url = doc["m_url"]
            self.detail_urls.add(url)

        print("unique crawled detail urls count:", len(self.detail_urls))

        #得到所有解析过的 tag_urls 列表
        self.tag_url_collection = db['tag_url']
        self.tag_urls = set()
        for doc in self.tag_url_collection.find():
            url = doc["m_url"]
            self.tag_urls.add(url)
        print("year&start index crawled urls count:", len(self.tag_urls))

        self.todo_collection = db['todo_url']
        return
    
    #根据年份获取detail urls放入数据库
    def get_douban_tag_urls(self):

        movie_fetcher = MovieFetcher(start_year = self.start_year, end_year = self.end_year)

        # 解析所有的索引页面，如果没有爬过，就加到要爬的 detail_urls 里面
        detail_urls = []
        for year in range(self.end_year, self.start_year, -1):
            start = 0
            while True:
                url_year_start = "https://movie.douban.com/tag/" + str(year) + "?type=O&start=" + str(start)
                #如果爬过这个year+start的组合
                if url_year_start in self.tag_urls:
                    continue
                code, content = movie_fetcher.url_fetch(url_year_start)
                if code != 1:
                    break
                
                soup = BeautifulSoup(content, "html5lib")
                div_movies = soup.find_all("a", class_="nbg", title=True)
                print(url_year_start, "div_movies len:", len(div_movies))
                for item in div_movies:
                    detail_url = item.get("href")
                    if detail_url not in self.detail_urls:
                        self.todo_collection.insert_one({"m_url" : detail_urls})
                #如果数目不是20，可能是因为被墙了或者到结尾了，这个年份就不再继续
                if len(div_movies) != 20:
                    print("soup:", soup)
                    break

    # 爬豆瓣数据不重复爬，如果被禁了从数据库看看哪些爬过
    def get_douban_movies(self):
        movie_parser = MovieParser()
        movie_saver = MovieSaver(start_year = self.start_year, end_year = self.end_year)
        # 解析detail页面
        for detail_url in self.todo_collection.find():
            code, content = movie_fetcher.url_fetch(url_year_start)
            soup = BeautifulSoup(content, "html5lib")
            movie = movie_parser.parse_detail(soup, detail_url)
            movie_saver.item_save(url = detail_url, item = movie)
        return

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    fetcher = DoubanMovieFetcher()
    fetcher.get_douban_tag_urls()
