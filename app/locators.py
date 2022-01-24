from selenium.webdriver.common.by import By


class AuthInsta:
    username = (By.CSS_SELECTOR, 'input[name="username"]')
    passw = (By.CSS_SELECTOR, 'input[name="password"]')
    submit = (By.CSS_SELECTOR, 'button[type="submit"]')

    save_enter_title = (By.CSS_SELECTOR, 'div.olLwo')
    save_not_now = (By.CSS_SELECTOR, 'div.cmbtv > button')

    on_notifications_title = (By.CSS_SELECTOR, 'div._08v79')
    notifications_on = (By.CSS_SELECTOR, 'div.mt3GC > button.aOOlW.bIiDR')
    notifications_not_now = (By.CSS_SELECTOR, 'div.mt3GC > button.aOOlW.HoLwm')


class ProfileInsta:
    amount_posts = (By.CSS_SELECTOR, 'li.LH36I > span._81NM2 > span')
    foll_foll = (By.CSS_SELECTOR, 'li.LH36I > a._81NM2 > span')
    posts = (By.CSS_SELECTOR, 'div.Nnq7C.weEfm > div > a')


class TagsInsta:
    amount_posts = (By.CSS_SELECTOR, 'span.g47SY')


class PostInsta:
    user_name = (By.CSS_SELECTOR, 'span > a')
    wrong_userpage = (By.CSS_SELECTOR, '#react-root > section > main > div > div > h2')



class UserInsta:
    user_name = (By.CSS_SELECTOR, 'div > h2')
    user_subscribe = (
        By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[2]/div/div/div/span/span[1]/button')
    user_send_message = (By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[2]/div/div/button/div')
    user_request_subscribe = (By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[2]/div/div/button')
    '//*[@id="react-root"]/section/main/div/header/section/div[2]/div/div/button'
    '//*[@id="react-root"]/section/main/div/header/section/div[2]/div/div/button'

    user_posts = (By.XPATH, '//*[@id="react-root"]/section/main/div/ul/li[1]/span/span')
    user_follow = (By.CSS_SELECTOR, 'ul > li > a > span')  # 2
    followers = (By.CSS_SELECTOR, 'li > div > div > div > div > span > a')
    followers_ul = (By.CSS_SELECTOR, 'body > div.RnEpo.Yx5HN > div > div > div.isgrP')

    user_post_like = (By.CSS_SELECTOR, 'button[type="button"] > div > span > svg')
    user_post_unlike = (By.XPATH,
    '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[3]/div/div/section[1]/span[1]/button/div/span/svg')


class MyProfile:
    profile = (By.CSS_SELECTOR, 'div.ctQZg.KtFt3 > div > div:nth-child(6) > span')
    edit_btn = (By.CSS_SELECTOR, 'div.VMs3J > button[type="button"]')
    exit_btn = (By.CSS_SELECTOR, 'div[role="dialog"] > div > div > div > button:nth-child(10)')
