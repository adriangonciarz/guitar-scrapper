from selenium.webdriver.common.by import By

from config import config
from scrappers.base import BaseScrapper


class KleinanzeigenScrapper(BaseScrapper):
    input_selector = (By.ID, 'site-search-query')
    result_container_selector = (By.CSS_SELECTOR, '.aditem-main--middle')
    title_selector = (By.CSS_SELECTOR, 'h2.text-module-begin > a')
    price_selector = (By.CSS_SELECTOR, 'p.aditem-main--middle--price')
    link_selector = title_selector
    cookies_accept_selector = (By.ID, 'gdpr-banner-accept')
    empty_results_selector = (By.CSS_SELECTOR, "div.outcomemessage-warning")
    wait_after_search = 3

    def __init__(self):
        super().__init__(config.kleinanziegen_basepath)
