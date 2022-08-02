from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from config import config
from scrappers.base import BaseScrapper


class MarktplaatsScrapper(BaseScrapper):
    no_results_text = 'Helaas heeft je zoekopdracht'
    input_selector = (By.CSS_SELECTOR, 'input[name="query"]')
    result_container_selector = (By.CSS_SELECTOR, 'li.mp-Listing--list-item:not([class*=mp-Listing--cas])')
    title_selector = (By.CSS_SELECTOR, 'h3.mp-Listing-title')
    price_selector = (By.CSS_SELECTOR, 'span.mp-text-price-label')
    link_selector = (By.CSS_SELECTOR, 'a.mp-Listing-coverLink')
    cookies_accept_selector = (By.ID, 'gdpr-consent-banner-accept-button')
    empty_results_selector = (By.XPATH, f'//div[contains(text(), "{no_results_text}")]')

    def __init__(self):
        super().__init__(config.marktplaats_basepath)

    def clear_input(self):
        input_element = self.driver.find_element(*self.input_selector)
        input_element.click()
        input_element.send_keys(Keys.COMMAND + 'A')
        input_element.send_keys(Keys.BACKSPACE)
