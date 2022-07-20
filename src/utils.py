import re
from typing import Optional

import config
from config import currency_map


class Item:
    def __init__(self, name: str, price_string: str, link: str):
        self.name = name
        self.price_string = price_string
        self.link = link

    @property
    def price(self) -> Optional[int]:
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
        for b in config.brand_models.keys():
            if b.lower() in self.name.lower():
                return b
        return None

    @property
    def model(self):
        if self.brand:
            for model in config.brand_models[self.brand]:
                if model.lower() in self.name.lower():
                    return model
            return None


def sanitize_string(input_string: str):
    return input_string.replace(',', '').replace(';', ' ')
