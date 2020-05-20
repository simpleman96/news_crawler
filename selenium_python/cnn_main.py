from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')

url_template = 'https://edition.cnn.com/world/live-news/coronavirus-pandemic-{}-intl/index.html'
date = '05-17-20'

driver = webdriver.Chrome(executable_path=r"driver/chromedriver", chrome_options=options)
driver.implicitly_wait(10)

driver.get(url_template.format(date))

# elems = driver.find_element_by_xpath("//header[@class=\"post-headlinestyles__Header-sc-2ts3cz-0 kpNfDn\"]//text()")
elems = driver.find_element_by_tag_name("body")
print(elems)

driver.close()