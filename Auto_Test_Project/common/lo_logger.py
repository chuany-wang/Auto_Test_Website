"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

import os
import sys
import time
import logging
from loguru import logger
from config import LOG_DIR
from common.read_data import read_conf
from loguru import logger as uru_logger


class LocalLogger:
    """
    日志设置类，使用logger 请从 logs 目录导入
    """

    DATE = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    LOG_PATH = os.path.join(LOG_DIR, f"{DATE}_all.log")
    ERR_LOG_PATH = os.path.join(LOG_DIR, f"{DATE}_err.log")
    logger.add(LOG_PATH, rotation="00:00", encoding='utf-8')
    logger.add(ERR_LOG_PATH, rotation="00:00", encoding='utf-8')
    logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
    levels = read_conf('CURRENCY').get('LEVEL')  # 读取配置
    handler_id = logger.add(sys.stderr, level=levels)
