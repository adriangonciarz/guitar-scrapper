import dataclasses
import re
from typing import Optional

import yaml

from config.config import currency_map, brand_models
from utils import unify_item_name


class Item:
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
        for key, values in currency_map.items():
            for value in values:
                if value in self.price_string:
                    return key
        return 'NA'

    @property
    def brand(self):
        for b in brand_models.keys():
            if unify_item_name(b) in unify_item_name(self.name):
                return b
        return None

    @property
    def model(self):
        if self.brand:
            for model in brand_models[self.brand]:
                if unify_item_name(model) in unify_item_name(self.name):
                    return model
            return None


@dataclasses.dataclass
class Model:
    name: str
    search: bool
    aliases: [str]


@dataclasses.dataclass
class Brand:
    name: str
    models: [Model]
    aliases: [str]


class SearchManager:
    def __init__(self, config_path):
        self.brands: [Brand] = []

        with open(config_path) as file:
            brands_config = yaml.load(file, Loader=yaml.FullLoader)
            for brand in brands_config:
                models = [Model(m['name'], m['search'], m['aliases']) for m in brand['models']]
                self.brands.append(Brand(brand['brand'], models, brand['brand_aliases']))

    def get_brands(self):
        return [b.name for b in self.brands]

    def get_search_terms(self):
        terms = []
        for brand in self.brands:
            for model in brand.models:
                if model.search:
                    terms.append(f'{brand.name} {model.name}'.lower())
        return terms


if __name__ == '__main__':
    sm = SearchManager('config/brands.yaml')
    print(sm.get_brands())
    print(sm.get_search_terms())
