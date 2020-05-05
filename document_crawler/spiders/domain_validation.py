# -*- coding: utf-8 -*-
import scrapy
import re

regex = re.compile('[0-9a-zàáảãạăắằẵặẳâầấậẫẩđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ .,!;]+')


def check_content(in_string):
    global regex
    if len(regex.sub('', in_string)) < 30:
        return True
    else:
        return False


class DomainValidationSpider(scrapy.Spider):
    name = 'domain_validation'

    def __init__(self, *args, **kwargs):
        super(DomainValidationSpider, self).__init__(*args, **kwargs)
        domain_path = '/home/dat/PycharmProjects/document_crawler/list_domain_test'
        with open(domain_path, 'r') as f:
            lines = f.read().splitlines()

        for line in lines:
            self.start_urls.append('http://' + line)

    def parse(self, response):
        wrong_path = 'wrong_domain'
        valid_path = 'valid_domain'

        if response.status != 200:
            with open(wrong_path, 'a') as wrong_f:
                wrong_f.write(response.url + ': Error Domain\n')
            pass

        title = response.selector.xpath('/head/title/text()').extract_first()
        with open(valid_path, 'a') as valid_f:
            with open(wrong_path, 'a') as wrong_f:
                if check_content(title):
                    valid_f.write(response.url + '|' + title + '\n')
                else:
                    wrong_f.write(response.url + '|' + title + '\n')
