from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from config import config
from scrappers.base import BaseScrapper


class BlocketScrapper(BaseScrapper):
    input_selector = (By.CSS_SELECTOR, 'input.react-autosuggest__input')
    result_container_selector = (By.XPATH, ".//div[@data-cy='search-results']/div[contains(@class, 'styled__Wrapper')]")
    title_selector = (By.XPATH, ".//a[contains(@class, 'styled__StyledTitleLink')]")
    price_selector = (By.XPATH, ".//div[contains(@class, 'Price__StyledPrice')]")
    link_selector = title_selector
    cookies_accept_selector = (By.ID, 'accept-ufti')
    empty_results_selector = (By.XPATH, '//div[contains(@class, "EmptyState__Container")]')
    clear_input_button = (By.XPATH, '//button[contains(@class, "SearchInput__StyledClearButton")]')
    url_id_pattern = '\/([0-9]+)'

    def __init__(self):
        super().__init__(config.blocket_basepath)

    def clear_input(self):
        try:
            self.driver.find_element(*self.clear_input_button).click()
        except NoSuchElementException:
            pass
