import logging
import threading

from config import search_terms
from scrappers.ebay_kleinanziegen import KleinanzeigenScrapper
from scrappers.olx import OLXScrapper
from scrappers.blocket import BlocketScrapper
from scrappers.markplaats import MarkplaatsScrapper
from scrappers.mercatino import MercatinoScrapper

scrapper_classes = [
    # OLXScrapper,
    BlocketScrapper,
    # MarkplaatsScrapper,
    # MercatinoScrapper,
    # KleinanzeigenScrapper
]
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


def perform_scrap(scrapper_class):
    scrapper = scrapper_class()
    scrapper.open_page()
    for term in search_terms():
        scrapper.search_and_scrap(term)
        print(scrapper.price_data)
    scrapper.dump_price_data_as_csv(f'{scrapper_class.__class__}.csv')
    scrapper.quit_page()


if __name__ == '__main__':
    threads = list()
    for scrapper_class in scrapper_classes:
        scrap_name = scrapper_class.__class__
        logging.info("Main    : create and start scrapper %s.", scrap_name)
        x = threading.Thread(target=perform_scrap, args=(scrapper_class,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining scrapper %s.", scrap_name)
        thread.join()
        logging.info("Main    : scrap %s done", scrap_name)
