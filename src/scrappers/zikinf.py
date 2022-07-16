from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import config
from scrappers.base import BaseScrapper


class ZikinfScrapper(BaseScrapper):
    input_selector = (By.ID, 'input_searchtext')
    result_container_selector = (By.CSS_SELECTOR, "table#searchResults tr")
    title_selector = (By.CSS_SELECTOR, "td.titre a span.lienVisible")
    price_selector = (By.CSS_SELECTOR, "td.titre a span.prix")
    link_selector = (By.CSS_SELECTOR, "td.titre a")
    # cookies_accept_selector = (By.ID, 'accept-ufti')
    empty_results_selector = (By.XPATH, '//strong[contains(text(), "Il n’y a pas d’annonce correspondant à votre recherche")]')
    clear_input_button = (By.XPATH, '//button[contains(@class, "SearchInput__StyledClearButton")]')
    url_id_pattern = '\/([0-9]+)'

    def __init__(self):
        super().__init__(config.zikinf_basepath)

    def clear_input(self):
        try:
            self.driver.find_element(*self.clear_input_button).click()
        except NoSuchElementException:
            pass
