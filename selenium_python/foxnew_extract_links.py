from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


options = Options()
options.add_argument('--headless')

in_url = 'https://www.foxnews.com/category/health/infectious-disease/coronavirus'

driver = webdriver.Chrome(executable_path="chromedriver_linux64/chromedriver", options=options)
driver.implicitly_wait(100)

driver.get(in_url)
news_links = []
last_links_len = 0
while True:
    elems = driver.find_elements_by_xpath("//section[@class=\"collection collection-article-list has-load-more\"]//article//header//a")
    if len(elems) == last_links_len:
        break
    last_links_len = len(elems)

    with open("foxnews_covid_links.txt", "a") as f:
        for ele in elems:
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
