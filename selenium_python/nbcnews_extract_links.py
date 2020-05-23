from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


options = Options()
# options.add_argument('--headless')

in_url = 'https://www.nbcnews.com/health/health-news/live-blog/2020-05-22-coronavirus-news-n1212671'

# driver = webdriver.Chrome(executable_path="chromedriver_linux64/chromedriver", options=options)
driver = webdriver.Chrome(executable_path="chromedriver_win32/chromedriver", options=options)

driver.implicitly_wait(10)

driver.get(in_url)
news_links = []
last_links_len = 0
while True:
    blogs = driver.find_element_by_xpath("//div[@class=\"cardsContainer\"]/div")
    if len(blogs) == last_links_len:
        break
    last_links_len = len(blogs)

    with open("nbc_covid_links.txt", "a") as f:
        for blog in blogs:
            url = ele.get_attribute("href")
            if url not in news_links:
                print(url)
                news_links.append(url)
                f.write(url + "\n")
    print("==================len {}".format(len(news_links)))
    element = driver.find_element_by_xpath("//footer/div[@class=\"button load-more js-load-more\"]/a")
    if element is not None:
        element.click()
        time.sleep(2)
    else:
        break

driver.close()
