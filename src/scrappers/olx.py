from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import config
from scrappers.base import BaseScrapper
from utils import PriceInfo


class OLXScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(config.olx_basepath)

    def search_for_term(self, query):
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler').click()
        except:
            pass
        search_input = self.driver.find_element(By.ID, 'search-text')
        search_input.clear()
        search_input.send_keys(query + Keys.ENTER)
        sleep(3)

    def scrap_page(self) -> [PriceInfo]:
        try:
            # Check for empty results
            self.driver.find_element(By.CSS_SELECTOR, 'div.emptynew')
        except NoSuchElementException:
            item_containers = self.driver.find_elements(By.CSS_SELECTOR, 'div.offer-wrapper')
            for cont in item_containers:
                title_element = cont.find_element(By.CSS_SELECTOR, 'a[data-cy="listing-ad-title"]')
                name = title_element.text
                link = title_element.get_attribute('href')
                price = cont.find_element(By.CSS_SELECTOR, 'p.price').text
                self.price_data.append(PriceInfo(name, price, link))


