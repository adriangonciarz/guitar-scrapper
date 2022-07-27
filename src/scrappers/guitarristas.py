from selenium.webdriver.common.by import By

from config import config
from scrappers.base import BaseScrapper


class GuitarristasScrapper(BaseScrapper):
    input_selector = (By.CSS_SELECTOR, 'div#search_container  input.query')
    result_container_selector = (By.CSS_SELECTOR, "div.msonic")
    title_selector = (By.CSS_SELECTOR, "h2.title a")
    price_selector = (By.CSS_SELECTOR, "div.price")
    link_selector = title_selector
    cookies_accept_selector = (By.XPATH, '//span[text()="ACEPTO"]')
    empty_results_selector = (By.XPATH, '//div[contains(text(), "No se produjeron resultados con las condiciones solicitadas.")]')


    def __init__(self):
        super().__init__(config.guitarristas_basepath)
