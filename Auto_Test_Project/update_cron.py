"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

import asyncio
import aiohttp
from common.lo_logger import logger
from common.init_sqlalchemy import db
from cron.site_theme import update_theme
from cron.site_api_key import update_api_key
from common.commom_api import retrieve_tokens
from models.site.site_key_info import SiteKey
from cron import update_quantity, update_func_status
from config.site_config import envir_to_filter_map_key
from cron.site_customer_address_info import update_address


async def corn_api(site_host=None, envir='all'):
    async with aiohttp.ClientSession() as session:
        if site_host:
            site_keys = db.query(SiteKey).filter(SiteKey.site_host == site_host).all()
        else:
            filter_condition_key = envir_to_filter_map_key.get(envir, lambda: SiteKey.site_id > 0)()

            site_keys = db.query(SiteKey).filter(filter_condition_key).all()

        tokens = await retrieve_tokens(session, site_keys)

        await update_theme(session, tokens)
        await update_func_status(session, tokens)


def corn_database():
    update_api_key()
    update_address()
    update_quantity()


if __name__ == '__main__':
    logger.info("执行定时任务开始.......")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(corn_api())
    corn_database()
    logger.info("执行定时任务结束........")
