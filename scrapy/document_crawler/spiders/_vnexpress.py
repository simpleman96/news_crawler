# -*- coding: utf-8 -*-
import scrapy
import re


class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    allowed_domains = ['e.vnexpress.net']
    start_urls = [
        'https://vnexpress.net/gan-100-canh-sat-dong-nai-bat-bang-giang-ho-4094652.html'
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_path = 'output/vnexpress_docs.txt'

    def parse(self, response):
        global regex
        date_time = response.xpath('//div[@class=\'header-content width_common\']/span[@class=\'date\']/text()').extract_first()
        title_doc = response.xpath('//div[@class=\'header-content width_common\']/h1[@class=\'title-detail\']//text()').extract_first()
        category = response.xpath('//div[@class=\'header-content width_common\']/ul[@class=\'breadcrumb\']//a/text()').extract_first()

        if category in self.allowed_cate:
            # content = response.selector.xpath('//div[@class=\'knc-content\']//p').extract_first()
            text = response.xpath('//article[@class=\'fck_detail\']//text()').extract_first()
            with open(self.output_path, 'a') as out_f:
                try:
                    text = re.sub('\n', ' ', text)
                    text = ' '.join(text.split())
                    if len(text) > 80:
                        line = date_time \
                               + '|' + category \
                               + '|' + title_doc \
                               + '|' + text
                        out_f.write(line + "\n")
                except:
                    print('Error')

            # next_page = response.selector.xpath('//div[@class=\'knc-rate-link\']/a/@href').extract_first()
            links = response.xpath('//article[@class=\'item-news full-thumb\']/h3[@class=\'item-news\']').extract()
            for link in links:
                next_page = link.xpath('a/@href').extract_first()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)
