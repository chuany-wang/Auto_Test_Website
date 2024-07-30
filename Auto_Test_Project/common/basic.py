"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

import os
import time
import json
import allure
import shutil
import urllib3
import requests
from loguru import logger
from typing import TypeVar
from bs4 import BeautifulSoup
from common.read_data import read_conf
from datetime import datetime, timedelta
from config.locate_config import by_dict, keys_mapping
from selenium.webdriver.common.by import By
from config import SCREENSHOT_DIR, JSON_DIR
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EM = TypeVar('EM')  # 可以是任何类型。


def basic_request(types: str, url: str, params: dict or list or str or None) -> object:
    """
    :param url:
    :param types:
    :param params:
    :return:
    """
    if types.lower() == 'get':
        urllib3.disable_warnings()
        response = requests.get(url, params, verify=False)
        return response

    elif types.lower() == 'post':
        urllib3.disable_warnings()
        response = requests.post(url, params, verify=False)
        return response


def format_current_datetime(date_style, duration_ms=None):
    """
    格式化当前日期时间

    Args:
        date_style (str): 日期时间格式，可选值有 'time', 'date', 'timestamp', 'plus_one', 'duration'
        duration_ms (int): 持续时间，单位毫秒

    Returns:
        str: 格式化后的日期时间
    """

    now = datetime.now()

    if date_style == 'time':
        return now.strftime('%Y_%m_%d')
    elif date_style == 'date':
        return now.strftime('%Y%m%d')
    elif date_style == 'timestamp':
        return str(int(time.time() * 1000))
    elif date_style == 'plus_one':
        return (now + timedelta(days=1)).timestamp() * 1000
    elif date_style == 'duration' and duration_ms:
        duration = timedelta(milliseconds=duration_ms)
        return f"{duration.seconds // 3600}:{duration.seconds % 3600 // 60:02d}:{duration.seconds % 60:02d}"
    else:
        return None


def basic_wait_for_element(sleep_time: float) -> float or int:
    if sleep_time:
        time.sleep(sleep_time)
    else:
        pass


class Basic:

    def __init__(self, driver):
        self.driver = driver

    # ------------------------------------------------- Page ----------------------------------------------------------
    def basic_open_site(self, url: str):
        self.driver.get(url)

    def basic_back(self):
        self.driver.back()

    def basic_refresh(self):
        self.driver.refresh()

    def basic_beautiful_soup(self):
        html_source = self.driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        return soup

    def basic_get_current_url(self):
        return self.driver.current_url

    def basic_get_all_windows(self):
        return self.driver.window_handles

    def basic_get_current_window(self):
        return self.driver.current_window_handle

    def basic_change_window(self):
        all_windows = self.basic_get_all_windows()
        curr_Window = self.basic_get_current_window()
        for handle in all_windows:
            if handle != curr_Window:
                self.driver.switch_to.window(handle)
        return curr_Window

    def basic_change_default_window(self, curr_Window):
        self.driver.switch_to.window(curr_Window)

    # -----------------------------------------------  Element  -------------------------------------------------------

    def basic_element(self, locate, wait_way, way, multiple, index):
        """
        等待元素直到指定的条件成立。

        :param locate: 元素的定位字符串
        :param wait_way: 等待条件 ('clickable', 'presence', 'visible')
        :param way: 定位方式 ('xpath', 'css', 'id', 'name', 'tag', 'class', 'link_text', 'partial_link_text')
        :param multiple: 是否查找多个元素，默认查找单个元素
        :param index: 指定返回第几个元素，默认返回第一个元素
        :return: 单个元素或元素列表
        """

        by = by_dict.get(way.lower())

        if not by:
            raise ValueError(f"不支持的定位方式: {way}")

        wait = WebDriverWait(self.driver, 10)
        condition = {
            'clickable': EC.element_to_be_clickable,
            'presence': EC.presence_of_all_elements_located if multiple else EC.presence_of_element_located,
            'visible': EC.visibility_of_all_elements_located if multiple else EC.visibility_of_element_located,
        }.get(wait_way)

        if not condition:
            raise ValueError(f"不支持的等待条件: {wait_way}")

        elements = wait.until(condition((by, locate)))

        if multiple:
            if not isinstance(elements, list):
                raise TypeError("返回的元素不是列表")
            if index >= len(elements):
                raise IndexError(f"索引 {index} 超出范围，元素个数为 {len(elements)}")
            return elements[index]

        return elements

    def basic_click(self, locate, way='xpath', wait_way='visible', multiple=False, index=0):
        self.basic_element(locate=locate, way=way, wait_way=wait_way, multiple=multiple, index=index).click()

    def basic_input(self, locate, text, way='xpath', wait_way='visible', multiple=False, index=0) -> None:
        self.basic_element(locate=locate, way=way, wait_way=wait_way, multiple=multiple, index=index).send_keys(text)

    def basic_send_keys(self, locate, keys, way='xpath', wait_way='visible', multiple=False, index=0):
        try:
            ele = self.basic_element(locate=locate, way=way, wait_way=wait_way, multiple=multiple, index=index)
            if not ele:
                logger.error(f"未能找到元素: {locate}")
                return

            key_to_send = keys_mapping.get(keys)
            ele.send_keys(key_to_send)

            logger.debug(f"向元素 {locate} 输入 {keys}")

        except Exception as e:
            logger.error(f"发送按键 {keys} 到元素 {locate} 时出现异常: {e}")

    def basic_switch_to_frame(self, locate, way='xpath', wait_way='visible', multiple=False, index=0):
        ele = self.basic_element(locate=locate, way=way, wait_way=wait_way, multiple=multiple, index=index)
        self.driver.switch_to.frame(ele)

    def basic_switch_to_default_frame(self):
        self.driver.switch_to.default_content()

    def basic_get_ele_text(self, locate, way='xpath', wait_way='visible', multiple=False, index=0) -> str:
        res = self.basic_element(locate=locate, way=way, wait_way=wait_way, multiple=multiple, index=index).text
        return res

    def basic_drag_drop(self, source, target, way='xpath', wait_way='visible', multiple=False, index=0):
        source_ele = self.basic_element(locate=source, way=way, wait_way=wait_way, multiple=multiple, index=index)
        target_ele = self.basic_element(locate=target, way=way, wait_way=wait_way, multiple=multiple, index=index)
        ActionChains(self.driver).drag_and_drop(source_ele, target_ele).perform()

    def basic_move_to_ele(self, locate, way='xpath', wait_way='visible', multiple=False, index=0):
        ele = self.basic_element(locate=locate, way=way, wait_way=wait_way, multiple=multiple, index=index)
        print(ele.get_attribute('class'))
        ActionChains(self.driver).move_to_element(ele).perform()

    def basic_select(self, locate, selectTypes, values, way='xpath', wait_way='visible', multiple=False, index=0):
        ele = self.basic_element(locate=locate, way=way, wait_way=wait_way, multiple=multiple, index=index)
        ele_select = Select(ele)

        select_method = getattr(ele_select, "select_by_" + selectTypes)
        select_method(values)

    def basic_alert(self):
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        return alert

    def basic_get_attribute(self, locate, tag='outerHTML', way='xpath', wait_way='visible', multiple=False, index=0):
        ele = self.basic_element(locate=locate, way=way, wait_way=wait_way, multiple=multiple, index=index)
        return ele.get_attribute(tag)

    def basic_shadow(self, shadow_locate):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, shadow_locate))
        )
        shadow_script = f'return arguments[0].shadowRoot'
        shadow = self.driver.execute_script(shadow_script, element)
        return shadow

    def basic_shadow_click(self, shadow_locate, locate, locate2=None):
        shadow = self.basic_shadow(shadow_locate)
        button = WebDriverWait(self.driver, 10).until(
            lambda d: shadow.find_element(By.CSS_SELECTOR, locate)
        )
        button.click()
        basic_wait_for_element(0.5)
        if locate2:
            button2 = WebDriverWait(self.driver, 10).until(
                lambda d: shadow.find_element(By.CSS_SELECTOR, locate2)
            )
            button2.click()

    # -------------------------------------------------Script---------------------------------------------------------

    def basic_script(self, script):
        res = self.driver.execute_script(script)
        return res

    def execute_script_with_ele(self, script, locate, way='xpath', wait_way='visible', multiple=False, index=0):
        elements = self.basic_element(locate=locate, way=way, wait_way=wait_way, multiple=multiple, index=index)
        if elements:
            if multiple:
                for element in elements:
                    self.driver.execute_script(script, element)
            else:
                self.driver.execute_script(script, elements)

    def basic_js_input(self, locate, text, way='xpath', wait_way='visible', multiple=False):
        js_script = f"arguments[0].value={json.dumps(text)}"
        self.execute_script_with_ele(js_script, locate, way, wait_way, multiple)

    def basic_js_click(self, locate, way='xpath', wait_way='visible', multiple=False):
        self.execute_script_with_ele("arguments[0].click()", locate, way, wait_way, multiple)

    def basic_js_clear(self, locate, way='xpath', wait_way='visible', multiple=False):
        logger.debug("js清空")
        self.execute_script_with_ele("arguments[0].value = '';", locate, way, wait_way, multiple)

    def basic_presence_element_with_script(self, id_text):
        js = f"document.getElementById(\"{id_text}\").style.display='block';"
        self.driver.execute_script(js)
        logger.debug(f"js脚本为 {js} ")

    def basic_script_to_scroll(self, locate, way='xpath', wait_way='visible', multiple=False, index=0):
        element = self.basic_element(locate=locate, way=way, wait_way=wait_way, multiple=multiple, index=index)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def reset_local_storage(self):
        current_timestamp = format_current_datetime('timestamp')
        # cookie权限
        js = f'window.localStorage.setItem("agree_use_cookie","{current_timestamp}")'
        self.driver.execute_script(js)
        # 订阅弹窗
        js = f'window.localStorage.setItem("user-show-sub-layer","{current_timestamp}")'
        self.driver.execute_script(js)

    # -------------------------------------------------  Other ---------------------------------------------------------


    def basic_screen_shot(self, name) -> str or None:
        currentTime = format_current_datetime(date_style="time")
        filename = name + "_" + currentTime + ".png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        logger.debug(f"截图成功已经存储在: {filepath}")
        return filepath

    def basic_attach_allure_report(self, module, title):
        filepath = self.basic_screen_shot(module)
        with open(filepath, mode='rb') as f:
            file = f.read()
        allure.attach(file, f'{title}', allure.attachment_type.PNG)


class RemoveReport:
    """
    删除已存在的报告
    """

    def mkdir(self, path: str) -> None:
        """
        当存储报告的文件夹不存在的时候，创建文件夹
        :param path:
        :return:
        """
        report_folder = os.path.exists(path)
        if not report_folder:
            os.mkdir(path)
        else:
            pass

    def clean_report(self, filepath: str) -> None:
        """
        :param filepath:历史报告所存储的路径
        :return:
        """
        rem_report_list = os.listdir(filepath)
        if rem_report_list:
            for f in rem_report_list:
                report_path = os.path.join(filepath, f)
                if f == '.gitignore' or f == '.gitkeep':
                    pass
                elif os.path.isfile(report_path):
                    if not report_path.endswith(".xml"):
                        os.remove(report_path)
                else:
                    os.path.isdir(report_path)
                    shutil.rmtree(report_path)

    def run_rem_report(self) -> None:
        """
        执行删除历史测试报告
        :return:
        """
        is_clean_report = read_conf('CURRENCY').get('IS_CLEAN_REPORT')
        if is_clean_report:
            dir_list = [JSON_DIR, SCREENSHOT_DIR]
            for _dir in dir_list:
                self.mkdir(_dir)
                self.clean_report(_dir)


class ErrorExcept(Exception):
    """
    自定义异常类
    """

    def __init__(self, message):
        super().__init__(message)
