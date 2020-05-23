# -*- coding: utf-8 -*-
import scrapy
import re


class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    allowed_domains = ['e.vnexpress.net']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_path = 'output/vnexpress_docs.txt'
        with open("input/evnexpress_covid_links.txt", "r") as f:
            self.start_urls = f.read().splitlines()

    def parse(self, response):
        date_time = response.xpath("//div[@class=\"author\"]/text()").extract()[1]
        date_time = clear_string(date_time)

        title_doc = response.xpath("//h1[@class=\"title_post\"]/text()").extract_first()
        title_doc = clear_string(title_doc)

        first_line = response.xpath("//*[@id=\"detail_page\"]/div[1]/div[3]/h2/text()").extract_first()

        normal_lines = response.xpath("//*[@id=\"detail_page\"]/div[1]/div[3]/div[4]/p/text()").extract()
        text_str = clear_string(' '.join([first_line] + normal_lines))
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