# -*- coding: utf-8 -*-
import scrapy
import re


class FoxNewsSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['www.foxnews.com']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_path = 'output/foxnews_docs.txt'
        with open("input/foxnews_covid_links.txt", "r") as f:
            self.start_urls = f.read().splitlines()

    def parse(self, response):
        if ".video." in response.url:
            pass
        date_time = response.xpath("//div/time/text()").extract_first()
        date_time = clear_string(date_time)

        title_doc = response.xpath("//main/article/header/h1/text()").extract_first()
        title_doc = clear_string(title_doc)

        normal_lines = response.xpath("//div[@class=\"article-body\"]/p/text()").extract()
        text_str = clear_string(' '.join(normal_lines))
        with open(self.output_path, 'a') as valid_f:
            with open(self.output_path, 'a') as error_f:
                try:
                    print('Valid===={}'.format(response.url))
                    line = response.url \
                           + '|' + date_time \
                           + '|' + title_doc \
                           + '|' + text_str
                    valid_f.write(line + "\n")
                except:
                    print('Error===={}'.format(response.url))
                    error_f.write(response.url + "\n")

def clear_string(x):
    try:
        x = re.sub('\n', ' ', x)
        x = re.sub('\r', ' ', x)
        x = re.sub('\t', ' ', x)
        x = re.sub('\|', ' ', x)
    except:
        x = "__clean_error__"
    return ' '.join(x.split())