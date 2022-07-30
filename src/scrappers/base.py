from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from config import config
from models import Item
from utils import sanitize_string_for_csv


def prepare_driver() -> webdriver.Chrome:
    options = Options()
    options.headless = config.headless
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.maximize_window()
    return driver


class BaseScrapper:
    input_selector = None
    result_container_selector = None
    title_selector = None
    price_selector = None
    link_selector = None
    cookies_accept_selector = None
    empty_results_selector = None
    wait_after_search = 1

    def __init__(self, base_path):
        self.base_path = base_path
        self.driver: WebDriver = None
        self.items: [Item] = []
        self.wait = WebDriverWait(self.driver, 10)
        self.ec = EC

    def __is_link_already_scrapped(self, item_link):
        for item in self.items:
            if item_link in item.link or item.link in item_link:
                return True
        return False

    def open_page(self):
        self.driver = prepare_driver()
        self.driver.get(self.base_path)
        if self.cookies_accept_selector:
            sleep(2)
            self.driver.find_element(*self.cookies_accept_selector).click()

    def add_item(self, item: Item):
        if not self.__is_link_already_scrapped(item.link):
            self.items.append(item)
        else:
            print(f'Item with link {item.link} already scrapped')

    def quit_page(self):
        self.driver.quit()

    def dump_items_data_as_csv(self, filename):
        s = '\n'.join(
            [f'{pi.brand};{pi.model};{sanitize_string_for_csv(pi.name)};{pi.price};{pi.currency};{pi.link}' for pi in
             self.items])
        with open(filename, 'w') as f:
            f.write(s)

    def search_and_scrap(self, query) -> [Item]:
        self.clear_input()
        self.search_for_term(query)
        if not self.is_results_empty():
            self.scrap_page()

    def clear_items(self):
        self.items = []

    def clear_input(self):
        search_input = self.driver.find_element(*self.input_selector)
        search_input.clear()

    def search_for_term(self, query):
        search_input = self.driver.find_element(*self.input_selector)
        search_input.send_keys(query + Keys.ENTER)
        sleep(self.wait_after_search)

    def parse_result_container(self, container: WebElement) -> Item:
        title_element = container.find_element(*self.title_selector)
        link_element = container.find_element(*self.link_selector)
        name = title_element.text
        link = link_element.get_attribute('href')
        price = self._get_container_price(container)
        return Item(name, price, link)

    def _get_container_price(self, container: WebElement):
        try:
            return container.find_element(*self.price_selector).text
        except:
            return ''

    def scrap_page(self) -> [Item]:
        item_containers = self.driver.find_elements(*self.result_container_selector)
        for cont in item_containers:
            item = self.parse_result_container(cont)
            self.add_item(item)
            print(f'Item {item.name} done')

    def is_results_empty(self):
        if self.empty_results_selector:
            try:
                self.driver.find_element(*self.empty_results_selector)
                return True
            except NoSuchElementException:
                return False
