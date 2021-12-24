from selenium.webdriver.common.by import By

import config
from scrappers.base import BaseScrapper


class MarkplaatsScrapper(BaseScrapper):
    input_selector = (By.CSS_SELECTOR, 'input[name="query"]')
    result_container_selector = (By.CSS_SELECTOR, 'li.mp-Listing--list-item')
    title_selector = (By.CSS_SELECTOR, 'h3.mp-Listing-title')
    price_selector = (By.CSS_SELECTOR, 'span.mp-text-price-label')
    link_selector = (By.CSS_SELECTOR, 'a.mp-Listing-coverLink')
    cookies_accept_selector = (By.ID, 'gdpr-consent-banner-accept-button')

    def __init__(self):
        super().__init__(config.markplaats_basepath)
