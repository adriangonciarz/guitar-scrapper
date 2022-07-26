import dataclasses
import re
from typing import Optional

import yaml

from config.config import brands_config_filepath
from utils import check_if_result_matches_substring


@dataclasses.dataclass
class Model:
    name: str
    search: bool
    aliases: [str]

    def get_possible_aliases(self) -> [str]:
        return [*self.aliases, self.name]


@dataclasses.dataclass
class Brand:
    name: str
    models: [Model]
    aliases: [str]

    def get_possible_aliases(self) -> [str]:
        return [*self.aliases, self.name]


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


class Item:
    brand_manager = BrandManager()

    def __init__(self, name: str, price_string: str, link: str):
        self.name = name
        self.price_string = price_string
        self.link = link

    @property
    def price(self) -> Optional[int]:
        """If the price contains both comma and a dot, dot is treated
        as separator for digit triples and the comma for floating values"""
        if price_group := re.search('(\d+.\d+),(\d+)', self.price_string):
            return int(price_group.group(1).replace('.', ''))
        price_extracted = ''.join(re.findall('[0-9]+', self.price_string))
        return int(price_extracted) if price_extracted else None

    @property
    def currency(self):
        from config.config import currency_map
        for key, values in currency_map.items():
            for value in values:
                if value in self.price_string:
                    return key
        return 'NA'

    @property
    def brand(self):
        return self.brand_manager.find_matching_brand(self.name)

    @property
    def model(self):
        if self.brand:
            return self.brand_manager.find_matching_model(self.brand, self.name)
