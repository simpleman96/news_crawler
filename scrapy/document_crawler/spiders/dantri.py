# -*- coding: utf-8 -*-
import scrapy
import re


class DantriSpider(scrapy.Spider):
    name = 'dantri'
    allowed_domains = ['dantri.com.vn']
    start_urls = [
        'https://dantri.com.vn/event/ca-nuoc-phong-chong-dich-corona-3813.htm'
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_path = 'output/dantri_docs.txt'

    def parse(self, response):
        next_page_link = response.xpath("//div[@class=\'fr\']/a/@href").extract_first()
        if next_page_link is not None:
            links = response.xpath("//*[@id=\"listcheckepl\"]//div/h2/a/@href").extract()
            links += response.xpath("//*[@id=\"listcheckepl\"]//div/div/h3/a/@href").extract()
            links += [next_page_link]

            for link in links:
                if link is not None:
                    link = response.urljoin(link)
                    yield scrapy.Request(link, callback=self.parse)
        else:
            date_time = response.xpath("//*[@id=\"ctl00_IDContent_ctl00_divContent\"]/div/span/text()").extract_first()
            date_time = clear_string(date_time)

            title_doc = response.xpath("//*[@id=\"ctl00_IDContent_ctl00_divContent\"]/h1/text()").extract_first()
            title_doc = clear_string(title_doc)

            tags = response.xpath("//*[@id=\"divNewsContent\"]//span[@class=\"news-tags-item\"]/a/text()").extract()
            tags = [clear_string(x) for x in tags]
            tags_str = '<>'.join(tags)

            texts = response.xpath("//*[@id=\"divNewsContent\"]/p//text()").extract()
            text_str = clear_string(' '.join(texts))
            with open(self.output_path, 'a') as valid_f:
                with open(self.output_path, 'a') as error_f:
                    try:
                        print('Valid===={}'.format(response.url))
                        line = response.url \
                               + '|' + date_time \
                               + '|' + tags_str \
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
