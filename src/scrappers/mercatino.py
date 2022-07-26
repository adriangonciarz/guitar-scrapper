from selenium.webdriver.common.by import By

from config import config
from scrappers.base import BaseScrapper


class MercatinoScrapper(BaseScrapper):
    input_selector = (By.CSS_SELECTOR, "input[name='kw']")
    result_container_selector = (By.XPATH, ".//div[@class='item pri']")
    title_selector = (By.CSS_SELECTOR, 'div.ann > h3 > a')
    price_selector = (By.CSS_SELECTOR, 'div.inf > span.prz')
    link_selector = title_selector
    cookies_accept_selector = (By.XPATH, "//a[text()='ACCETTA']")
    empty_results_selector = (By.ID, 'search_notfound')
    url_id_pattern = '_id([0-9]+)'

    def __init__(self):
        super().__init__(config.mercatino_basepath)
