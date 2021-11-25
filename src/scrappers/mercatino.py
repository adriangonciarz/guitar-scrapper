from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config
from scrappers.base import BaseScrapper
from utils import PriceInfo


class MercatinoScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(config.mercatino_basepath)

    def search_for_term(self, query):
        search_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='kw']")
        search_input.clear()
        search_input.send_keys(query + Keys.ENTER)

    def scrap_page(self) -> [PriceInfo]:
        item_containers = self.driver.find_elements(By.XPATH, "//div[@class='item pri']")
        sleep(1)
        for cont in item_containers:
            title_element = cont.find_element(By.CSS_SELECTOR, 'div.ann > h3 > a')
            name = title_element.text
            link = title_element.get_attribute('href')
            price = cont.find_element(By.CSS_SELECTOR, 'div.inf > span.prz').text
            self.price_data.append(PriceInfo(name, price, link))

    def search_and_scrap(self, query) -> [PriceInfo]:
        self.search_for_term(query)
        self.scrap_page()
