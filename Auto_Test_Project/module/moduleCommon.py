"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

from common.init_redis import re_db
from common.read_data import read_loc
from selenium.webdriver.common.by import By
from common.basic import Basic, logger, basic_wait_for_element


class ModuleCommon(Basic):

    def __init__(self, driver, url: str, theme: str, host: str):
        super().__init__(driver)
        self.url = url
        self.host = host
        self.theme = theme
        self.common_loc = read_loc(theme, "common_loc.yaml")

    def common_open_site(self):
        try:
            self.basic_cookie(way='delete')
            self.basic_open_site(self.url)
            logger.debug(f"打开网页 {self.url}")
            basic_wait_for_element(0.5)
        except Exception as e:
            logger.error(f"{self.url} 未正常打开网页{e}")




