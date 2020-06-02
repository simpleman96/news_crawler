# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from datetime import datetime
from pymongo import MongoClient
import traceback

class FoxNewsSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['www.foxnews.com']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mongo_client = MongoClient("localhost", 27011)
        with open("input/foxnews_covid_links.txt", "r") as f:
            self.start_urls = f.read().splitlines()

    def parse(self, response):
        try:
            if ".video." in response.url:
                pass
            date_time = response.xpath("//div/time/text()").extract_first()
            date_time = clear_string(date_time)

            title_doc = response.xpath("//main/article/header/h1/text()").extract_first()
            title_doc = clear_string(title_doc)

            normal_lines = response.xpath("//div[@class=\"article-body\"]/p/text()").extract()
            text_str = clear_string(' '.join(normal_lines))
            url = response.url
            key = str(int(hashlib.sha1(url.encode()).hexdigest(), 16) % 10 ** 8)
            doc = {"key": key,
                   "domain": self.allowed_domains[0],
                   "url": url,
                   "time": datetime.now().strftime("%Y%m%d_%H%M%S") + " - " + date_time,
                   "title": title_doc,
                   "content": text_str,
                   "status": 0}
            save_status = self.save_doc("tich_hop_xu_ly_du_lieu", "covid_news_data", key, doc)
            if save_status:
                print(f"Save doc: {key} : {url} success!")
            else:
                print(f"Save doc: {key} : {url} already saved!")
        except Exception:
            traceback.print_exc()
            print(f"Parsing {response.url} got exception!")
            yield scrapy.Request(response.url, callback=self.parse)

    def reconnect(self):
        self.mongo_client = MongoClient("localhost", 27011)

    def save_doc(self, db_name, collection_name, key, doc):
        collection = self.mongo_client[db_name][collection_name]
        find_collection = collection.find({"key": key})
        if find_collection.count() == 0:
            try:
                collection.insert_one(doc)
                return True
            except Exception:
                traceback.print_exc()
                self.reconnect()
                raise Exception("Save driver got exception")
        else:
            return False

def clear_string(x):
    try:
        x = re.sub('\n', ' ', x)
        x = re.sub('\r', ' ', x)
        x = re.sub('\t', ' ', x)
        x = re.sub('\|', ' ', x)
    except:
        x = "__clean_error__"
    return ' '.join(x.split())



