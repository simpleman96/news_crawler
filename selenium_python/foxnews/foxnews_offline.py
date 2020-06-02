from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from foxnews_crawler import FoxNewsCrawler

in_url = 'https://www.foxnews.com/category/health/infectious-disease/coronavirus'
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path="chromedriver_linux64/chromedriver", chrome_options=options)
# driver = webdriver.Chrome(executable_path="chromedriver_win32/chromedriver", options=options)
driver.implicitly_wait(100)

crawler = FoxNewsCrawler("foxnews.com")
crawler.start()

driver.get(in_url)
news_links = []
while True:
    elems = driver.find_elements_by_xpath("//section[@class=\"collection collection-article-list has-load-more\"]//article//header//a")

    for ele in elems:
        url = ele.get_attribute("href")
        if url not in news_links and "video.foxnews" not in url:
            print(f"Got new url: {url}")
            news_links.append(url)
            crawler.add_url(url)

    print("==================len {}".format(len(news_links)))
    element = driver.find_element_by_xpath("//footer/div[@class=\"button load-more js-load-more\"]/a")
    if element is not None:
        element.click()
        time.sleep(30)
    else:
        break

driver.close()
