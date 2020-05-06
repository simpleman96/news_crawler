# -*- coding: utf-8 -*-
import scrapy
import re

class Kenh14Spider(scrapy.Spider):
    name = 'kenh14'
    allowed_domains = ['kenh14.vn']
    start_urls = [
        'http://kenh14.vn/xuan-truong-lang-le-dung-nhin-dong-doi-tung-ho-thay-park-len-cao-20181215230442445.chn'
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allowed_cate = ['Sport']

    def parse(self, response):
        global regex
        output_path = 'sport_kenh14_docs'
        date_time = response.selector.xpath(
            '//div[@class=\'kbwc-meta\']/span[@class=\'kbwcm-time\']/@title').extract_first()
        title_doc = response.selector.xpath('//h1[@class=\'kbwc-title\']/text()').extract_first()
        category = response.selector.xpath('//li[@class=\'kmli active\']/a/@title').extract_first()
        if category in self.allowed_cate:
            # content = response.selector.xpath('//div[@class=\'knc-content\']//p').extract_first()
            texts = response.selector.xpath('//div[@class=\'knc-content\']//p//text()').extract()
            with open(output_path, 'a') as out_f:
                try:
                    for content in texts:
                        # content = temp.xpath('//text()').extract_first()
                        if len(content) > 80:
                            line = date_time \
                                   + '|' + category \
                                   + '|' + title_doc \
                                   + '|' + content
                            out_f.write(re.sub('\n', ' ', line) + "\n")
                        break
                except:
                    print('Error')

            # next_page = response.selector.xpath('//div[@class=\'knc-rate-link\']/a/@href').extract_first()
            links = response.selector.xpath('//li[@class=\'krwli\']')
            for link in links:
                next_page = link.xpath('a/@href').extract_first()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)
