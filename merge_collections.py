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

def remove_duplicate_urls():

    #连接数据库
    connection = pymongo.MongoClient(
        'localhost',
        27017
    )
    db = connection['douban_merge']
    collection_names = db.collection_names()
    merge_collection = connection['douban']['movie']
    for collection_name in collection_names:
        collection = db[collection_name]
        print(collection_name, " has count:", collection.find().count())
        for doc in collection.find():
            url = doc["m_url"]
            if (merge_collection.find({"m_url" : url}).count() == 0):
                merge_collection.insert_one(doc)

    return


def remove_duplicate_urls_using_set():

    #连接数据库
    connection = pymongo.MongoClient(
        'localhost',
        27017
    )
    db = connection['douban']
    collection_names = db.collection_names()
    merge_collection = connection['douban_merge']['movie']
    url_dict = {}
    duplicate_count = 0
    for collection_name in collection_names:
        collection = db[collection_name]
        for doc in collection.find():
            url = doc["m_url"]
            if url in url_dict:
                if url_dict[url] == 1:
                    duplicate_count = duplicate_count + 1
                print(duplicate_count, ":", url, ":", url_dict[url])
                url_dict[url] = url_dict[url] + 1
            else:
                url_dict[url] = 1
                del doc['_id']
                merge_collection.insert_one(doc)

    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    #remove_duplicate_urls()
    remove_duplicate_urls_using_set()
