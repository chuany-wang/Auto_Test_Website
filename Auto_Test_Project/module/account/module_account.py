import string
import random
import time

from module.moduleCommon import ModuleCommon
from common.basic import basic_wait_for_element
from common.lo_logger import logger
from common.read_data import read_loc


def gen_name():
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for _ in range(4))
    return random_string


def gen_phone():
    # 生成随机的前三位
    first_three_digits = str(random.randint(100, 999))
    # 生成随机的后八位
    last_eight_digits = ''.join(random.choice('0123456789') for _ in range(8))
    # 拼接手机号码
    phone_number = f"1{first_three_digits}{last_eight_digits}"

    return phone_number


class Account(ModuleCommon):

    def __init__(self, driver, url, theme, host):
        super().__init__(driver, url, theme=theme, host=host)
        self.account_loc = read_loc(theme, "account_loc.yaml")

    def click_account(self):
        try:
            self.basic_js_click(**self.account_loc['my_account'])
            logger.debug(f"{self.host}首页点击个人中心")
        except Exception as e:
            logger.error(f"{self.host}首页点击个人中心出现异常{e}")

    """-----------------------------------------**** 谷歌登录功能****--------------------------------------------------"""

    def gmail_login(self):
        try:
            if self.theme == 'kte-m':
                self.basic_click(**self.account_loc['google_login'])
            else:
                soup = self.basic_beautiful_soup()
                social_login_container_divs = soup.find_all('div', class_='social-login-container')
                if len(social_login_container_divs) > 2:
                    self.basic_click(**self.account_loc['google_login'])
                else:
                    self.basic_click(**self.account_loc['google_login_bak'])
            logger.debug(f"{self.host}使用谷歌邮箱快捷登录")
        except Exception as e:
            logger.error(f"使用谷歌邮箱快捷登录出现异常{e}")

    def google_login_case(self):
        basic_wait_for_element(1)
        self.gmail_login()
        basic_wait_for_element(2)
