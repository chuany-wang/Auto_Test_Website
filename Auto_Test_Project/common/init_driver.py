"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

import sys
from typing import TypeVar
from selenium import webdriver
from selenium.common import SessionNotCreatedException
from common.lo_logger import logger

sys.path.append('../')
T = TypeVar("T")


class WebDriver:
    """
    创建浏览器驱动，返回浏览器驱动
    """

    def __init__(self, terminal):
        self.terminal = terminal

    def browser_setup_args(self, driver: T) -> T:
        driver.maximize_window()
        return driver

    def _get_common_options(self) -> webdriver.ChromeOptions:
        """
        获取常用的 ChromeOptions 设置
        """
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-gpu')
        option.add_argument("--disable-cache")
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument("--disable-application-cache")
        option.add_argument("--disable-offline-load-stale-cache")
        option.add_argument("--blink-settings=imagesEnabled=false")
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_experimental_option("prefs", {"credentials_enable_service": False,
                                                 "profile.password_manager_enabled": False,
                                                 'profile.default_content_setting_values':
                                                     {
                                                         'notifications': 2
                                                     }
                                                 })
        option.page_load_strategy = 'eager'  # 指定加载策略

        return option

    def _get_linux_mobile_options(self) -> webdriver.ChromeOptions:
        """
        获取 Linux 操作系统移动终端的 ChromeOptions 设置
        """
        option = self._get_common_options()
        mobile_emulation = {"deviceName": "iPhone 6/7/8"}
        option.add_argument('--headless')
        option.add_experimental_option("mobileEmulation", mobile_emulation)
        return option

    def _get_linux_pc_options(self) -> webdriver.ChromeOptions:
        """
        获取 Linux 操作系统个人电脑终端的 ChromeOptions 设置
        """
        option = self._get_common_options()
        option.add_argument('--headless')
        return option

    def _get_win32_mobile_options(self) -> webdriver.ChromeOptions:
        """
        获取 Win32 操作系统移动终端的 ChromeOptions 设置
        """
        option = self._get_common_options()
        mobile_emulation = {"deviceName": "iPhone 6/7/8"}
        option.add_experimental_option("mobileEmulation", mobile_emulation)
        # option.add_argument('--headless')
        return option

    def _get_win32_pc_options(self) -> webdriver.ChromeOptions:
        """
        获取 Win32 操作系统个人电脑终端的 ChromeOptions 设置
        """
        option = self._get_common_options()
        # option.add_argument('--headless')
        return option

    def set_up(self) -> T:
        """
        创建浏览器驱动
        """
        try:
            current_sys = sys.platform.lower()
            options_mapping = {
                'linux': {
                    'ph': self._get_linux_mobile_options,
                    'pc': self._get_linux_pc_options
                },
                'win32': {
                    'ph': self._get_win32_mobile_options,
                    'pc': self._get_win32_pc_options
                }
            }

            options_func = options_mapping.get(current_sys, {}).get(self.terminal)
            if options_func:
                options = options_func()
                driver = webdriver.Chrome(options=options)
                return self.browser_setup_args(driver)
            else:
                logger.error(f'当前{current_sys}系统或终端类型不支持！')

        except SessionNotCreatedException:
            logger.warning('浏览器版本和当前驱动不匹配，请下载或者更新：https://npm.taobao.org/mirrors/chromedriver/')
            logger.error('浏览器版本和当前驱动不匹配，请下载或者更新：https://npm.taobao.org/mirrors/chromedriver/')

    @property
    def enable(self) -> T:
        return self.set_up()
