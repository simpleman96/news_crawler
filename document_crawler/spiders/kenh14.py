# -*- coding: utf-8 -*-
import scrapy
import re

regex = re.compile("\n")


class Kenh14Spider(scrapy.Spider):
    name = 'kenh14'
    allowed_domains = ['kenh14.vn']
    start_urls = [
        # 'http://kenh14.vn/cach-day-3-nam-lam-tay-tung-viet-tam-thu-tha-thiet-duoc-vao-doi-tuyen-viet-nam-20181215224913227.chn'
        # 'http://kenh14.vn/hang-trieu-cdv-viet-nam-do-ra-duong-an-mung-chien-thang-chung-ta-la-nhung-nha-vo-dich-20181215203028133.chn'
        'http://kenh14.vn/xuan-truong-lang-le-dung-nhin-dong-doi-tung-ho-thay-park-len-cao-20181215230442445.chn'
    ]

    def parse(self, response):
        global regex
        output_path = 'sport_kenh14_docs'
        cate_filter = 'Sport'
        date_time = response.selector.xpath(
            '//div[@class=\'kbwc-meta\']/span[@class=\'kbwcm-time\']/@title').extract_first()
        title_doc = response.selector.xpath('//h1[@class=\'kbwc-title\']/text()').extract_first()
        category = response.selector.xpath('//li[@class=\'kmli active\']/a/@title').extract_first()
        if category == cate_filter:
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
                        out_f.write(regex.sub(' ', line) + "\n")
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
