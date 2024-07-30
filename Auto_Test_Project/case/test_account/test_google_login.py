"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""
import pytest
import allure
from common.lo_logger import logger
from case.conftest import process_url, check_fixture_value
from module.account.module_account import Account


@allure.feature('个人中心用例')
class TestGoogleLogin:

    @pytest.mark.GoogleLoginPh
    @allure.story('手机端使用谷歌邮箱快捷登录')
    @pytest.mark.skipif(condition=check_fixture_value('module_social_login_google_status'),
                        reason="站点未开启 oceanPay支付方式")
    def test_google_login_ph(self, google_params, goDriver_m):
        host = google_params.get('site_host')
        url = process_url(site_host=host, test_type=1002)
        mobile_theme = google_params.get('mobile_theme')

        if mobile_theme == "kte-m":
            obj = Account(goDriver_m, url, theme=mobile_theme, host=host)
            logger.info(f"正在测试站点 {host} 的手机端谷歌邮箱快捷登录功能")

            # 1. see the title
            obj.common_open_site()

            # 2. login with google
            obj.google_login_case()

            # 3. assert
            assert_res = obj.common_assert_url()
            if 'authError' in assert_res or 'google.com' not in assert_res:
                obj.allure_report(module="谷歌邮箱快捷登录", title=f"{host}的谷歌邮箱快捷登录")

            pytest.assume('authError' not in assert_res)
            pytest.assume('google.com' in assert_res)

        else:
            logger.info(f"站点{host} 未开启手机端，不执行测试")

    @pytest.mark.GoogleLoginPc
    @allure.story('PC端使用谷歌邮箱快捷登录')
    @pytest.mark.skipif(condition=check_fixture_value('module_social_login_google_status'),
                        reason="站点未开启 谷歌快捷登录")
    def test_google_login_pc(self, google_params, goDriver):
        host = google_params.get('site_host')
        url = process_url(site_host=host, test_type=1002)
        pc_theme = google_params.get('pc_theme')

        if pc_theme == "kte":
            obj = Account(goDriver, url, theme=pc_theme, host=host)
            logger.info(f"正在测试站点 {host} 的PC端谷歌邮箱快捷登录功能")

            # 1. see the title
            obj.common_open_site()

            # 2. login with google
            obj.google_login_case()

            # 3. assert
            assert_res = obj.common_assert_url()
            if 'authError' in assert_res or 'google.com' not in assert_res:
                obj.allure_report(module="谷歌邮箱快捷登录", title=f"{host}的谷歌邮箱快捷登录")

            pytest.assume('authError' not in assert_res)
            pytest.assume('google.com' in assert_res)

        else:
            logger.info(f"站点{host} 未开启手机端，不执行测试")
