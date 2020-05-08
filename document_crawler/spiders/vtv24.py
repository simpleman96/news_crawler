# -*- coding: utf-8 -*-
import scrapy
import re
from time import sleep

class VTV24Spider(scrapy.Spider):
    name = 'vtv24'
    allowed_domains = ['vtv.vn']
    start_urls = [
        'https://vtv.vn/timeline-thread/242/trang-1.htm'
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_path = 'output/vtv24_docs.txt'

    def parse(self, response):
        if response is not None:
            url_template = 'https://vtv.vn/timeline-thread/242/trang-'
            current_url = response.url
            if current_url.startswith(url_template):
                sleep(0.05)
                current_index = int(current_url[41:-4])
                next_index = current_index + 1
                next_page_link = url_template + str(next_index) + '.htm'
                sub_links = response.xpath("/html/body/li/h4/a/@href").extract()
                sub_links += [next_page_link]
                for link in sub_links:
                    if link is not None:
                        link = response.urljoin(link)
                        yield scrapy.Request(link, callback=self.parse)
            else:
                date_time = response.xpath("//h1[@class=\"title_detail\"]/text()").extract_first()
                date_time = clear_string(date_time)

                title_doc = response.xpath("//h1[@class=\"title_detail\"]/text()").extract_first()
                title_doc = clear_string(title_doc)

                tags = response.xpath("//a[@itemprop=\"keywords\"]/text()").extract()
                tags = [clear_string(x) for x in tags]
                tags_str = '<>'.join(tags)

                texts = response.xpath("//*[@id=\"entry-body\"]/p//text()").extract()
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
