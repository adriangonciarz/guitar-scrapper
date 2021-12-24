from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config
from scrappers.base import BaseScrapper
from utils import PriceInfo


class KleinanzeigenScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(config.kleinanziegen_basepath)

    def search_for_term(self, query):
        search_input = self.driver.find_element(By.ID, 'site-search-query')
        search_input.clear()
        search_input.send_keys(query + Keys.ENTER)

    def scrap_page(self) -> [PriceInfo]:
        item_containers = self.driver.find_elements(By.CSS_SELECTOR, '.aditem-main--middle')
        sleep(3)
        for cont in item_containers:
            title_element = cont.find_element(By.CSS_SELECTOR, 'h2.text-module-begin > a')
            name = title_element.text
            link = title_element.get_attribute('href')
            price = cont.find_element(By.CSS_SELECTOR, 'p.aditem-main--middle--price').text
            self.price_data.append(PriceInfo(name, price, link))

