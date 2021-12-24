from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import config
from utils import PriceInfo, sanitize_string


def prepare_driver() -> webdriver.Chrome:
    options = Options()
    options.headless = config.headless
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    # options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options)
    # driver.maximize_window()
    return driver


class BaseScrapper:
    def __init__(self, base_path):
        self.base_path = base_path
        self.driver = prepare_driver()
        self.price_data: [PriceInfo] = []

    def open_page(self):
        self.driver.get(self.base_path)

    def quit_page(self):
        self.driver.quit()

    def dump_price_data_as_csv(self, filename):
        s = '\n'.join(
            [f'{pi.brand};{pi.model};{sanitize_string(pi.name)};{pi.price};{pi.link}' for pi in self.price_data])
        with open(filename, 'w') as f:
            f.write(s)

    def search_and_scrap(self, query) -> [PriceInfo]:
        self.search_for_term(query)
        self.scrap_page()