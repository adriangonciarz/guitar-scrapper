from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from config import config
from scrappers.base import BaseScrapper


class OLXScrapper(BaseScrapper):
    input_selector = (By.ID, 'search')
    result_container_selector = (By.XPATH, '//div[@data-testid="listing-grid"]/div[@data-cy="l-card"]')
    title_selector = (By.CSS_SELECTOR, 'h6')
    price_selector = (By.XPATH, ".//p[@data-testid='ad-price']")
    link_selector = (By.CSS_SELECTOR, 'a')
    cookies_accept_selector = (By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')
    empty_results_selector = (By.XPATH, "//p[contains(text(), 'Nie znaleźliśmy żadnych wyników')]")
    clear_input_button_selector = (By.XPATH, '//button[@data-testid="clear-btn"]')

    def __init__(self):
        super().__init__(config.olx_basepath)

    def clear_input(self):
        try:
            self.driver.find_element(*self.clear_input_button_selector).click()
        except NoSuchElementException:
            super().clear_input()
