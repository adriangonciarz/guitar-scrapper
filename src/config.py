import os

olx_basepath = 'https://www.olx.pl/muzyka-edukacja/instrumenty/'
kleinanziegen_basepath = 'https://www.ebay-kleinanzeigen.de/s-musikinstrumente/c74'
mercatino_basepath = 'https://www.mercatinomusicale.com/'
blocket_basepath = 'https://www.blocket.se/annonser/hela_sverige/fritid_hobby/musikutrustning/gitarr_bas_forstarkare?cg=6161'
marktplaats_basepath = 'https://www.marktplaats.nl/l/muziek-en-instrumenten/snaarinstrumenten-gitaren-elektrisch/'
zikinf_basepath = 'https://www.zikinf.com/annonces/liste.php?rub=9'

headless = False

# Proxy settings
proxy_enabled = os.getenv('PROXY_ENABLED')
proxy_server = os.getenv('PROXY_SERVER')
proxy_port = os.getenv('PROXY_PORT')
proxy_user = os.getenv('PROXY_USER')
proxy_password = os.getenv('PROXY_PASSWORD')
plugin_path = 'proxy_auth_plugin.zip'

brand_models = {
    'PRS': ('Custom 24', '408', 'McCarty', '594', 'Paul\'s Guitar', 'DGT'),
    'Fender': ('Custom Shop', 'masterbuilt'),
    'Music Man': ('Luke', 'Cutlass',),
    'Tom Anderson': ('Classic', 'Drop Top', 'Angel'),
    'Suhr': ('Classic', 'Modern', 'Scott Henderson'),
    'Nik Huber': ('Krautster', 'Orca', 'Dolphin'),
    'Eastman': ('sb59', 'sb57', 'sb55'),
    'James Tyler': ('Studio Elite', 'Burning Water'),
    'Valley Arts': ('Custom', 'California', 'M series'),
    'Maybach': ('Lester', 'Teleman', 'Capitol'),

    # 'Parker': ('Fly Classic', 'Fly Mojo'),
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
}

currency_map = {
    'PLN': ('zł', 'PLN'),
    'EUR': ('€', 'EUR'),
    'SEK': ('kr', 'SEK')
}


def search_terms():
    terms = []
    for brand in brand_models.keys():
        for model in brand_models[brand]:
            terms.append(f'{brand} {model}'.lower())
    return terms
