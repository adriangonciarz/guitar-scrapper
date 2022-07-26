from selenium.webdriver.common.by import By

from config import config
from scrappers.base import BaseScrapper


class OLXScrapper(BaseScrapper):
    input_selector = (By.ID, 'search-text')
    result_container_selector = (By.CSS_SELECTOR, 'div.offer-wrapper')
    title_selector = (By.CSS_SELECTOR, 'a[data-cy="listing-ad-title"]')
    price_selector = (By.CSS_SELECTOR, 'p.price')
    link_selector = title_selector
    cookies_accept_selector = (By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')
    empty_results_selector = (By.XPATH, "//p[contains(text(), 'Nie znaleźliśmy ogłoszeń dla tego zapytania')]")
    url_id_pattern = '([a-zA-Z0-9+]+-[a-zA-Z0-9]+).html'

    def __init__(self):
        super().__init__(config.olx_basepath)
