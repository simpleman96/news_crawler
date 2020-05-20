# -*- coding: utf-8 -*-
import scrapy
import re
from time import sleep
import json
import xml.etree.ElementTree as ET


class EVNExpress(scrapy.Spider):
    name = 'evnexpress'
    allowed_domains = ['e.vnexpress.net']
    start_urls = [
        ''
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_path = 'output/evnexpress_docs.txt'
        self.current_page = 2
        # self.

    def start_requests(self):
        yield scrapy.FormRequest('https://e.vnexpress.net/search/loadmore',
                                 method="POST",
                                 headers={"accept": "application/json, text/javascript, */*; q=0.01",
                                          "accept-encoding": "gzip, deflate, br",
                                          "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7,fr-FR;q=0.6,fr;q=0.5",
                                          # "content-length": "197",
                                          "content-type": "application/x-www-form-urlencoded",
                                          "cookie": """_ga=GA1.2.781012389.1535376355; __gads=ID=a4f7d5b20a0c4059:T=1553333412:S=ALNI_MbfOLvU3tFdiGb6poXI78qohXCbdA; fosp_aid=uqb0j4j3kxs6emuw; login_system=1; orig_aid=uqb0j4j3kxs6emuw; fosp_gender=3; fosp_country=vn; fosp_isp=12; _gaexp=GAX1.2.UC11UjtnTVqkxzcIzUjX6w.18479.1; sizefontcookie=100; _gid=GA1.2.370667368.1589909139; fosp_loc=24-2-vn; fosp_location=24; readed_news=%5B4065788%5D; trc_cookie_storage=taboola%2520global%253Auser-id%3Df71ddd5c-a721-47d3-9769-ba72002af040-tuct24dbf76; old_version=0; smartbanner=hide; device_env=4; cdevice=4; device_env_real=4; sw_version=1; num_load_newsletter=5; _gat=1; _gat_UA-138647571-1=1; _dc_gtm_UA-50285069-28=1; _pk_ref=%5B%22%22%2C%22%22%2C1590001978%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_cvar=%7B%224%22%3A%5B%22fosp_aid%22%2C%22uqb0j4j3kxs6emuw%22%5D%2C%227%22%3A%5B%22fosp_aid_bk%22%2C%22uqb0j4j3kxs6emuw%22%5D%2C%228%22%3A%5B%22eatv%22%2C%2228-03-2014%22%5D%2C%229%22%3A%5B%22fosp_session%22%2C%22zmzqzqzi1uzq1vznzkzqzg1tzhzj1y21zdzizmzrzqzqzjzqziznzjzdzizdzizmzrzqzqzjzqziznzjzdzizmzrzqzqzjzqziznzjzdzizdzjzdzjzdzezdzg%22%5D%2C%2210%22%3A%5B%22fosp_gender%22%2C%220%22%5D%7D; "_pk_ses=*; fblg=true; network_speed=5615493.11; display_cpd=6; _pk_id=d318c4140539defa.1535376355.32.1590001986.1589996465.; cpx_ar=11""",
                                          "origin": "https://e.vnexpress.net",
                                          "referer": "https://e.vnexpress.net/search?q=covid-19&csrf=2577e02d43ef0d05b4d854dd7243251e",
                                          "sec-fetch-mode": "cors",
                                          "sec-fetch-site": "same-origin",
                                          "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                                          "x-requested-with": "XMLHttpRequest"},
                                 formdata={
                                     "cate_id": {"cate_code": "", "q": "covid-19", "latest": "", "media_type": "all",
                                                 "date_format": "all", "search_f": "title,lead"},
                                     "page": str(self.current_page)},
                                 callback=self.parse)

    def parse(self, response):
        url = "https://e.vnexpress.net/search/loadmore"
        current_url = response.url
        if current_url == url:
            sleep(0.05)
            self.current_page += 1

            json_response = json.loads(response.text)
            html_field = json_response['message']
            html_content = html_field.replace("\t", " ").replace("\n", " ").replace("\r", " ").replace("\"",
                                                                                                       "\"").replace(
                "\/", "/")

            sub_links = re.compile(
                r"<h4 +class=\"title_news_site\"><a +href=\"(https://e\.vnexpress\.net.+)\">.+</h4>").findall(
                html_content)
            for link in sub_links:
                if link is not None:
                    link = response.urljoin(link)
                    yield scrapy.Request(link, callback=self.parse)

            # if not json_response['end']:
            #     yield scrapy.FormRequest('https://e.vnexpress.net/search/loadmore',
            #                              formdata={
            #                                  "cate_id": {"cate_code": "", "q": "covid-19", "latest": "",
            #                                              "media_type": "all",
            #                                              "date_format": "all", "search_f": "title,lead"},
            #                                  "page": str(self.current_page)},
            #                              callback=self.parse)
        else:
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
