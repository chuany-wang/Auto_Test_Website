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
import pytest
import subprocess
from config import *
import multiprocessing
from common.lo_logger import logger
from common.basic import RemoveReport
from common.init_test_data import init_data
from apis_check.api_check import run_checks
from common.init_dingding import send_report

current_os = sys.platform.lower()


def move_sqlData():
    try:
        # 执行前检查清除报告
        RemoveReport().run_rem_report()
        logger.info('清除之前的测试数据成功')
    except Exception as e:
        logger.error(f"清除历史数据失败{e}")


def report(envir):
    if envir == 'test':
        os.system(f'allure generate {JSON_DIR} -o {ALLURE_DIR} --clean')
        logger.info('测试报告生成完成')
        # 自动打开allure报告
        os.system(f'allure serve {JSON_DIR}  -p 12306')

    elif envir == "pro" or envir == 'dev':
        # 生成测试报告
        generate_cmd = f'/data/allure-2.13.7/bin/allure generate {JSON_DIR} -o {ALLURE_DIR} --clean'
        subprocess.run(generate_cmd, shell=True)
        logger.info(f'测试报告生成完成')


def run(process=10, mark=None, envir=None, site_host=None):
    # clean last test garbage
    move_sqlData()

    try:
        if not envir:
            envir = sys.argv[2]
            logger.info(f"当前运行环境为{envir}")

    except Exception as e:
        logger.error(f"获取当前环境参数出现异常{e}")

    # get new data into redis
    init_data(envir=envir, site_host=site_host)

    # run case
    if not mark:
        logger.info('运行所有用例开始！！！')
        pytest.main(['-n', f'{process}', '--alluredir', f'{JSON_DIR}'])

    elif mark:
        logger.info(f'运行手机端模块用例 {mark} 开始！！！')
        pytest.main(['-m', f'{mark}', '-n', f'{process}', '--alluredir', f'{JSON_DIR}'])

    # create report
    a = multiprocessing.Process(target=report(envir=envir))

    # send message with dingding
    b = multiprocessing.Process(target=send_report(envir=envir))

    a.start()
    time.sleep(15)
    b.start()


def api_run(envir=None, site_host=None):
    try:
        if not envir:
            envir = sys.argv[2]
        version_new = sys.argv[1]
    except IndexError:
        logger.error("缺少必要的命令行参数, 使用方式: python script.py <version> <environment>")
        return

    run_checks(version_new=version_new, envir=envir, site_host=site_host)


if __name__ == '__main__':

    if current_os == "linux":
        task_api_run = multiprocessing.Process(target=api_run)
        task_run = multiprocessing.Process(target=run)

    else:
        # task_api_run = multiprocessing.Process(target=api_run)
        task_run = multiprocessing.Process(
            target=run(process=1, mark='WishListPc', envir='test', site_host="https://www.kitneed.com/")
        )

    # task_api_run.start()
    task_run.start()
