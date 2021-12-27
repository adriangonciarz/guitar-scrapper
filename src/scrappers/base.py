import os
import zipfile
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import config
from utils import PriceInfo, sanitize_string

def write_zip_plugin(plugin_path):
    proxy_server = os.getenv('PROXY_SERVER')
    proxy_port = os.getenv('PROXY_PORT')
    proxy_user = os.getenv('PROXY_USER')
    proxy_password = os.getenv('PROXY_PASSWORD')
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
    """ % (proxy_server, proxy_port, proxy_user, proxy_password)
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)


def prepare_driver() -> webdriver.Chrome:
    options = Options()
    options.headless = config.headless
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    if os.getenv('PROXY_ENABLED'):
        pluginfile = 'proxy_auth_plugin.zip'
        write_zip_plugin(pluginfile)
        options.add_extension(pluginfile)
    # options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options)
    # driver.maximize_window()
    return driver


class BaseScrapper:
    input_selector = None
    result_container_selector = None
    title_selector = None
    price_selector = None
    link_selector = None
    cookies_accept_selector = None

    def __init__(self, base_path):
        self.base_path = base_path
        self.driver = prepare_driver()
        self.price_data: [PriceInfo] = []

    def open_page(self):
        self.driver.get(self.base_path)
        if self.cookies_accept_selector:
            sleep(1)
            self.driver.find_element(*self.cookies_accept_selector).click()

    def quit_page(self):
        self.driver.quit()

    def dump_price_data_as_csv(self, filename):
        s = '\n'.join(
            [f'{pi.brand};{pi.model};{sanitize_string(pi.name)};{pi.price};{pi.currency};{pi.link}' for pi in self.price_data])
        with open(filename, 'w') as f:
            f.write(s)

    def search_and_scrap(self, query) -> [PriceInfo]:
        self.search_for_term(query)
        self.scrap_page()

    def search_for_term(self, query):
        search_input = self.driver.find_element(*self.input_selector)
        search_input.clear()
        search_input.send_keys(query + Keys.ENTER)
        sleep(2)

    def scrap_page(self) -> [PriceInfo]:
        item_containers = self.driver.find_elements(*self.result_container_selector)
        for cont in item_containers:
            title_element = cont.find_element(*self.title_selector)
            link_element = cont.find_element(*self.link_selector)
            name = title_element.text
            link = link_element.get_attribute('href')
            price = cont.find_element(*self.price_selector).text
            self.price_data.append(PriceInfo(name, price, link))
