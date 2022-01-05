import os
import zipfile
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import config
from utils import PriceInfo, sanitize_string


def prepare_driver() -> webdriver.Chrome:
    options = Options()
    options.headless = config.headless
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    if config.proxy_enabled:
        options.add_extension(config.plugin_path)
    # options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options)
    # driver.maximize_window()
    return driver


class BaseScrapper:
    input_selector = None
    result_container_selector = None
    title_selector = None
    price_selector = None
    link_selector = None
    cookies_accept_selector = None
    empty_results_selector = None

    def __init__(self, base_path):
        self.base_path = base_path
        self.driver = prepare_driver()
        self.price_data: [PriceInfo] = []

    def open_page(self):
        self.driver.get(self.base_path)
        if self.cookies_accept_selector:
            sleep(1)
            self.driver.find_element(*self.cookies_accept_selector).click()

    def quit_page(self):
        self.driver.quit()

    def dump_price_data_as_csv(self, filename):
        s = '\n'.join(
            [f'{pi.brand};{pi.model};{sanitize_string(pi.name)};{pi.price};{pi.currency};{pi.link}' for pi in
             self.price_data])
        with open(filename, 'w') as f:
            f.write(s)

    def search_and_scrap(self, query) -> [PriceInfo]:
        self.clear_input()
        self.search_for_term(query)
        if not self.is_results_empty():
            self.scrap_page()

    def clear_input(self):
        search_input = self.driver.find_element(*self.input_selector)
        search_input.clear()

    def search_for_term(self, query):
        search_input = self.driver.find_element(*self.input_selector)
        search_input.send_keys(query + Keys.ENTER)
        sleep(2)

    def scrap_page(self) -> [PriceInfo]:
        item_containers = self.driver.find_elements(*self.result_container_selector)
        for cont in item_containers:
            title_element = cont.find_element(*self.title_selector)
            link_element = cont.find_element(*self.link_selector)
            name = title_element.text
            link = link_element.get_attribute('href')
            price = cont.find_element(*self.price_selector).text
            self.price_data.append(PriceInfo(name, price, link))

    def is_results_empty(self):
        if self.empty_results_selector:
            try:
                self.driver.find_element(*self.empty_results_selector)
                return True
            except NoSuchElementException:
                return False
