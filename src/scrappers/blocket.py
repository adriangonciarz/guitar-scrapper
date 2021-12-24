from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config
from scrappers.base import BaseScrapper
from utils import PriceInfo


class BlocketScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(config.blocket_basepath)

    def search_for_term(self, query):
        search_input = self.driver.find_element(By.CSS_SELECTOR, 'input.react-autosuggest__input')
        search_input.clear()
        search_input.send_keys(query + Keys.ENTER)

    def scrap_page(self) -> [PriceInfo]:
        item_containers = self.driver.find_elements(By.XPATH, '//div[@data-cy="search-results"]/div')
        # sleep(2)
        for cont in item_containers:
            title_element = self.driver.find_element(By.CSS_SELECTOR, "//a[contains(@class, 'StyledTitleLink']")
            name = title_element.text
            link = title_element.get_attribute('href')
            price = cont.find_element(By.XPATH, "//div[contains(@class, 'Price__StyledPrice')]").text
            self.price_data.append(PriceInfo(name, price, link))
