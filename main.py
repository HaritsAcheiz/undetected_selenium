import requests
import json
from bs4 import BeautifulSoup as bs


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
        for i in proxies:
            formated_proxy = {"http":i}
            print(f'checking {formated_proxy}')
            try:
                response = requests.get(url=url, proxies=formated_proxy, timeout=3)
                print(response.content)
                proxy.append(i)
                print(f'{i} selected')
                break
            except Exception as e:
                print("not working")
                pass
        return proxy

if __name__ == '__main__':
    us = UndetectedSelenium()
    proxy_lists = us.get_proxies()
    selected_proxy = us.working_proxy(proxies=proxy_lists)
    print(selected_proxy)



