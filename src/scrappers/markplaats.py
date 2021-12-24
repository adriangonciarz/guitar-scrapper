from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config
from scrappers.base import BaseScrapper
from utils import PriceInfo


class MarkplaatsScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(config.markplaats_basepath)

    def search_for_term(self, query):
        search_input = self.driver.find_element(By.CSS, 'input[name="query"]')
        search_input.clear()
        search_input.send_keys(query + Keys.ENTER)

    def scrap_page(self) -> [PriceInfo]:
        item_containers = self.driver.find_elements(By.CSS_SELECTOR, 'li.mp-Listing--list-item')
        # sleep(2)
        for cont in item_containers:
            title_element = cont.find_element(By.CSS_SELECTOR, 'h3.mp-Listing-title')
            name = title_element.text
            link = con.find_element(By.CSS_SELECTOR, 'a.mp-Listing-coverLink').get_attribute('href')
            price = cont.find_element(By.CSS_SELECTOR, 'span.mp-text-price-label').text
            self.price_data.append(PriceInfo(name, price, link))
