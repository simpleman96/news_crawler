from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from evnexpress_crawler import EVnExpressCrawler

options = Options()
options.add_argument('--headless')

url_template = 'https://e.vnexpress.net/search/?q=covid-19&csrf=2bd5238aa590f617572961379ded9189'

driver = webdriver.Chrome(executable_path="chromedriver_linux64/chromedriver", chrome_options=options)
driver.implicitly_wait(100)

crawler = EVnExpressCrawler("e.vnexpress.net")
crawler.start()

driver.get(url_template)
news_links = []
while True:
    elems = driver.find_elements_by_class_name("title_news_site")

    for ele in elems:
        url = ele.find_element_by_tag_name("a").get_attribute("href")
        if url not in news_links:
            print(f"Got new url: {url}")
            news_links.append(url)
            crawler.add_url(url)

    print("==================len {}".format(len(news_links)))
    element = driver.find_element_by_id("vnexpress_folder_load_more")
    if element is not None:
        element.click()
        time.sleep(1)
    else:
        break

driver.close()
