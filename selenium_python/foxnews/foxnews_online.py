from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from foxnews_crawler import FoxNewsCrawler
import traceback

in_url = 'https://www.foxnews.com/category/health/infectious-disease/coronavirus'
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path="chromedriver_linux64/chromedriver", chrome_options=options)
# driver = webdriver.Chrome(executable_path="chromedriver_win32/chromedriver", options=options)
driver.implicitly_wait(20)

crawler = FoxNewsCrawler("foxnews.com")
crawler.start()

news_links = []
while True:
    try:
        driver.get(in_url)
        elems = driver.find_elements_by_xpath("//section[@class=\"collection collection-article-list has-load-more\"]//article//header//a")

        for ele in elems:
            url = ele.get_attribute("href")
            if url not in news_links and "video.foxnews" not in url:
                print(f"Got new url: {url}")
                news_links.append(url)
                crawler.add_url(url)
    except Exception:
        traceback.print_exc()
    finally:
        time.sleep(600)