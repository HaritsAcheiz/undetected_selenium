import requests
import json
import random
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from fake_useragent import UserAgent


class UndetectedSelenium:
    # Constructor
    def __init__(self, search_term=None):
        self.search_term = search_term

    def get_proxies(self):
        url = 'https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt'
        proxies = []
        response = requests.get(url)
        soup = bs(response.content, 'html.parser').find_all("td", {"class": "blob-code blob-code-inner js-file-line"})
        for i in soup:
            proxies.append(i.text)

        return proxies

    def working_proxy(self, proxies):
        url = 'https://www.google.com'
        proxy = []
        for i, item in enumerate(proxies):
            if i < 10:
                formated_proxy = {"http":item}
                print(f'checking {formated_proxy}')
                try:
                    with requests.Session() as session:
                        session.get(url=url, proxies=formated_proxy, timeout=3)
                    proxy.append(item)
                    print(f'{item} selected')
                except Exception as e:
                    print("not working")
                    pass
            else:
                break

        return proxy

    def webdriver_setup(self, proxy):
        host, port = proxy.split(sep=':')
        ua = UserAgent()
        useragent = ua.firefox
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("network.proxy.type", 1)  # 1 for MANUAL
        firefox_options.set_preference("network.proxy.http", host)
        firefox_options.set_preference("network.proxy.http_port", int(port))
        firefox_options.set_preference("network.proxy.ssl", host)
        firefox_options.set_preference("network.proxy.ssl_port", int(port))
        # firefox_options.headless = True
        firefox_options.set_preference("")

        return firefox_options

if __name__ == '__main__':
    us = UndetectedSelenium()
    proxy_lists = us.get_proxies()
    selected_proxy = us.working_proxy(proxies=proxy_lists)




