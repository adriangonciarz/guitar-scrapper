import os

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

brands_config_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'brands.yaml')

currency_map = {
    'PLN': ('zł', 'PLN'),
    'EUR': ('€', 'EUR'),
    'SEK': ('SEK', 'kr')
}
