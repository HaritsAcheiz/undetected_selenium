from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.core.http import HttpClient
from webdriver_manager.core.download_manager import WDMDownloadManager
import requests

class CustomHttpClient(HttpClient):
    def get(self, url, params=None):
        proxies={
            'http': 'socks5:// *proxy adress*',
            'https': 'socks5:// *proxy adress*'
         }
        return requests.get(url, params, proxies=proxies, verify=False)

http_client = CustomHttpClient()
download_manager = WDMDownloadManager(http_client)

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager(download_manager=download_manager).install()))
driver.get('https://www.google.com')
print(driver.title)
driver.quit()

# driver = webdriver.Chrome(service=Service(ChromeDriverManager(download_manager=download_manager).install()),options=opt)`
