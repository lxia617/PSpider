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

def get_douban_movies():
    #连接数据库
    end_year = 1950
    start_year = 1900

    # 构造爬虫
    dou_spider = spider.WebSpider(MovieFetcher(start_year = start_year, end_year = end_year), MovieParser(max_deep=-1), MovieSaver(start_year = start_year, end_year = end_year), spider.UrlFilter())
    
    for year in range(end_year, start_year, -1):
      dou_spider.set_start_url("https://movie.douban.com/tag/" + str(year) + "?type=O&start=0", ("index", str(year)), priority=1)

    dou_spider.start_work_and_wait_done(fetcher_num=20)
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    get_douban_movies()
