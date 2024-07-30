"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

from sqlalchemy import and_
from models.site.site_key_info import SiteKey
from models.site.site_theme_info import SiteTheme
from models.site.site_database_info import SiteDatabase
from models.site.site_sku_quantity_info import SiteSkuQuantity
from models.site.site_customer_address_info import SiteCustomerAddInfo

envir_to_filter_map_theme = {
    "pro": lambda: SiteTheme.site_id >= 3000,
    "dev": lambda: and_(SiteTheme.site_id >= 2000, SiteTheme.site_id < 3000),
    "test": lambda: SiteTheme.site_id < 2000,
    "all": lambda: SiteKey.site_id > 0
}

envir_to_filter_map_product = {
    "pro": lambda: SiteSkuQuantity.site_id >= 3000,
    "dev": lambda: and_(SiteSkuQuantity.site_id >= 2000, SiteSkuQuantity.site_id < 3000),
    "test": lambda: SiteSkuQuantity.site_id < 2000,
    "all": lambda: SiteKey.site_id > 0
}
