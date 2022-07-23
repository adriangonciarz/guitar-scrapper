import pytest

from models import Item


@pytest.mark.parametrize("test_item,expected_price", [
    (Item('PRS Custom 24 2003 Blood Orange', '1.870 €', 'http://www.ebay.com/item1234'), 1870),
    (Item('PRS Custom 24 2010 Green', '€ 2.429,00', 'http://www.ebay.com/item12345'), 2429),
    (Item('Xotic XTC-1', 'SEK 22,900', 'http://www.ebay.com/item124434'), 22900),
    (Item('Telecaster 52 US 1993', '1650 €', 'http://www.ebay.com/item1234'), 1650),
    (Item('Telecaster 52 US 1994', '71 900 zł', 'http://www.ebay.com/item1234'), 71900),
])
def test_item_price_value_parsing(test_item: Item, expected_price):
    assert test_item.price == expected_price


@pytest.mark.parametrize("test_item,expected_currency", [
    (Item('PRS Custom 24 2003 Blood Orange', '1.870 €', 'http://www.ebay.com/item1234'), 'EUR'),
    (Item('PRS Custom 24 2010 Green', '€ 2.429,00', 'http://www.ebay.com/item12345'), 'EUR'),
    (Item('Xotic XTC-1', 'SEK 22,900', 'http://www.ebay.com/item124434'), 'SEK'),
    (Item('Telecaster 52 US 1993', '1650 €', 'http://www.ebay.com/item1234'), 'EUR'),
    (Item('Telecaster 52 US 1994', '71 900 zł', 'http://www.ebay.com/item1234'), 'PLN'),
])
def test_item_currency_parsing(test_item: Item, expected_currency):
    assert test_item.currency == expected_currency
