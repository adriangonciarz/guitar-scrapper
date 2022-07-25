import os
from typing import Optional

import yaml

from models import Brand, Model
from utils import check_if_result_matches_substring

olx_basepath = 'https://www.olx.pl/muzyka-edukacja/instrumenty/'
kleinanziegen_basepath = 'https://www.ebay-kleinanzeigen.de/s-musikinstrumente/c74'
mercatino_basepath = 'https://www.mercatinomusicale.com/'
blocket_basepath = 'https://www.blocket.se/annonser/hela_sverige/fritid_hobby/musikutrustning/gitarr_bas_forstarkare?cg=6161'
marktplaats_basepath = 'https://www.marktplaats.nl/l/muziek-en-instrumenten/snaarinstrumenten-gitaren-elektrisch/'
zikinf_basepath = 'https://www.zikinf.com/annonces/liste.php?rub=9'

headless = False
MAX_PARALLEL_SCRAPPERS = 3
DB_HOST = os.getenv('DBHOST')
DB_PORT = os.getenv('DBPORT', 3306)
DB_USER = os.getenv('DBUSER')
DB_PASSWORD = os.getenv('DBPASSWORD')
DB_NAME = 'scrapper'

brands_config_filepath = os.path.join(os.getcwd(), 'brands.yaml')

currency_map = {
    'PLN': ('zł', 'PLN'),
    'EUR': ('€', 'EUR'),
    'SEK': ('SEK', 'kr')
}


class BrandManager:
    def __init__(self, config_path=brands_config_filepath):
        self.brands: [Brand] = []

        with open(config_path) as file:
            brands_config = yaml.load(file, Loader=yaml.FullLoader)
            for brand in brands_config:
                models = [Model(m['name'], m['search'], m['aliases']) for m in brand['models']]
                self.brands.append(Brand(brand['brand'], models, brand['brand_aliases']))

    def get_brand_names(self):
        return [b.name for b in self.brands]

    def get_search_terms(self):
        terms = []
        for brand in self.brands:
            for model in brand.models:
                if model.search:
                    terms.append(f'{brand.name} {model.name}'.lower())
        return terms

    def get_brand_by_name(self, brand_name: str) -> Brand:
        return next(b for b in self.brands if b.name == brand_name)

    def find_matching_brand(self, search_string) -> Optional[str]:
        for brand in self.brands:
            for brand_alias in brand.get_possible_aliases():
                if check_if_result_matches_substring(search_string, brand_alias):
                    return brand.name

    def find_matching_model(self, brand_name, search_string) -> Optional[str]:
        brand = self.get_brand_by_name(brand_name)
        for model in brand.models:
            for model_alias in model.get_possible_aliases():
                if check_if_result_matches_substring(search_string, model_alias):
                    return model.name
