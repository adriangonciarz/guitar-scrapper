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

scrapper_classes = [
    # OLXScrapper,
    BlocketScrapper,
    # MarkplaatsScrapper,
    # MercatinoScrapper,
    # KleinanzeigenScrapper
]
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


def write_zip_plugin():
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
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
            username: "%s",
            password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
    );
    """ % (config.proxy_server, config.proxy_port, config.proxy_user, config.proxy_password)
    with zipfile.ZipFile(config.plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)


def perform_scrap(scrapper_class):
    scrapper = scrapper_class()
    scrapper.open_page()
    for term in search_terms():
        scrapper.search_and_scrap(term)
        print(scrapper.price_data)
    scrapper.dump_price_data_as_csv(f'{scrapper_class.__name__}.csv')
    scrapper.quit_page()


if __name__ == '__main__':
    threads = list()
    if config.proxy_enabled:
        write_zip_plugin()

    for scrapper_class in scrapper_classes:
        scrap_name = scrapper_class.__name__
        logging.info("Main    : create and start scrapper %s.", scrap_name)
        x = threading.Thread(target=perform_scrap, args=(scrapper_class,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()
