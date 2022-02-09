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
        """метод проверяет по переданому селектору существует ли элемент на странице"""

        try:
            self.driver.find_element(*selector)
            exist = True

        except NoSuchElementException:
            exist = False

        return exist

    def auth(self):
        """Метод авторизации на сайте Инстаграм"""

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
        """Метод перехода на профиль пользователя"""

        self.driver.get(f'https://www.instagram.com/{user}/')

    def goto_tag(self, tag: str):
        """Метод перехода по тегу"""
        self.driver.get(f'https://www.instagram.com/explore/tags/{tag}/')

    def parce_posts_by_tag(self, tag: str):
        """Метод создания списка постов по тегу.
        Принимает тег, парсит 24+12*10 первых постов, записывает в файл."""

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
        """Метод создания списка уникальных пользователей из постов по тегу.
        Принимает тег, читает файл постов, парсит пользоваьелей, создает и записывает в файл
        список уникальных пользователей."""

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

        users_url = list(set(users_url))
        print(f'Количество уникальных пользователей {len(users_url)}')

        print(f'Сохранение в файл {tag}_users_url.txt')
        with open(f'files\\{tag}_users_url.txt', 'a') as text_file:
            for user in users_url:
                text_file.write(user + '\n')

    def parse_followers_users(self, user_name: str):
        """Метод создания списка уникальных подписчиков пользователя.
        Принимает имя пользователя, читает подписчиков, создает и записывает в файл список подписчиков."""

        try:
            self.driver.get(f'https://www.instagram.com/{user_name}/')
            sleep(randrange(4, 10))

            # создаём папку с именем пользователя
            if os.path.exists(f'files\\{user_name}'):
                print(f"Папка c пользователем {user_name} уже существует.")
            else:
                print(f"Создаём папку пользователя {user_name}.")
                os.mkdir(f'files\\{user_name}')

            if self.selector_exist(UserInsta.user_name):
                user_follower = self.driver.find_elements(*UserInsta.user_follow)[0].text.split()
                user_follower = int(''.join(user_follower))
                loops_count = int(user_follower / 12)

                print(f'Пользователь {user_name}: {user_follower} подписчиков, {loops_count} итераций.')
                sleep(randrange(2, 4))

                self.driver.find_elements(*UserInsta.user_follow)[0].click()
                followers_ul = self.driver.find_element(*UserInsta.followers_ul)

                followers_urls = []

                try:
                    for i in range(1, loops_count + 1):
                        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                        print(f'\r   Итерация # {i}. ', end='')
                        sleep(randrange(4, 7))
                        if i % 15 == 0:
                            self.delay_action(30)
                        if i % 30 == 0:
                            self.delay_action(40)

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
                    with open(f"files\\{user_name}\\{user_name}_followers.txt", "w") as text_file:
                        for link in followers_urls:
                            text_file.write(link + "\n")

                    print(f'Обработка подписчиков пользователя {user_name} завершена')

                    self.driver.find_element(*UserInsta.followers_close).click()

            else:
                print(f'Пользователь {user_name} не открывается')
        except Exception as ex:
            print(f'Вызвано исключение: {ex}')
            self.close_browser()

    def parse_followings_users(self, user_name: str):
        """Метод создания списка уникальных подписок пользователя.
        Принимает имя пользователя, читает подписки, создает и записывает в файл список подписок."""

        try:
            self.driver.get(f'https://www.instagram.com/{user_name}/')
            sleep(randrange(4, 10))

            # создаём папку с именем пользователя
            if os.path.exists(f'files\\{user_name}'):
                print(f"Папка c пользователем {user_name} уже существует.")
            else:
                print(f"Создаём папку пользователя {user_name}.")
                os.mkdir(f'files\\{user_name}')

            if self.selector_exist(UserInsta.user_name):
                user_following = self.driver.find_elements(*UserInsta.user_follow)[1].text.split()
                user_following = int(''.join(user_following))
                loops_count_following = int(user_following / 12)

                # Чтение подписок
                print(f'Пользователь {user_name}: {user_following} подписок, {loops_count_following} итераций.')
                sleep(randrange(2, 4))

                self.driver.find_elements(*UserInsta.user_follow)[1].click()
                followings_ul = self.driver.find_element(*UserInsta.followings_ul)

                followings_urls = []

                try:
                    for i in range(1, loops_count_following + 2):
                        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",
                                                   followings_ul)
                        print(f'\r   Итерация # {i}. ', end='')
                        sleep(randrange(4, 7))
                        if i % 15 == 0:
                            self.delay_action(30)
                        if i % 30 == 0:
                            self.delay_action(40)

                except Exception as ex:
                    print(f'Вызвано исключение: {ex}')

                finally:
                    print('Обрабатываем URL подписок')
                    all_followings_urls = followings_ul.find_elements(By.TAG_NAME, 'li')
                    for url in all_followings_urls:
                        url = url.find_element(By.TAG_NAME, 'a').get_attribute("href")
                        followings_urls.append(url)

                    print(
                        f'Сохраняем подписки пользователя {user_name} в файл "files\\{user_name}\\{user_name}_followings.txt"')
                    with open(f"files\\{user_name}\\{user_name}_followings.txt", "w") as text_file:
                        for link in followings_urls:
                            text_file.write(link + "\n")

                    print(f'Обработка подписок пользователя {user_name} завершена')

                    self.driver.find_element(*UserInsta.followers_close).click()

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
        """Метод подписки и лайков на посты подписчиков пользователя, полученного по посту тега.
        Принимает имя пользователя, читает файл с подписчиками, переходит на страницу каждого подписчика,
        подписывается и ставит лайки на первые 10 (или меньше) постов подписчика."""

        with open(f'files\\{user}\\{user}_followers.txt') as file:
            followers_url = file.readlines()

        print()
        print(f'Прочитано {len(followers_url)} ссылок на профили подписчиков пользователя {user}')

        subscribe_list = []
        for i, follower_url in enumerate(followers_url[133:134]):
            try:
                follower = follower_url.split('/')[-2]
                self.driver.get(follower_url)
                sleep(randrange(2, 5))
                print(f'Итерация # {i + 1}. Пользователь {follower}... ', end='')

                if (not self.selector_exist(PostInsta.wrong_userpage1)) or (
                        not self.selector_exist(PostInsta.wrong_userpage)):
                    self.driver.find_element(*MyProfile.edit_btn)

                    # Подписка на пользователя
                    status_selector = self.selector_exist(UserInsta.user_subscribe)
                    if not status_selector:
                        user_status_before = self.driver.find_element(*UserInsta.user_subscribe1).text
                        if user_status_before == 'Подписаться':
                            self.driver.find_element(*UserInsta.user_subscribe1).click()
                    else:
                        user_status_before = self.driver.find_element(*UserInsta.user_subscribe).text
                        if user_status_before == 'Подписаться':
                            self.driver.find_element(*UserInsta.user_subscribe).click()

                    sleep(randrange(1, 3))
                    user_status_after = self.driver.find_element(*UserInsta.user_subscribe).text
                    if user_status_before != user_status_after:
                        subscribe_list.append(follower_url)

                    if user_status_before == 'Подписаться' and user_status_after == 'Отправить сообщение':
                        print('Успешно подписались!')

                        self.delay_action(80)

                        # Лайк на посты
                        amount_posts = self.driver.find_element(*UserInsta.user_posts).text.split()
                        amount_posts = int(''.join(amount_posts))
                        print(f'  Всего постов у пользователя {follower} - {amount_posts}')

                        hrefs = self.driver.find_elements(By.TAG_NAME, 'a')
                        posts_url = [item.get_attribute('href') for item in hrefs if
                                     '/p/' in item.get_attribute('href')]
                        sleep(randrange(3, 5))

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

                    elif user_status_before == 'Подписаться' and user_status_after == 'Запрос отправлен':
                        print('Запросили подписку.')
                        sleep(randrange(1, 3))

                    elif user_status_before == 'Отправить сообщение':
                        print('Уже подписаны.')
                        sleep(randrange(1, 3))

                    elif user_status_before == 'Запрос отправлен':
                        print('Уже была запрошена подписка.')
                        sleep(randrange(1, 3))

                else:
                    print(f'Не удалось прочитать пользователя {follower}')

            except Exception as ex:
                print(f'Вызвано исключение: {ex}')

    def compare_followers_following_lists(self, user_name: str):
        """Метод сравнения списков подписчиков и подписок, получения списка не подписаных на нас пользователей.
        Принимает имя пользователя, читает подписчиков и подписки, создает и записывает в файл
        неподписанных пользователей."""

        print()
        if os.path.isfile(f'files\\{user_name}\\{user_name}_followers.txt') and os.path.isfile(
                f'files\\{user_name}\\{user_name}_followings.txt'):
            with open(f'files\\{user_name}\\{user_name}_followers.txt') as file:
                followers_url = file.readlines()
            print(f'Прочитано {len(followers_url)} ссылок на профили подписчиков пользователя {user_name}')

            with open(f'files\\{user_name}\\{user_name}_followings.txt') as file:
                followings_url = file.readlines()
            print(f'Прочитано {len(followings_url)} ссылок на профили подписок пользователя {user_name}')

            count = 0
            unfollow_list = []
            for user in followings_url:
                if user not in followers_url:
                    count += 1
                    unfollow_list.append(user)
            print(f"Необходимо отписаться от {count} пользователей")

            # сохраняем всех от кого нужно отписаться в файл
            with open(f"files\\{user_name}\\{user_name}_unfollow_list.txt", "w") as unfollow_file:
                for user in unfollow_list:
                    unfollow_file.write(user)
        else:
            print(f'Отсутствует файл {user_name}_followers.txt или {user_name}_followings.txt')

    # Modify method -> user_unsubscribe
    def smart_unsubscribe(self, user_name: str):

        print()
        if os.path.isfile(f'files\\{user_name}\\{user_name}_unfollow_list.txt'):
            with open(f'files\\{user_name}\\{user_name}_unfollow_list.txt') as file:
                unfollowers_url = file.readlines()
            print(f'Прочитано {len(unfollowers_url)} ссылок на профили для отписок.')

        for i, unfollower_url in enumerate(unfollowers_url[500:535]):
            try:
                unfollower = unfollower_url.split('/')[-2]
                self.driver.get(unfollower_url)
                sleep(randrange(4, 6))
                print(f'Итерация # {i + 1}. Пользователь {unfollower}... ', end='')

                if not self.selector_exist(PostInsta.wrong_userpage):
                    self.driver.find_element(*MyProfile.edit_btn)
                    # Отписка от пользователя
                    if self.selector_exist(UserInsta.user_send_message):
                        self.driver.find_element(*UserInsta.user_subscribe).click()
                        sleep(randrange(1, 2))
                        self.driver.find_element(*UserInsta.user_unsubscribe_confirm).click()
                        print('Успешно отписались!')

                        self.delay_action(90)

                    elif self.driver.find_element(*UserInsta.user_subscribe).text == 'Подписаться':
                        print('Уже отписались!')

                else:
                    print(f'Не удалось прочитать пользователя {unfollower}')

            except Exception as ex:
                print(f'Вызвано исключение: {ex}')
                # self.close_browser()

    def smart_unsubscribe_full(self, user_name: str):
        # Парсинг подписчиков пользователя
        self.parse_followers_users(user_name)
        # Парсинг подписок пользователя
        self.parse_followings_users(user_name)
        # Сравнение подписчиков и подписок и получение файла отписок
        self.compare_followers_following_lists(user_name)
        # Отписка от тех, кто не подписан на нас
        self.smart_unsubscribe(user_name)


instabot = InstaBot(kardon_login, kardon_passw)
try:
    instabot.auth()
    sleep(randrange(3, 5))
    # Чтение ссылок на посты по тегу
    # instabot.parce_posts_by_tag('СовместныеПокупкиХарьков')
    # Парсинг пользователей по постам в теге
    # instabot.parce_users_post_by_tag('СовместныеПокупкиХарьков')
    # Парсинг подписчиков пользователя тега
    # instabot.parse_follower_users('usa_shop_kharkov')
    # sleep(randrange(4, 6))
    # Подписки и лайки на посты подписчиков пользователя
    instabot.like_posts_and_follower('shopping.usa.brand')
    # Отписка от тех, кто не подписан на нас
    # instabot.smart_unsubscribe(kardon_login)
    instabot.goto_profile(kardon_login)
    sleep(randrange(3, 5))
    #
    instabot.exit_profile()
    sleep(randrange(3, 5))
except Exception as ex:
    print(f'Вызвано исключение: {ex}')
finally:
    instabot.close_browser()
