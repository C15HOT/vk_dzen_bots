
import re
import time
from pprint import pprint
from typing import List

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

    def authorization(self):
        """
        Авторизация в Дзене
        :return:
        """
        self.driver.get(self.link)
        enter = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/header/div/div[2]/div[3]/button')
        enter.click()
        time.sleep(3)
        yandex_enter = self.driver.find_element(By.CSS_SELECTOR,
                                                '#tooltip-0-1 > div > div.login-content__yaButtonWrapper-15 > a')
        yandex_enter.click()
        time.sleep(3)
        mail = self.driver.find_element(By.XPATH,
                                        '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[1]/div[1]/button').click()
        login = self.driver.find_element(By.XPATH,
                                         '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[2]/div/div[2]/span/input')
        time.sleep(3)
        login.send_keys(self.login)
        login_enter = self.driver.find_element(By.CSS_SELECTOR, '#passp\:sign-in')
        login_enter.click()
        time.sleep(3)
        password = self.driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/form/div[2]/div[1]/span/input')
        password.send_keys(self.password)
        password_enter = self.driver.find_element(By.CSS_SELECTOR, '#passp\:sign-in')
        password_enter.click()
        time.sleep(3)


    def get_recomends(self, scroll_count=10):
        """
        Получение рекомендаций "Интересное в Дзене"
        :param scroll_count: Количество прокручиваний страницы
        :return: data
        """
        self.authorization()

        for _ in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        posts = self.driver.find_elements(By.CLASS_NAME, 'feed__row')
        interesting_posts = []
        for post in posts:
            records = post.find_elements(By.CLASS_NAME, 'card-rtb-label-view__part')
            for record in records:
                if 'интересное' in record.text:
                    interesting_posts.append(post)

        data = []

        for interesting_post in interesting_posts:
            post_data = {}
            post_author = interesting_post.find_element(By.CLASS_NAME, 'zen-ui-channel-info__title')
            post_data['author'] = post_author.text
            logo = interesting_post.find_element(By.CLASS_NAME, 'zen-ui-channel-info__logo-wrapper')
            link = logo.find_element(By.TAG_NAME, 'a')
            post_data['channel_link'] = link.get_attribute('href')

            try:
                likes = interesting_post.find_element(By.CLASS_NAME, 'zen-ui-button-like__text')
                post_data['likes_count'] = likes.text
            except:
                post_data['likes_count'] = None

            try:
                video_description = interesting_post.find_element(By.CLASS_NAME, 'card-layer-content-header-view__theme_white')
                post_data['video_description'] = video_description
                post_data['type'] = 'video'
            except:
                try:
                    title = interesting_post.find_element(By.CLASS_NAME, 'zen-ui-line-clamp')
                    post_data['title'] = title.text
                    description = interesting_post.find_element(By.CLASS_NAME, 'card-layer-snippet-view')
                    post_data['description'] = description.text
                    link = interesting_post.find_element(By.CLASS_NAME, 'card-image-compact-view__content').find_element(By.TAG_NAME, 'a').get_attribute('href')
                    post_data['post_link'] = link
                    post_data['type'] = 'short'
                except:
                    try:
                        interesting_post.find_element(By.CLASS_NAME, 'zen-ui-rich-text').click()
                        description = interesting_post.find_element(By.CLASS_NAME, 'zen-ui-rich-text__text')
                        post_data['description'] = description.text
                        text_divs = interesting_post.find_elements(By.CLASS_NAME, 'zen-ui-rich-text__p')
                        text = ''
                        for text_div in text_divs:
                            text += text_div.text
                        post_data['text'] = text
                        post_data['type'] = 'long'
                    except:
                        print('непонятный блок')
            data.append(post_data)

        for record in data:
            self.driver.get(record['channel_link'])

            subscribers_count = self.driver.find_element(By.CLASS_NAME, 'channel-counter__value-3W')
            record['subscribers_count'] = subscribers_count.text
            time.sleep(3)
            self.driver.find_element(By.CLASS_NAME, 'auto-height-transition-block').click()
            channel_description = self.driver.find_element(By.CLASS_NAME, 'zen-ui-rich-text__text')
            record['channel_description'] = channel_description.text

        return data

    def subscribe(self, channel_links: List):
        """
        Подписка на каналы
        :param channel_links: Список ссылок на каналы
        :return:
        """
        self.authorization()
        for link in channel_links:
            self.driver.get(link)
            button = self.driver.find_element(By.CLASS_NAME, 'desktop-channel-info-layout__mainButton-1w').click()
            time.sleep(2)

    def like_short_post(self, post_links: List):
        """
        Лайк коротких постов (которые имеют ссылки на статьи)
        :param post_links: Список ссылок на посты
        :return:
        """
        self.authorization()
        for link in post_links:
            self.driver.get(link)
            button = self.driver.find_element(By.CLASS_NAME, 'ui-lib-button-like__content').click()
            time.sleep(2)


    def enter_interest(self, interests: List[str]):
        """
        Подписка на интересы
        :param interests: Список строк-названий категорий (в сокращенном виде, например для раздела "Красота и мода" нужно писать просто "Красота"
        :return:
        """
        self.authorization()
        for _ in range(1):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        try:
            our_interests = self.driver.find_element(By.CLASS_NAME, 'interest-list-view__container-cx')
            our_interests.find_element(By.CLASS_NAME, 'button__button-14').click()


            svgs = self.driver.find_elements(By.CLASS_NAME, 'zen-ui-generic-svg')
            for svg in svgs:
                if '_is-selected' in svg.get_attribute('class'):
                    svg.click()

        except:
            pass


        recommendations = self.driver.find_element(By.CLASS_NAME, 'zen-ui-carousel-view__scroller')
        containers = recommendations.find_elements(By.CLASS_NAME, 'zen-ui-carousel-view__item-container')
        for container in containers:
            name = container.find_element(By.CLASS_NAME, 'interest-card-view__domain')
            for interest in interests:
                if interest in name.text:
                    name.click()
                    time.sleep(3)
        try:
            update = self.driver.find_element(By.CLASS_NAME, 'zen-ui-button2__text').click()
            time.sleep(3)
        except:
            pass


parser = DzenParser(login='leto2017a', password='gibsoncsv16xp')

# parser.enter_interest(['Кино', 'Юмор'])

data = parser.get_recomends()
pprint(data)
# channel_link = ['https://dzen.ru/rgo?lang=ru&country_code=ru&parent_rid=1697862782.96.1671896696738.45223&from_parent_id=-740625132394824576&from_parent_type=native&from_page=other_page']
# parser.subscribe(channel_links=channel_link)
#
# post_link = ['https://dzen.ru/a/YzFA0uETSgUpwRBB']
# parser.like_short_post(post_link)