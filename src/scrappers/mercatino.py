from selenium.webdriver.common.by import By

import config
from scrappers.base import BaseScrapper


class MercatinoScrapper(BaseScrapper):
    input_selector = (By.CSS_SELECTOR, "input[name='kw']")
    result_container_selector = (By.XPATH, "//div[@class='item pri']")
    title_selector = (By.CSS_SELECTOR, 'div.ann > h3 > a')
    price_selector = (By.CSS_SELECTOR, 'div.inf > span.prz')
    link_selector = title_selector

    def __init__(self):
        super().__init__(config.mercatino_basepath)
