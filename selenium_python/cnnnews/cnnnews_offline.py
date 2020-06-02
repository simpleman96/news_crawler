from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import hashlib
from datetime import datetime
from datetime import timedelta
import re
from selenium_python.cnnnews.mongo_utils import MongoUtils


def main():
    url_template = 'https://edition.cnn.com/world/live-news/coronavirus-pandemic-{}-intl/index.html'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="../chromedriver_linux64/chromedriver", chrome_options=options)
    # driver = webdriver.Chrome(executable_path="chromedriver_win32/chromedriver", options=options)
    driver.implicitly_wait(100)

    mongo_client = MongoUtils()

    run_time = datetime.strptime("2020-04-17", "%Y-%m-%d")
    begin_time = datetime.strptime("2020-01-01", "%Y-%m-%d")
    news_links = []
    last_height = 0
    while run_time > begin_time:
        in_url = url_template.format(run_time.strftime("%m-%d-%y"))
        print(f"==============Crawling for url {in_url}")
        driver.get(in_url)
        while True:
            blogs = driver.find_elements_by_xpath("//article[@class=\"sc-cJSrbW poststyles__PostBox-sc-1egoi1-0 tzojb\"]")

            for blog in blogs:
                title = blog.find_element_by_xpath("header/h2").text
                key = str(int(hashlib.sha1(title.encode()).hexdigest(), 16) % 10 ** 8)
                if key not in news_links:
                    print(f"Got new blog: {title}")
                    news_links.append(key)
                    if save_doc(mongo_client, blog):
                        print(f"Save blog: {key} : {title} success!")
                    else:
                        print(f"Blog: {key} : {title} already saved!")

            print("==================len {}".format(len(news_links)))

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            new_height = driver.execute_script("return document.body.scrollHeight")
            time.sleep(10)
            if new_height == last_height:
                break

            last_height = new_height
            
        run_time = run_time - timedelta(days=1)
    driver.close()


def save_doc(mongo_client, blog):
    title = blog.find_element_by_xpath("header/h2").text
    key = str(int(hashlib.sha1(title.encode()).hexdigest(), 16) % 10 ** 8)

    try:
        date_time = blog.find_element_by_xpath("header/span")
        date_time = clear_string(date_time.text)
    except Exception:
        date_time = ""

    try:
        title_doc = clear_string(title)
    except Exception:
        title_doc = ""

    try:
        normal_lines = blog.find_elements_by_xpath("div/p")
        texts = [x.text for x in normal_lines]
        text_str = clear_string(' '.join(texts))
    except Exception:
        text_str = ""

    print('Valid===={}'.format(title))
    doc = {"key": key,
           "domain": "cnn.com",
           "url": "",
           "time": date_time,
           "title": title_doc,
           "content": text_str,
           "status": 0}
    return mongo_client.save_doc("tich_hop_xu_ly_du_lieu", "covid_news_data", key, doc)

def clear_string(x):
    try:
        x = re.sub('\n', ' ', x)
        x = re.sub('\r', ' ', x)
        x = re.sub('\t', ' ', x)
        x = re.sub('\|', ' ', x)
    except:
        x = "__clean_error__"
    return ' '.join(x.split())


if __name__ == '__main__':
    main()