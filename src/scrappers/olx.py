from selenium.webdriver.common.by import By

from config import config
from scrappers.base import BaseScrapper


class OLXScrapper(BaseScrapper):
    input_selector = (By.ID, 'search')
    result_container_selector = (By.XPATH, '//div[@data-testid="listing-grid"]/div[@data-cy="l-card"]')
    title_selector = (By.CSS_SELECTOR, 'a[data-cy="listing-ad-title"]')
    price_selector = (By.CSS_SELECTOR, 'p.price')
    link_selector = title_selector
    cookies_accept_selector = (By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')
    empty_results_selector = (By.XPATH, "//p[contains(text(), 'Nie znaleźliśmy żadnych wyników')]")

    def __init__(self):
        super().__init__(config.olx_basepath)
