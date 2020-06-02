from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from datetime import datetime
import traceback
import hashlib
from mongo_utils import MongoUtils


class EVnExpressCrawler(Thread):
    def __init__(self, domain):
        super().__init__()
        self.domain = domain
        self.url_queue = []
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path="chromedriver_linux64/chromedriver", chrome_options=options)
        self.driver.implicitly_wait(30)
        self.mongo_client = MongoUtils()

    def add_url(self, url):
        self.url_queue.append(url)

    def run(self):
        try:
            while True:
                if len(self.url_queue) > 0:
                    print(f"Current urls queue size {len(self.url_queue)}")
                    url = self.url_queue[0]
                    key = str(int(hashlib.sha1(url.encode()).hexdigest(), 16) % 10 ** 8)
                    if not self.mongo_client.check_doc_saved("tich_hop_xu_ly_du_lieu", "covid_news_data", key):
                        status = self.parser_doc(url)
                        if status:
                            self.url_queue.pop(0)
                        print(f"Save doc: {key} : {url} success!")
                    else:
                        self.url_queue.pop(0)
                        print(f"Doc: {key} : {url} already saved!")
                else:
                    time.sleep(1)
        finally:
            print("eVnexpress crawler got exception, terminating ...")
            self.driver.close()

    def parser_doc(self, url):
        try:
            self.driver.get(url)
            try:
                date_time = self.driver.find_elements_by_xpath("//div[@class=\"author\"]")[1]
                date_time = clear_string(date_time.text)
            except Exception:
                date_time = ""

            try:
                title_doc = self.driver.find_element_by_xpath("//h1[@class=\"title_post\"]")
                title_doc = clear_string(title_doc.text)
            except Exception:
                title_doc = ""

            try:
                first_line = self.driver.find_element_by_xpath("//*[@id=\"detail_page\"]/div[1]/div[3]/h2")
                normal_lines = self.driver.find_elements_by_xpath("//*[@id=\"detail_page\"]/div[1]/div[3]/div[4]/p")
                texts = [x.text for x in [first_line] + normal_lines]
                text_str = clear_string(' '.join(texts))
            except Exception:
                text_str = ""

            print('Valid===={}'.format(url))
            key = str(int(hashlib.sha1(url.encode()).hexdigest(), 16) % 10 ** 8)
            doc = {"key": key,
                   "domain": self.domain,
                   "url": url,
                   "time": date_time,
                   "title": title_doc,
                   "content": text_str,
                   "status": 0}
            return self.mongo_client.save_doc("tich_hop_xu_ly_du_lieu", "covid_news_data", key, doc)
        
        except Exception:
            print('Error===={}'.format(url))
            traceback.print_exc()
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
