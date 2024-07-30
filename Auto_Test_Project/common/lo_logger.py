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

# DATE = time.strftime("%Y-%m-%d", time.localtime(time.time()))
# log_path = os.path.join(LOG_DIR, f"{DATE}_all.log")
# flag = 0
# handler_id = 1
# file_log_handler_flag = 0
# allure_log_handler_flag = 0
#
#
# class AllureHandler(logging.Handler):
#     def emit(self, record):
#         logging.getLogger(record.name).handle(record)
#
#
# class MyLogger:
#     logger = uru_logger
#
#     # log level: TRACE < DEBUG < INFO < SUCCESS < WARNING < ERROR < CRITICAL
#     def __init__(self, log_file_path=log_path):
#         level = read_conf('CURRENCY').get('LEVEL')  # 读取配置
#         self.stdout_handler(level=level)
#         self.file_handler(level=level, log_file_path=log_file_path)
#         # 多线程不开启allure日志，日志会被打乱
#         self.allure_handler(level=level)
#
#     def stdout_handler(self, level):
#         """配置控制台输出日志"""
#         global flag
#         # 添加控制台输出的格式,sys.stdout为输出到屏幕;
#         if flag != 0:
#             return
#             # 清空所有设置
#         self.logger.remove()
#         h_id = self.logger.add(
#             sys.stdout,
#             level=level.upper(),
#             format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> "  # 颜色>时间
#                    "<m>[{thread.name}]</m>-"  # 进程名
#                    "<cyan>[{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
#                    ":<cyan>{line}]</cyan>-"  # 行号
#                    "<level>[{level}]</level>: "  # 等级
#                    "<level>{message}</level>",  # 日志内容
#         )
#         flag += 1
#         global handler_id
#         handler_id = h_id
#
#     def file_handler(self, level, log_file_path):
#         """配置日志文件"""
#         global file_log_handler_flag
#         # 控制只添加一个file_handler
#         if file_log_handler_flag == 0:
#             self.logger.add(
#                 log_file_path,
#                 level=level.upper(),
#                 format="{time:YYYY-MM-DD HH:mm:ss} "
#                        "[{thread.name}]-"
#                        "[{module}.{function}:{line}]-[{level}]:{message}",
#                 rotation="10 MB",
#                 encoding="utf-8",
#             )
#             file_log_handler_flag += 1
#
#     def allure_handler(self, level):
#         """日志输出到allure报告中"""
#         _format = "{time:YYYY-MM-DD HH:mm:ss} [{module}.{function}:{line}]-[{level}]:{message}"
#         self.logger.add(AllureHandler(), level=level.upper(), format=_format)
#
#     @classmethod
#     def change_level(cls, level):
#         """更改stdout_handler级别"""
#         # 清除stdout_handler配置
#         logger.remove(handler_id=handler_id)
#         # 重新载入配置
#         cls.logger.add(
#             sys.stdout,
#             level=level.upper(),
#             format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> "  # 颜色>时间
#                    "<m>[{process.name}]</m>-"  # 进程名
#                    "<m>[{thread.name}]</m>-"  # 进程名
#                    "<cyan>[{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
#                    ":<cyan>{line}]</cyan>-"  # 行号
#                    "<level>[{level}]</level>: "  # 等级
#                    "<level>{message}</level>",  # 日志内容
#         )
#
#
# _logger = MyLogger()
# logger = _logger.logger
