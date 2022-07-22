import argparse
import concurrent.futures
import logging

import config
from config import search_terms
from dbclient import DBClient
from scrappers.blocket import BlocketScrapper
from scrappers.ebay_kleinanziegen import KleinanzeigenScrapper
from scrappers.marktplaats import MarktplaatsScrapper
from scrappers.mercatino import MercatinoScrapper
from scrappers.olx import OLXScrapper
from scrappers.zikinf import ZikinfScrapper

MAX_PARALLEL_SCRAPPERS = 3

page_scrappers_map = {
    'olx': OLXScrapper,
    'blocket': BlocketScrapper,
    'markplaats': MarktplaatsScrapper,
    'mercatino': MercatinoScrapper,
    'kleinanziegen': KleinanzeigenScrapper,
    'zikinf': ZikinfScrapper
}
supported_pages = ", ".join(page_scrappers_map.keys())

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


class MissingPageException(Exception):
    pass


class UnknownScrapperException(Exception):
    pass


class SingleScrapAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values not in page_scrappers_map:
            raise UnknownScrapperException(f'Unknown page key: {values}, allowed keys: {supported_pages}')
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-w", "--website", action=SingleScrapAction, help="Key of the website to scrap")
group.add_argument("--all", action='store_true', help="Flag to scrap all websites")
args = parser.parse_args()


def scrap_single_website(website_name):
    scrapper_class = page_scrappers_map[website_name]
    scrapper = scrapper_class()
    scrapper.open_page()
    for term in search_terms():
        scrapper.search_and_scrap(term)
    scrapper.dump_items_data_as_csv(f'{scrapper_class.__name__}.csv')
    db_client = DBClient(f'{scrapper_class.__name__}.db')
    db_client.create_items_table()
    db_client.insert_items(scrapper.items)
    scrapper.quit_page()


def scrap_all_websites():
    print('Scrapping all websites')
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL_SCRAPPERS) as executor:
        executor.map(scrap_single_website, page_scrappers_map.keys())


if __name__ == '__main__':
    if args.all:
        scrap_all_websites()
    else:
        scrap_single_website(args.website)
    # create_proxyauth_extension(config.proxy_server, config.proxy_port, config.proxy_user, config.proxy_password)
