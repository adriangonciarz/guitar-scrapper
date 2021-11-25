from config import search_terms
from scrappers.ebay_kleinanziegen import KleinanzeigenScrapper
from scrappers.olx import OLXScrapper

# scrapper = OLXScrapper()
scrapper = KleinanzeigenScrapper()
scrapper.open_page()
for term in search_terms():
    scrapper.search_and_scrap(term)
    print(scrapper.price_data)
scrapper.dump_price_data_as_csv('../kleinanziegen.csv')
scrapper.quit_page()
