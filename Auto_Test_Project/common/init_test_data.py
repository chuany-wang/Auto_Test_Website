"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

from sqlalchemy import and_
from common.init_redis import re_db
from common.lo_logger import logger
from common.init_sqlalchemy import db
from models.site.site_status import SiteStatus
from models.site.site_func_info import SiteFunc
from models.site.site_theme_info import SiteTheme
from config.site_config import envir_to_filter_map_theme, envir_to_filter_map_product
from models.site.site_func_status import SiteFuncStatus
from models.site.site_sku_quantity_info import SiteSkuQuantity


def reset_data():
    res_flu = re_db.flush_all()
    if res_flu:
        logger.info("清除缓存测试数据成功")
    else:
        logger.error("清除缓存测试数据失败")


class InitData:

    def __init__(self, envir=None, site_host=None, func_name=None):
        self.envir = envir
        self.site_host = site_host
        self.func_name = func_name
        self.filter_condition_theme = envir_to_filter_map_theme.get(envir, lambda: SiteTheme.site_id < 2000)()
        self.filter_condition_product = envir_to_filter_map_product.get(envir, lambda: SiteSkuQuantity.site_id < 2000)()
        self.theme_list = self.get_theme()
        self.func_list = self.get_func()

    def get_theme(self):
        if self.site_host:
            host_theme = db.query(SiteTheme).join(SiteStatus, SiteTheme.site_id == SiteStatus.site_id).filter(and_(
                SiteTheme.site_host == self.site_host, SiteStatus.site_status == 1)).all()
        else:
            host_theme = db.query(SiteTheme).join(SiteStatus, SiteTheme.site_id == SiteStatus.site_id).filter(
                and_(self.filter_condition_theme, SiteStatus.site_status == 1)).all()

        theme_list = [{"site_host": theme.site_host, "pc_theme": theme.pc_theme,
                       "mobile_theme": theme.mobile_theme if theme.mobile_theme else 0} for theme in host_theme]

        return theme_list

    def get_func(self):
        if not self.func_name:
            func_list = [{'func_id': func.func_id, 'func_key': func.func_key} for func in db.query(SiteFunc).all()]
        else:
            func_list = [{'func_id': func.func_id, 'func_key': func.func_key} for func in
                         db.query(SiteFunc).filter_by(func_name=self.func_name).all()]
        return func_list

    def set_func_data(self):
        for f_id in self.func_list:
            func_id = f_id.get('func_id')
            func_key = f_id.get('func_key')
            list_host_match = []

            if str(func_id) == "8":
                res = re_db.set_list(key="common", value=self.theme_list, expiration=3600)
                if res:
                    logger.info("common相关数据写入缓存成功")
                else:
                    logger.error("common相关数据写入缓存失败")
            else:
                func_statu = db.query(SiteFuncStatus.site_host).filter(
                    and_(SiteFuncStatus.func_id == func_id, SiteFuncStatus.func_status == 1)).all()

                # 遍历状态为1的站点的host,取站点对应的主题，组成新的数组
                for fuc_sta in func_statu:
                    list_host_match.extend(
                        [the for the in self.theme_list if fuc_sta.site_host == the.get('site_host')])

                if list_host_match:
                    re_db.set_list(key=func_key, value=list_host_match, expiration=3600)
                    logger.info(f"{func_key}相关数据写入缓存成功")

                else:
                    logger.info(f"{func_key}无测试数据")

    def set_product_data(self):

        if self.site_host:
            sku_quan = db.query(SiteSkuQuantity).join(SiteStatus, SiteSkuQuantity.site_id == SiteStatus.site_id).filter(
                and_(SiteSkuQuantity.site_host == self.site_host, SiteStatus.site_status == 1)).all()
        else:
            sku_quan = db.query(SiteSkuQuantity).join(SiteStatus, SiteSkuQuantity.site_id == SiteStatus.site_id).filter(
                and_(self.filter_condition_product, SiteStatus.site_status == 1)).all()

        dict_sku_quan = {}

        for quan in sku_quan:
            dict_sku_quan[quan.site_host] = {'sku': quan.site_sku, 'keyword': quan.keyword}

        re_db.set_multiple(key_value_dict=dict_sku_quan, expiration=3600)

        logger.info(f"站点产品数据写入缓存成功")


def init_data(envir=None, site_host=None, func_name=None):
    reset_data()
    in_data = InitData(envir=envir, site_host=site_host, func_name=func_name)
    in_data.set_func_data()
    in_data.set_product_data()


if __name__ == '__main__':
    init_data(envir='pro')
