from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')

url = 'https://e.vnexpress.net/search?q=covid-19&csrf=2577e02d43ef0d05b4d854dd7243251e'

driver = webdriver.Chrome(executable_path=r"driver/chromedriver", chrome_options=options)
driver.implicitly_wait(10)

driver.get(url)

WebElement element = driver.findElement(By.id("gbqfd"));
JavascriptExecutor executor = (JavascriptExecutor)driver;
executor.executeScript("arguments[0].click();", element);

# elems = driver.find_element_by_xpath("//header[@class=\"post-headlinestyles__Header-sc-2ts3cz-0 kpNfDn\"]//text()")
elems = driver.find_element_by_tag_name("body")
print(elems)

driver.close()