from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

by_dict = {
    'xpath': By.XPATH,
    'css': By.CSS_SELECTOR,
    'id': By.ID,
    'name': By.NAME,
    'tag': By.TAG_NAME,
    'class': By.CLASS_NAME,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
}

keys_mapping = {
    "space": Keys.SPACE,
    "enter": Keys.ENTER
}
