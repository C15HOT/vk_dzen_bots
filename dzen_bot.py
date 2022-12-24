
import re
import time
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By

from random import random






class DzenParser:
    def __init__(self, login, password):
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-infobars')
        # self.chrome_options.add_argument('--remote-debugging-port=9222')
        # self.chrome_options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.login = login
        self.password = password
        self.link = 'https://dzen.ru'



    def get_recomends(self):
        self.driver.get(self.link)
        enter = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/header/div/div[2]/div[3]/button')
        enter.click()
        time.sleep(3)
        yandex_enter = self.driver.find_element(By.CSS_SELECTOR, '#tooltip-0-1 > div > div.login-content__yaButtonWrapper-15 > a')
        yandex_enter.click()
        time.sleep(3)
        login = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[2]/div/div[2]/span/input')
        time.sleep(3)
        login.send_keys(self.login)
        login_enter = self.driver.find_element(By.CSS_SELECTOR, '#passp\:sign-in')
        login_enter.click()
        time.sleep(3)
        password = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/form/div[2]/div[1]/span/input')
        password.send_keys(self.password)
        password_enter = self.driver.find_element(By.CSS_SELECTOR, '#passp\:sign-in')
        password_enter.click()
        time.sleep(3)



parser = DzenParser(login='leto2017a', password='gibsoncsv16xp')
parser.get_recomends()