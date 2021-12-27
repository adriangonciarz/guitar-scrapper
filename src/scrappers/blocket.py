from selenium.webdriver.common.by import By

import config
from scrappers.base import BaseScrapper


class BlocketScrapper(BaseScrapper):
    input_selector = (By.CSS_SELECTOR, 'input.react-autosuggest__input')
    result_container_selector = (By.XPATH, './/div[@data-cy="search-results"]/div')
    title_selector = (By.XPATH, ".//a[contains(@class, 'styled__StyledTitleLink')]")
    price_selector = (By.XPATH, ".//div[contains(@class, 'Price__StyledPrice')]")
    link_selector = title_selector
    cookies_accept_selector = (By.ID, 'accept-ufti')

    def __init__(self):
        super().__init__(config.blocket_basepath)
