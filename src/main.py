import argparse
import concurrent.futures
import os

from config import config
from dbclient import DBClient
from models import BrandManager
from scrappers.blocket import BlocketScrapper
from scrappers.guitarristas import GuitarristasScrapper
from scrappers.kleinanziegen import KleinanzeigenScrapper
from scrappers.marktplaats import MarktplaatsScrapper
from scrappers.mercatino import MercatinoScrapper
from scrappers.olx import OLXScrapper
from scrappers.zikinf import ZikinfScrapper

page_scrappers_map = {
    'olx': OLXScrapper,
    'blocket': BlocketScrapper,
    'marktplaats': MarktplaatsScrapper,
    'mercatino': MercatinoScrapper,
    'kleinanziegen': KleinanzeigenScrapper,
    'zikinf': ZikinfScrapper,
    'guitarristas': GuitarristasScrapper,
}
supported_pages = ", ".join(page_scrappers_map.keys())


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
group.add_argument("-a", "--all", action='store_true', help="Flag to scrap all websites")
args = parser.parse_args()

brands_config_yaml_path = os.path.join(os.getcwd(), 'config', 'brands.yaml')
search_manager = BrandManager(brands_config_yaml_path)


def scrap_single_website(website_name):
    db_client = DBClient(config.DB_NAME)
    scrapper_class = page_scrappers_map[website_name]
    scrapper = scrapper_class()
    scrapper.open_page()
    for term in search_manager.get_search_terms():
        scrapper.search_and_scrap(term)
        db_client.insert_items(scrapper.items)
        scrapper.clear_items()
    scrapper.quit_page()


def scrap_all_websites():
    print('Scrapping all websites')
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.MAX_PARALLEL_SCRAPPERS) as executor:
        executor.map(scrap_single_website, page_scrappers_map.keys())


if __name__ == '__main__':
    db_client = DBClient(config.DB_NAME).create_items_table()
    if args.all:
        scrap_all_websites()
    else:
        scrap_single_website(args.website)
