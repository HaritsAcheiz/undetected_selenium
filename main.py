import requests
import json
import random
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

socket.setdefaulttimeout(180)


class UndetectedSelenium:
    # Constructor
    def __init__(self, search_term=None):
        self.search_term = search_term

    def get_proxies(self):
        # url = 'https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt'
        url = 'https://github.com/TheSpeedX/PROXY-List/blob/master/socks5.txt'
        proxies = []
        response = requests.get(url)
        soup = bs(response.content, 'html.parser').find_all("td", {"class": "blob-code blob-code-inner js-file-line"})
        for i in soup:
            proxies.append(i.text)
        return proxies


    def working_proxy(self, proxies):
        url = 'https://www.showmyip.com/'
        proxy = []
        for i, item in enumerate(proxies):
            if i < len(proxies) and len(proxy) < 3:
                formated_proxy = {
                    "http": f"socks5://{item}",
                    "https": f"socks5://{item}"
                }

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
        # ua = UserAgent()
        # useragent = ua.firefox
        useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        firefox_options = Options()
        firefox_options.page_load_strategy = 'eager'
        firefox_options.proxy = Proxy(
            {
            'proxyType': ProxyType.MANUAL,
            "socksVersion": 5,
            'httpProxy': proxy,
            'sslProxy': proxy,
            "socksProxy": proxy,
            'noProxy': ''
            }
        )

        # firefox_options.headless = True
        firefox_options.add_argument('--no-sandbox')
        firefox_options.set_preference("general.useragent.override", useragent)
        firefox_options.set_preference("network.cookie.cookieBehavior", 2);

        return firefox_options

if __name__ == '__main__':
    s = Service('C:/geckodriver-v0.31.0-win64/geckodriver.exe')
    us = UndetectedSelenium()
    proxy_lists = us.get_proxies()
    selected_proxy = us.working_proxy(proxies=proxy_lists)
    print(selected_proxy)
    counter = 0
    proxy = random.choice(selected_proxy)
    # while 1:
    #     if counter % 5 == 0:
    #         proxy = random.choice(selected_proxy)
    #     else:
    #         continue
    #
    #     option = us.webdriver_setup(proxy=proxy)
    #
    #     with webdriver.Firefox(service=s, options=option) as driver:
    #         response = driver.get('https://www.etsy.com')
    # print(proxy)
    option = us.webdriver_setup(proxy=proxy)
    driver = webdriver.Firefox(service=s, options=option)
    driver.set_page_load_timeout(25)
    driver.implicitly_wait(20)
    driver.set_script_timeout(20)
    response = driver.get('https://reqbin.com/echo')
    print(response)





