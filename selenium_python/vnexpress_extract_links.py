from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


options = Options()
options.add_argument('--headless')

url_template = 'https://e.vnexpress.net/search/?q=covid+19&csrf=c5080081c84dd2cb2b0f4f362747d677'

driver = webdriver.Chrome(executable_path="chromedriver_linux64/chromedriver", chrome_options=options)

driver.get(url_template)
news_links = []
last_links_len = 0
while True:
    elems = driver.find_elements_by_class_name("title_news_site")
    if len(elems) == last_links_len:
        break
    last_links_len = len(elems)

    for ele in elems:
        url = ele.find_element_by_tag_name("a").get_attribute("href")
        if url not in news_links:
            print(url)
            news_links.append(url)

    element = driver.find_element_by_id("vnexpress_folder_load_more")
    if element is not None:
        element.click()
        time.sleep(2)
    else:
        break

with open("evnexpress_covid_links.txt", "w") as f:
    for url in news_links:
        f.write(url + "\n")

driver.close()
