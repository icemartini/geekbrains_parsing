import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

s = Service('./chromedriver')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 ' \
             'Safari/537.36 '
options = Options()
options.add_argument('--headless')
options.add_argument('window-size=1600,900')
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(service=s, options=options)
url = "https://www.mvideo.ru/"

client = MongoClient('localhost', 27017)
mongo_base = client['mvideo_db']
collection = mongo_base['hits']


def wait_and_return(xpath, multiple=False):
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, 10).until(element_present)
        if multiple:
            return driver.find_elements(By.XPATH, xpath)
        return driver.find_element(By.XPATH, xpath)
    except TimeoutException:
        print("Timeout, shutting down")
        driver.quit()


def parse_product():
    images = wait_and_return('//button[@class="product-carousel__item-button"]/img', multiple=True)
    data = {'productId': wait_and_return('//span[@itemprop="sku"]').text,
            'productLink': driver.current_url,
            'productName': wait_and_return('//h1[@class="title"]').text,
            'productPrice': wait_and_return('//span[@class="price__main-value"]').text,
            'productImgs': ['https:' + re.sub('\s\d+w', '', image.get_attribute('srcset').split(', ')[-1]) for image in
                            images]}
    return data


driver.get(url)
urls = []
try:
    links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//h2[text()='Хиты продаж']/ancestor::mvid-simple-product"
                                                       "-collection//mvid-product-cards-group//div[@class='title']/a")))
    for link in links:
        urls.append(link.get_attribute('href'))
except TimeoutException:
    print("Loading took too much time!")
for url in urls:
    driver.get(url)
    collection.insert_one(parse_product())

driver.quit()
