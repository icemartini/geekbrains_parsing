from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

s = Service('./chromedriver')
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(service=s, options=options)
url = "https://account.mail.ru/login"
name = "gbselenium@bk.ru"
password = "!geekbrains"

client = MongoClient('localhost', 27017)
mongo_base = client['mail_db']
collection = mongo_base['mail.ru']


def login():
    WebDriverWait(driver, 10).until(EC.title_contains("Авторизация"))
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'username')))
    username.send_keys(name)
    username.send_keys(Keys.ENTER)
    pwd = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'password')))
    pwd.send_keys(password)
    pwd.send_keys(Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.title_contains("Входящие"))


def wait_and_return(xpath, multiple=False):
    try:
        element_clickable = EC.element_to_be_clickable((By.XPATH, xpath))
        WebDriverWait(driver, 10).until(element_clickable)
        if multiple:
            return driver.find_elements(By.XPATH, xpath)
        return driver.find_element(By.XPATH, xpath)
    except TimeoutException:
        print("Timeout, shutting down")
        driver.quit()


def parse_letter():
    letter = {'sender': wait_and_return("//div[@class='letter__author']/span").text,
              'email': wait_and_return("//div[@class='letter__author']/span").get_attribute('title'),
              'date': wait_and_return("//div[@class='letter__date']").text,
              'link': driver.current_url,
              'subject': wait_and_return("//h2[@class='thread__subject']").text,
              'content': wait_and_return("//div[@class='js-helper js-readmsg-msg']/div/div/div").text}
    return letter


driver.get(url)
try:
    login()
except:
    print('Cannot login')
    driver.quit()

urls = []
try:
    letters = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'js-letter-list-item')]")))
    for letter in letters:
        urls.append(letter.get_attribute('href'))
except TimeoutException:
    print("Loading took too much time!")
for url in urls:
    driver.get(url)
    collection.insert_one(parse_letter())

driver.quit()
