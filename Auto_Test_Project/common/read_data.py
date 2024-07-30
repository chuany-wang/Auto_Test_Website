"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""
import os
import yaml
from typing import TypeVar
from loguru import logger
from config import STETTING_YAML_DIR, LOCATOR_DIR

T = TypeVar('T')


def open_yaml(yaml_path: str, value=None):
    try:
        with open(yaml_path, encoding='utf-8') as f:
            data = yaml.load(f.read(), Loader=yaml.FullLoader)
            if value:
                for da in data:
                    if da.get(value):
                        return da.get(value)
            else:
                return data
    except Exception as E:
        logger.error(f"读取yaml文件异常{E}")


def read_conf(value: str) -> list or dict or str:
    conf = open_yaml(yaml_path=STETTING_YAML_DIR, value=value)
    return conf


def read_loc(theme, file_name) -> list or dict or str:
    try:
        loc_data = open_yaml(yaml_path=os.path.join(LOCATOR_DIR, theme, f"{file_name}"))
    except Exception as e:
        loc_data = ""
        logger.error(f"传入的测试环境不为PC或PH{e}")
    result = {k: v for item in loc_data for k, v in item.items()}
    return result
