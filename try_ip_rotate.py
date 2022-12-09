from random import choice
from time import sleep

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
import os
import csv

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# proxy_string = "67.207.190.112:20000:Narusegawa:M1tsut4n1,67.207.190.114:20000:Narusegawa:M1tsut4n1,67.207.190.116:20000:Narusegawa:M1tsut4n1"
# proxy_list = proxy_string.split(sep=",")

def webdriver_setup(proxies = None):
    ip, port = proxies.split(sep=':')
    ua = UserAgent()
    useragent = ua.firefox
    firefox_options = Options()

    # firefox_options.headless = True
    firefox_options.add_argument('--no-sandbox')

    firefox_options.set_preference("general.useragent.override", useragent)
    firefox_options.set_preference('network.proxy.type', 1)
    firefox_options.set_preference('network.proxy.socks', ip)
    firefox_options.set_preference('network.proxy.socks_port', int(port))
    firefox_options.set_preference('network.proxy.socks_version', 4)
    # firefox_options.set_preference('network.proxy.socks_remote_dns', True)
    # firefox_options.set_preference('network.proxy.http', ip)
    # firefox_options.set_preference('network.proxy.http_port', int(port))
    # firefox_options.set_preference('network.proxy.ssl', ip)
    # firefox_options.set_preference('network.proxy.ssl_port', int(port))

    # firefox_options.set_capability("acceptSslCerts", True)
    # firefox_options.set_capability("acceptInsecureCerts", True)
    # firefox_options.set_capability("ignore-certificate-errors", False)

    driver = webdriver.Firefox(options=firefox_options)
    return driver

def to_csv(datas=None, filepath='C:/project/etsy/result/result_sel.csv'):
    print('Creating file...')
    folder = filepath.rsplit("/", 1)[0]
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass
    with open(filepath, 'w+', encoding="utf-8", newline='') as f:
        headers = ['url', 'title', 'price', 'sales']
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for i in datas:
            writer.writerow(i)
        f.close()
    print(f'{filepath} created')

def get_proxy():
    with requests.Session() as s:
        response = s.get('https://www.socks-proxy.net/')
    s.close()
    soup = BeautifulSoup(response.text, 'html.parser')
    list_data = soup.select('table.table.table-striped.table-bordered>tbody>tr')
    proxy_data= []
    for i in list_data:
        ip = i.select_one('tr > td:nth-child(1)').text
        port = i.select_one('tr > td:nth-child(2)').text
        proxy_data.append(f'{ip}:{port}')
    return proxy_data

def choose_proxy(proxies):
    proxy=[]
    for i, item in enumerate(proxies):
        if i < len(proxies) and len(proxy) < 3:
            formated_proxy = {
                "http": f"socks4://{item}",
                "https": f"socks4://{item}"
            }
            print(f'checking {formated_proxy}')
            try:
                with requests.Session() as session:
                    session.get(url='https://www.etsy.com', proxies=formated_proxy, timeout=3)
                session.close()
                proxy.append(item)
                print(f'{item} selected')
            except Exception as e:
                print(f"not working with {e}")
                pass
        else:
            break
    return proxy

if __name__ == '__main__':
    page = 249
    proxy_list = choose_proxy(get_proxy())
    print(proxy_list)
    # proxy_list = ['125.27.10.84:4153', '78.130.151.74:1088', '138.186.133.161:4153']
    proxy = choice(proxy_list)
    # ip, port, user, pw = proxy.split(sep=':')
    ip, port = proxy.split(sep=':')
    url = 'https://www.etsy.com/'
    search_term = 'necklace'
    driver = webdriver_setup(proxies=proxy)
    driver.delete_all_cookies()
    driver.fullscreen_window()
    driver.implicitly_wait(10)
    driver.get(url)
    sleep(10)
    driver.find_element(By.ID, 'global-enhancements-search-query').send_keys(search_term + Keys.RETURN)
    sleep(10)
    query_url = driver.current_url
    search_url = f'{query_url}&ref=pagination&page={str(page)}'
    data = {'url': '', 'title': '', 'price': '', 'sales': ''}
    res = []
    #
    while True:
        if page % 3 == 0:
            proxy = choice(proxy_list)
        else:
            pass
        search_url = f'{query_url}&ref=pagination&page={str(page)}'
        driver = webdriver_setup(proxy)
        driver.delete_all_cookies()
        driver.fullscreen_window()
        driver.implicitly_wait(10)

        driver.get(search_url)
        try:
            result = driver.find_elements(By.CSS_SELECTOR,
                                           'ol.wt-grid.wt-grid--block.wt-pl-xs-0.tab-reorder-container > li')
        except Exception as e:
            print(e)
            break

        for i in result:
            try:
                data['url'] = i.find_element(By.CSS_SELECTOR, 'a.listing-link.wt-display-inline-block').get_attribute(
                    'href')
            except TypeError:
                print('not found')
                break
            data['title'] = i.find_element(By.CSS_SELECTOR, 'h3.wt-text-caption.v2-listing-card__title').text
            data['title'] = re.sub(r'\n +', '', data['title'])
            data['price'] = i.find_element(By.CSS_SELECTOR,
                                           'div.n-listing-card__price.wt-display-flex-xs.wt-align-items-center > p.wt-text-title-01.lc-price > span:nth-of-type(2)').text
            data['price'] = re.sub(r'\D', '', data['price'])
            try:
                data['sales'] = i.find_element(By.CSS_SELECTOR,
                                               'span.wt-text-caption.wt-text-gray.wt-display-inline-block.wt-nudge-l-3.wt-pr-xs-1').text
                data['sales'] = re.sub(r'\D', '', data['sales'])
            except AttributeError:
                data['sales'] = 0
            res.append(data.copy())

        driver.quit()
        print(f'\n{len(res)} products collected by selenium from page {page}')
        page += 1

    to_csv(datas=res)
    # my_proxies = get_proxy()
    # working_proxies = choose_proxy(my_proxies)
    # print(working_proxies)