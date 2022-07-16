import logging
import os
import threading
import zipfile

import config
from config import search_terms
from scrappers.ebay_kleinanziegen import KleinanzeigenScrapper
from scrappers.olx import OLXScrapper
from scrappers.blocket import BlocketScrapper
from scrappers.markplaats import MarkplaatsScrapper
from scrappers.mercatino import MercatinoScrapper
from scrappers.zikinf import ZikinfScrapper
import argparse

page_scrappers_map = {
    'olx': OLXScrapper,
    'blocket': BlocketScrapper,
    'markplaats': MarkplaatsScrapper,
    'mercatino': MercatinoScrapper,
    'kleinanziegen': KleinanzeigenScrapper,
    'zikinf': ZikinfScrapper
}
supported_pages = ", ".join(page_scrappers_map.keys())

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--page", help="Key of the page to scrap")
args = parser.parse_args()


class MissingPageException(Exception):
    pass


class UnknownScrapperException(Exception):
    pass


def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http'):
    import string
    import zipfile

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                  },
                  bypassList: ["foobar.com"]
                }
              };
     
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
     
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
     
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: [""]},
                    ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(config.plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)


if __name__ == '__main__':
    if not args.page:
        raise MissingPageException(f'Provide parameter --page with page key to use from: {supported_pages}')
    if args.page not in page_scrappers_map:
        raise UnknownScrapperException(f'Unknown page key: {args.page}, allowed keys: {supported_pages}')
    # create_proxyauth_extension(config.proxy_server, config.proxy_port, config.proxy_user, config.proxy_password)
    scrapper_class = page_scrappers_map[args.page]
    scrapper = scrapper_class()
    scrapper.open_page()
    for term in search_terms():
        scrapper.search_and_scrap(term)
        print(scrapper.items)
    scrapper.dump_price_data_as_csv(f'{scrapper_class.__name__}.csv')
    scrapper.quit_page()
