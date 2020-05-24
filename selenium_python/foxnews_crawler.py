from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from datetime import datetime
import traceback
import hashlib


class FoxNewsCrawler(Thread):
    def __init__(self, output_dir):
        super().__init__()
        self.url_queue = []
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path="chromedriver_linux64/chromedriver", chrome_options=options)
        self.driver.implicitly_wait(30)
        self.output_dir = output_dir

    def add_url(self, url):
        self.url_queue.append(url)

    def run(self):
        try:
            while True:
                if len(self.url_queue) > 0:
                    print(f"Current urls queue size {len(self.url_queue)}")
                    status = self.parser_doc(self.url_queue[0])
                    if status:
                        self.url_queue.pop(0)
                else:
                    time.sleep(10)
        finally:
            print("Fox news crawler got exception, terminating ...")
            self.driver.close()

    def parser_doc(self, url):
        try:
            self.driver.get(url)
            date_time = self.driver.find_element_by_xpath("//div/time")
            date_time = clear_string(date_time.text)

            title_doc = self.driver.find_element_by_xpath("//main/article/header/h1")
            title_doc = clear_string(title_doc.text)

            normal_lines = self.driver.find_elements_by_xpath("//div[@class=\"article-body\"]/p")
            texts = [x.text for x in normal_lines]
            text_str = clear_string(' '.join(texts))

            output_path = self.output_dir + "/" + datetime.now().strftime("%Y%m%d") + ".txt"
            with open(output_path, 'a') as valid_f:
                with open(output_path + '_error', 'a') as error_f:
                    print('Valid===={}'.format(url))
                    key = str(int(hashlib.sha1(url.encode()).hexdigest(), 16) % 10 ** 8)
                    line = key \
                           + '|' + url \
                           + '|' + datetime.now().strftime("%Y%m%d_%H%M%S") + " - " + date_time \
                           + '|' + title_doc \
                           + '|' + text_str
                    valid_f.write(line + "\n")
            return True
        except Exception:
            print('Error===={}'.format(url))
            traceback.print_exc()
            error_f.write(url + "\n")
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
