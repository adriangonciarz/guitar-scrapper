import os

olx_basepath = 'https://www.olx.pl/muzyka-edukacja/instrumenty/'
kleinanziegen_basepath = 'https://www.ebay-kleinanzeigen.de/s-musikinstrumente/c74'
mercatino_basepath = 'https://www.mercatinomusicale.com/'
blocket_basepath = 'https://www.blocket.se/annonser/hela_sverige/fritid_hobby/musikutrustning/gitarr_bas_forstarkare?cg=6161'
markplaats_basepath = 'https://www.marktplaats.nl/l/muziek-en-instrumenten/snaarinstrumenten-gitaren-elektrisch/'

headless = False

# Proxy settings
proxy_enabled = os.getenv('PROXY_ENABLED')
proxy_server = os.getenv('PROXY_SERVER')
proxy_port = os.getenv('PROXY_PORT')
proxy_user = os.getenv('PROXY_USER')
proxy_password = os.getenv('PROXY_PASSWORD')
plugin_path = 'proxy_auth_plugin.zip'

brand_models = {
    'PRS': ('Custom 24', 'Custom 22', '408', 'McCarty', '594', 'Paul\'s Guitar'),
    'Fender': ('American Standard', 'American Special', 'Custom Shop', 'Masterbuilt', 'Esquire'),
    'Music Man': ('Luke', 'Cutlass', 'Silhouette', 'Reflex'),
    'Gibson': ('Les Paul Standard',),
    'Tom Anderson': ('Classic', 'Drop Top'),
    'Suhr': ('Classic', 'Modern'),
    'Parker': ('Fly Classic', 'Fly Mojo'),
    'Mayones': ('Aquila', 'Legend'),
    'Nik Huber': ('Krautster', 'Orca'),
    'Aristides': ('060',),
    'Eastman': ('sb59', 'sb57', 'sb55'),
    'James Tyler': ('Studio Elite',),
    'Valley Arts': ('Custom', 'California', 'M series'),
    'Harmony': ('Jupiter', 'Rebel', 'Comet'),
}


def search_terms():
    terms = []
    for brand in brand_models.keys():
        for model in brand_models[brand]:
            terms.append(f'{brand} {model}'.lower())
    return terms
