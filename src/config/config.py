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

brand_models = {
    'PRS': ('Custom 24', '408', 'McCarty', '594', 'Paul\'s Guitar', 'DGT'),
    'Fender': ('Telecaster Custom Shop', 'Stratocaster Custom Shop', 'Nocaster', 'Stratocaster Masterbuilt', 'Telecaster Masterbuilt'),
    'Music Man': ('Luke', 'Cutlass', 'Axis'),
    'Tom Anderson': ('Classic', 'Drop Top', 'Angel'),
    'Suhr': ('Modern', 'Scott Henderson'),
    'Nik Huber': ('Krautster',),
    'Eastman': ('sb59', 'sb57',),
    'James Tyler': ('Studio Elite', 'Burning Water', 'Classic'),
    # 'Valley Arts': ('Custom', 'California', 'M series'),
    'Maybach': ('Lester', 'Teleman', 'Capitol'),
    'Parker': ('Fly',),
    # 'Gibson': ('Les Paul Standard',),
    # 'Mayones': ('Aquila', 'Legend'),
    # 'Aristides': ('060',),
    # 'Harmony': ('Jupiter', 'Rebel', 'Comet'),
    # 'Melancon': ('Cajun', 'Custom'),
    # 'Lipe': ('Virtuoso', ''),
    # 'Haar': ('',),
    # 'Carvin': ('DC 127', 'Bolt'),
    # 'Fano': ('',),
    # 'Real Guitars': ('',),
    # 'SVL': ('',),
    # 'Nash': ('',),
    'Xotic': ('XSC', 'XTC')
}

currency_map = {
    'PLN': ('zł', 'PLN'),
    'EUR': ('€', 'EUR'),
    'SEK': ('SEK', 'kr')
}


def search_terms():
    terms = []
    for brand in brand_models.keys():
        for model in brand_models[brand]:
            terms.append(f'{brand} {model}'.lower())
    return terms
