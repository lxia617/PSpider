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
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_shiguang_movies():
    connection = pymongo.MongoClient(
        'localhost',
        27017
    )
    db = connection['shiguang']
    collection = db['list']

    url_index_list = []
    url_index_list.append("http://movie.mtime.com/movie/list/")
    for i in range(2, 14,1):
        url_index_list.append("http://movie.mtime.com/movie/list/index-" + str(i) + ".html")

    # 找到所有的列表的页面
    url_list = []
    for url in url_index_list:
        html = urlopen(url)
        soup = BeautifulSoup(html.read())
        div_movies = soup.find_all("dd", class_="tr px14 mt15")
        for item in div_movies:
            if "list" in item.find("a").get("href"):
                url_list.append(item.find("a").get("href"))

    print("url_list:", url_list)
    
    lists = []
    connection = pymongo.MongoClient(
        'localhost',
        27017
    )
    db = connection['shiguang']
    collection = db['list']
    # url_list = ["http://movie.mtime.com/list/217.html"]
    # 找到所有的列表的标题
    for url in url_list:
        # one_list 是一个列表，可能包含100个电影，只获得电影的标题
        list_dict = {}
        html = urlopen(url)
        soup = BeautifulSoup(html)
        try:
            list_dict["title"] = soup.find("h2").get_text()
            list_dict["desc"] = soup.find("h3").get_text()
            list_dict["url"] = url
            list_dict["movies"] = []
            pagerPopUl = soup.find("ul", id="pagerPopUl")
            if pagerPopUl:
                # http://movie.mtime.com/list/1473.html
                lis = pagerPopUl.find_all("li")
            else:
                lis = soup.find_all("div", class_="texter")
                if len(lis) == 0:
                    # http://movie.mtime.com/list/217.html
                    if soup.find("div", class_ = "top_nlist"):
                        lis = soup.find("div", class_ = "top_nlist").find_all("h3")
                    else:
                        # http://movie.mtime.com/list/1369.html
                        lis = soup.find("div", class_ = "top_piclist").find_all("h3")
            
            for li in lis:
                list_dict["movies"].append(li.find("a").get_text())
            
            lists.append(list_dict)
            collection.insert_one(list_dict)
        except:
            print(url, " ", sys.exc_info(), list_dict, "\n\n")
    
    print(lists)
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    get_shiguang_movies()
