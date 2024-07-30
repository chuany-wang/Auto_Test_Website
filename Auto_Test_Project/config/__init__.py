"""
@Author:
@E-mail:
@Time:
@Explain: 封装公共方法
"""

import os

__all__ = ['BASE_DIR', 'STETTING_YAML_DIR', 'LOG_DIR', 'CASE_DIR', 'SCREENSHOT_DIR', 'ALLURE_DIR', 'REPORT_DATA_DIR',
           'JSON_DIR', 'CASE_YAML_DIR', 'IMG_DIR', 'LOCATOR_DIR']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

""" 配置目录 """
STETTING_YAML_DIR = os.path.join(BASE_DIR, "config", "setting.yaml")

""" 日志路径 """
LOG_DIR = os.path.join(BASE_DIR, "log")

""" 测试用例集路径 """
CASE_DIR = os.path.join(BASE_DIR, "case")

""" 元素定位数据 """
LOCATOR_DIR = os.path.join(BASE_DIR, "data", 'loc')

""" 用例Yaml文件 """
CASE_YAML_DIR = os.path.join(BASE_DIR, "data", 'caseYaml')

""" 截图目录 """
SCREENSHOT_DIR = os.path.join(BASE_DIR, "report", "report_screen")

""" 测试结果报告目录 """
ALLURE_DIR = os.path.join(BASE_DIR, "report", "report_allure")

""" 测试结果报告目录 """
REPORT_DATA_DIR = os.path.join(BASE_DIR, "report", "report_allure", "widgets", "summary.json")

"""测试用例结果目录 """
JSON_DIR = os.path.join(BASE_DIR, "report", "report_json")

"""测试图片路径 """
IMG_DIR = os.path.join(BASE_DIR, "data", "picture")
