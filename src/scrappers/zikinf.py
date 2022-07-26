from selenium.webdriver.common.by import By

from config import config
from scrappers.base import BaseScrapper


class ZikinfScrapper(BaseScrapper):
    input_selector = (By.ID, 'input_searchtext')
    result_container_selector = (By.CSS_SELECTOR, "table#searchResults tr:not(.listeAnnoncesHeader)")
    title_selector = (By.CSS_SELECTOR, "td.titre a span.lienVisible")
    price_selector = (By.CSS_SELECTOR, "td.titre a span.prix")
    link_selector = (By.CSS_SELECTOR, "td.titre a")
    empty_results_selector = (By.XPATH, '//strong[contains(text(), "Il n’y a pas d’annonce correspondant à votre recherche")]')
    clear_input_button = (By.XPATH, '//button[contains(@class, "SearchInput__StyledClearButton")]')
    url_id_pattern = '\d+'

    def __init__(self):
        super().__init__(config.zikinf_basepath)
