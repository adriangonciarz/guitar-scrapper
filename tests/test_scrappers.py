from scrappers.base import BaseScrapper
from models import Item


def test_adding_already_scrapped_items():
    scrapper = BaseScrapper('some_base_path')
    scrapper.items = [
        Item('PRS Custom 24', '13.54', 'https://example.com/items/1234151'),
        Item('PRS Custom 22', '23.54', 'https://example.com/items/1234157?promote=true'),
    ]
    test_item_1 = Item('PRS Custom 24', '13.54', 'https://example.com/items/1234151?promote=true')
    test_item_2 = Item('PRS Custom 24', '13.54', 'https://example.com/items/1234157')
    scrapper.add_item(test_item_1)
    assert len(scrapper.items) == 2
    scrapper.add_item(test_item_2)
    assert len(scrapper.items) == 2
