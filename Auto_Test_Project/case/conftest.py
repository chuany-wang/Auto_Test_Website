"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

import pytest
from common.init_driver import WebDriver
from common.init_redis import re_db


def get_params(key):
    result = re_db.get_list(key=key)
    return result


def process_url(site_host, test_type):
    """
    :param site_host: 站点域名
    :param test_type: 1001 商品详情页， 1002 登录页面, 1003 注册页面
    :return:
    """
    if test_type == 1001:
        # pay or cart, go to pro page
        keyword = re_db.get_list(site_host).get('keyword')
        url = site_host + 'product/' + keyword

    elif test_type == 1002:
        # like account, got to login page
        url = site_host + 'index.php?route=account/login'

    elif test_type == 1003:
        # like account, got to login page
        url = site_host + 'index.php?route=account/register'

    else:
        # others, go to home page
        url = site_host

    return url


@pytest.fixture(scope='session')
def goDriver_m():
    driver = WebDriver(terminal='ph').enable
    yield driver
    driver.quit()

@pytest.fixture(scope='session')
def goDriver():
    driver = WebDriver(terminal='pc').enable
    yield driver
    driver.quit()

@pytest.fixture(scope='module', params=get_params('common'))
def common_params(request):
    yield request.param




def check_fixture_value(key):
    res = get_params(key)
    return False if res else True
