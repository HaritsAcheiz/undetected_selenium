import time
from random import choice
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
import os
import csv
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


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
    firefox_options.set_preference('network.proxy.socks_remote_dns', True)
    firefox_options.set_preference('network.proxy.http', ip)
    firefox_options.set_preference('network.proxy.http_port', int(port))
    firefox_options.set_preference('network.proxy.ssl', ip)
    firefox_options.set_preference('network.proxy.ssl_port', int(port))

    firefox_options.set_capability("acceptSslCerts", True)
    firefox_options.set_capability("acceptInsecureCerts", True)
    firefox_options.set_capability("ignore-certificate-errors", False)

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
        response = s.get('https://free-proxy-list.net/')
    s.close()
    soup = BeautifulSoup(response.text, 'html.parser')
    list_data = soup.select('table.table.table-striped.table-bordered>tbody>tr')
    proxy_data= []
    blocked_cc = ['IR','RU']
    for i in list_data:
        ip = i.select_one('tr > td:nth-child(1)').text
        port = i.select_one('tr > td:nth-child(2)').text
        cc = i.select_one('tr > td:nth-child(3)').text
        if cc in blocked_cc:
            continue
        else:
            proxy_data.append(f'{ip}:{port}')
    return proxy_data

def choose_proxy(proxies):
    proxy=[]
    for i, item in enumerate(proxies):
        if i < len(proxies) and len(proxy) < 5:
            formated_proxy = {
                "http": f"http://{item}",
                "https": f"http://{item}"
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

def get_data(page=1, proxy=None):
    while True:
        try:
            driver = webdriver_setup(proxies=proxy)
            driver.delete_all_cookies()
            driver.fullscreen_window()
            # driver.implicitly_wait(10)
            driver.get(url)
            WebDriverWait(driver,10).until(ec.presence_of_element_located((By.ID, 'global-enhancements-search-query')))
            driver.find_element(By.ID, 'global-enhancements-search-query').send_keys(search_term + Keys.RETURN)
        # WebDriverWait(driver,10).until(ec.presence_of_element_located((By.ID, 'content')))
            time.sleep(10)
            query_url = driver.current_url
            driver.quit()
            break
        except WebDriverException as e:
            print(e)
            proxy = choice(proxy_list)
            driver.quit()
            continue
    data = {'url': '', 'title': '', 'price': '', 'sales': ''}
    res = []
    while True:
        if page % 3 == 0 :
            proxy = choice(proxy_list)
        else:
            pass
        search_url = f"{query_url}&ref=pagination&page={str(page)}"
        while True:
            try:
                driver = webdriver_setup(proxy)
                driver.delete_all_cookies()
                driver.fullscreen_window()
                # driver.implicitly_wait(10)
                driver.get(search_url)
                break
            except WebDriverException as e:
                print(e)
                proxy = choice(proxy_list)
                continue

        WebDriverWait(driver,10).until(ec.presence_of_element_located((By.ID, 'content')))
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
            except (TypeError, NoSuchElementException) as e:
                print(e)
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
            except (AttributeError, NoSuchElementException) as e:
                data['sales'] = 0
            res.append(data.copy())

        driver.quit()
        print(f'\n{len(res)} products collected by selenium from page {page}')
        page += 1
    return res


if __name__ == '__main__':
    # Define variable input
    page = 249
    url = 'https://www.etsy.com'
    search_term = 'necklace'

    # Get proxy list
    proxy_list = choose_proxy(get_proxy())
    print(proxy_list)

    # random choice proxy from proxy list
    # proxy_list = ['134.238.252.143:8080', '185.143.146.171:8080', '213.230.97.98:3128']
    proxy = choice(proxy_list)

    # Get data
    res = get_data(page=page, proxy=proxy)

    # Export to csv
    to_csv(datas=res)
