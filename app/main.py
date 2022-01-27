import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import randrange
from user import *
from data import InstaUrl, ChromeDrUrl
from locators import *


class InstaBot():

    def __init__(self, username: str, passw: str):

        self.username = username
        self.passw = passw
        service = Service(ChromeDrUrl.webdriver_url)
        option = Options()
        # option.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
        option.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(service=service, options=option)
        self.driver.set_window_size(720, 960)
        self.driver.delete_all_cookies()
        self.driver.implicitly_wait(10)

    def close_browser(self):

        self.driver.close()
        self.driver.quit()

    def selector_exist(self, selector: tuple) -> bool:

        try:
            self.driver.find_element(*selector)
            exist = True

        except NoSuchElementException:
            exist = False

        return exist

    def auth(self):

        try:
            self.driver.get('https://www.instagram.com/')
            sleep(randrange(3, 5))

            input_username = self.driver.find_element(*AuthInsta.username)
            input_username.clear()
            input_username.send_keys(self.username)
            sleep(randrange(2, 4))

            input_passw = self.driver.find_element(*AuthInsta.passw)
            input_passw.clear()
            input_passw.send_keys(self.passw)
            sleep(randrange(2, 4))

            self.driver.find_element(*AuthInsta.submit).click()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(AuthInsta.save_enter_title))
            self.driver.find_element(*AuthInsta.save_not_now).click()
            sleep(randrange(1, 3))

            exist = self.selector_exist(AuthInsta.on_notifications_title)
            if exist:
                self.driver.find_element(*AuthInsta.notifications_not_now).click()
        except Exception as ex:
            print(f'Вызвано исключение: {ex}')
            self.close_browser()

    def goto_profile(self, user: str):

        self.driver.get(f'https://www.instagram.com/{user}/')

    def goto_tag(self, tag: str):

        self.driver.get(f'https://www.instagram.com/explore/tags/{tag}/')

    def parce_posts_by_tag(self, tag: str):

        self.driver.get(f'https://www.instagram.com/explore/tags/{tag}/')
        sleep(randrange(3, 5))

        amount_posts = self.driver.find_element(*TagsInsta.amount_posts).text.split()
        amount_posts = int(''.join(amount_posts))
        print()
        print(f'Всего постов по тегу {tag} - {amount_posts}')

        hrefs = self.driver.find_elements(By.TAG_NAME, 'a')
        posts_url = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
        sleep(randrange(4, 7))

        for i in range(0, 10):
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
            sleep(randrange(4, 7))
            hrefs = self.driver.find_elements(By.TAG_NAME, 'a')
            posts_url_part = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
            posts_url += posts_url_part

        print(f'Количество постов всего {len(posts_url)}')
        posts_url = list(set(posts_url))
        print(f'Количество уникальных постов {len(posts_url)}')

        print(f'Сохранение в файл {tag}_links.txt')
        with open(f'files\\{tag}_links.txt', 'a') as text_file:
            for link in posts_url:
                text_file.write(link + '\n')

    def parce_users_post_by_tag(self, tag: str):

        with open(f'files\\{tag}_links.txt') as file:
            urls_list = file.readlines()

            print()
            print(f'Прочитано ссылок на посты {len(urls_list)}')

            users_url = []
            for i, post_url in enumerate(urls_list[0:15]):
                try:
                    self.driver.get(post_url)
                    sleep(randrange(4, 6))
                    print(f'Итерация # {i + 1}... ', end='')

                    if self.selector_exist(PostInsta.user_name):
                        user_url = self.driver.find_element(*PostInsta.user_name).get_attribute('href')
                        user_name = user_url.split('/')[-2]
                        if user_name != f'{kardon_login}':
                            users_url.append(user_url)
                            print(f'Добавлен пользователь {user_name}')
                        else:
                            print(f'Пропущен пользователь {user_name}')
                    else:
                        print('Не удалось прочитать пользователя')

                except Exception as ex:
                    print(f'Вызвано исключение: {ex}')
                    self.close_browser()

        users_url = list(set(users_url))
        print(f'Количество уникальных пользователей {len(users_url)}')

        print(f'Сохранение в файл {tag}_users_url.txt')
        with open(f'files\\{tag}_users_url.txt', 'a') as text_file:
            for user in users_url:
                text_file.write(user + '\n')

    def parse_follower_users(self, user_url: str):

        try:
            self.driver.get(user_url)
            sleep(randrange(4, 10))

            user_name = user_url.split('/')[-2]

            # создаём папку с именем пользователя
            if os.path.exists(f'files\\{user_name}'):
                print(f"Папка c пользователем {user_name} уже существует!")
            else:
                print(f"Создаём папку пользователя {user_name}.")
                os.mkdir(f'files\\{user_name}')

            if self.selector_exist(UserInsta.user_name):
                user_follower = self.driver.find_elements(*UserInsta.user_follow)[0].text.split()
                user_follower = int(''.join(user_follower))
                loops_count = int(user_follower / 12)

                print(f'Пользователь {user_name}, подписчиков {user_follower}, итераций {loops_count}.')
                sleep(randrange(2, 4))

                self.driver.find_elements(*UserInsta.user_follow)[0].click()
                followers_ul = self.driver.find_element(*UserInsta.followers_ul)

                followers_urls = []

                try:
                    for i in range(1, loops_count + 1):
                        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                        print(f'\rИтерация # {i}. ', end='')
                        sleep(randrange(4, 7))
                        if i % 15 == 0:
                            rand = randrange(40, 60)
                            print(f'Засыпаем на {rand} сек.')
                            sleep(rand)
                        if i % 30 == 0:
                            rand = randrange(40, 60)
                            print(f'Засыпаем еще на {rand} сек.')
                            sleep(rand)

                except Exception as ex:
                    print(f'Вызвано исключение: {ex}')

                finally:
                    print('Обрабатываем URL подписчиков')
                    all_followers_urls = followers_ul.find_elements(By.TAG_NAME, 'li')
                    for url in all_followers_urls:
                        url = url.find_element(By.TAG_NAME, 'a').get_attribute("href")
                        followers_urls.append(url)

                    print(
                        f'Сохраняем подписчиков пользователя {user_name} в файл "files\\{user_name}\\{user_name}_followers.txt"')
                    with open(f"files\\{user_name}\\{user_name}_followers.txt", "a") as text_file:
                        for link in followers_urls:
                            text_file.write(link + "\n")

                    print(f'Обработка подписчиков пользователя {user_name} завершена')
            else:
                print(f'Пользователь {user_name} не открывается')
        except Exception as ex:
            print(f'Вызвано исключение: {ex}')
            self.close_browser()

    def exit_profile(self):
        self.driver.find_element(*MyProfile.edit_btn).click()
        sleep(randrange(1, 3))
        self.driver.find_element(*MyProfile.exit_btn).click()

    def delay_action(self, min: int):
        delay = randrange(min, min + 20)

        while delay:
            print(f'\rЗадержка {delay - 1} с.', end='')
            sleep(1)
            delay -= 1

        print('\r ', end='')

    def like_posts_and_follower(self, user: str):

        with open(f'files\\{user}\\{user}_followers.txt') as file:
            followers_url = file.readlines()

        print()
        print(f'Прочитано {len(followers_url)} ссылок на профили подписчиков пользователя {user}')

        subscribe_list = []
        for i, follower_url in enumerate(followers_url[21:41]):
            try:
                follower = follower_url.split('/')[-2]
                self.driver.get(follower_url)
                sleep(randrange(4, 6))
                print(f'Итерация # {i + 1}. Пользователь {follower}... ', end='')

                if not self.selector_exist(PostInsta.wrong_userpage):
                    self.driver.find_element(*MyProfile.edit_btn)
                    # Подписка на пользователя
                    if self.selector_exist(UserInsta.user_subscribe) and not self.selector_exist(
                            UserInsta.user_send_message):
                        self.driver.find_element(*UserInsta.user_subscribe).click()
                        subscribe_list.append(follower_url)
                        print('Успешно подписались!')

                        self.delay_action(80)

                        # Лайк на посты
                        amount_posts = self.driver.find_element(*UserInsta.user_posts).text.split()
                        amount_posts = int(''.join(amount_posts))
                        print(f'  Всего постов у пользователя {follower} - {amount_posts}')

                        hrefs = self.driver.find_elements(By.TAG_NAME, 'a')
                        posts_url = [item.get_attribute('href') for item in hrefs if
                                     '/p/' in item.get_attribute('href')]
                        sleep(randrange(4, 7))

                        # Чтение > 24 постов
                        # if amount_posts > 24:
                        #     amount_iter = (amount_posts - 24) // 12
                        #     for i in range(0, amount_iter):
                        #         # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        #         self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
                        #         sleep(randrange(4, 7))
                        #         hrefs = self.driver.find_elements(By.TAG_NAME, 'a')
                        #         posts_url_part = [item.get_attribute('href') for item in hrefs if
                        #                           '/p/' in item.get_attribute('href')]
                        #         posts_url += posts_url_part

                        posts_url = list(set(posts_url))
                        amount_parce_posts = len(posts_url)

                        if amount_parce_posts == 0:
                            print('   Переходим к следующему пользователю.')
                        else:
                            if amount_parce_posts < 10:
                                amount_like_posts = amount_parce_posts
                            else:
                                amount_like_posts = 10
                            print(
                                f'   Постов прочитано: {amount_parce_posts}. Ставим лайки на первые {amount_like_posts}.')

                        # print(f'Сохранение в файл {tag}_links.txt')
                        # with open(f'files\\{tag}_links.txt', 'a') as text_file:
                        #     for link in posts_url:
                        #         text_file.write(link + '\n')

                        print('\r ', end='')

                        for i, post_url in enumerate(posts_url[0:amount_like_posts]):
                            try:
                                self.driver.get(post_url)
                                sleep(randrange(4, 6))
                                if self.selector_exist(UserInsta.user_post_like):
                                    print(f'     Пост # {i + 1} - ставим лайк')
                                    self.driver.find_element(*UserInsta.user_post_like).click()
                                    self.delay_action(40)

                                else:
                                    print(f'   Пост # {i + 1} - уже есть лайк')
                            except Exception as ex:
                                print(f'Вызвано исключение: {ex}')
                                self.close_browser()

                    elif self.selector_exist(UserInsta.user_request_subscribe):
                        if self.selector_exist(UserInsta.user_send_message):
                            print('Уже подписаны.')
                        else:
                            status = self.driver.find_element(*UserInsta.user_request_subscribe).text
                            if status == 'Подписаться':
                                self.driver.find_element(*UserInsta.user_request_subscribe).click()
                                subscribe_list.append(follower_url)
                                print('Запросили подписку.')
                            elif status == 'Запрос отправлен':
                                print('Уже была запрошена подписка.')

                else:
                    print(f'Не удалось прочитать пользователя {follower}')

            except Exception as ex:
                print(f'Вызвано исключение: {ex}')
                self.close_browser()


instabot = InstaBot(kardon_login, kardon_passw)
try:
    instabot.auth()
    sleep(randrange(3, 5))
    # instabot.parce_posts_by_tag('СовместныеПокупкиХарьков')
    # instabot.parce_users_post_by_tag('СовместныеПокупкиХарьков')
    # instabot.parse_follower_users('https://instagram.com/usa_shop_kharkov/')
    # sleep(randrange(4, 6))
    instabot.like_posts_and_follower('usa_shop_kharkov')
    instabot.goto_profile(kardon_login)
    sleep(randrange(3, 5))
    instabot.exit_profile()
    sleep(randrange(3, 5))
except Exception as ex:
    print(f'Вызвано исключение: {ex}')
finally:
    instabot.close_browser()
