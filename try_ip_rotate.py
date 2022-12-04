import time
from random import choice
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# s = Service(r'C:/geckodriver-v0.32.0-win32/geckodriver.exe')
# path = r"C:/geckodriver-v0.32.0-win32/geckodriver.exe"

def rotate():
    proxy_string = "47.241.191.76:40059 47.241.191.76:40060 8.214.112.193:40034"
    proxy_list = proxy_string.split(sep=" ")
    proxy = choice(proxy_list)
    # proxy = "147.135.65.90:40034"
    ua = UserAgent()
    useragent = ua.firefox
    firefox_options = Options()
    firefox_options.binary = r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
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

    firefox_options.set_capability("acceptSslCerts", True)
    firefox_options.set_capability("acceptInsecureCerts", True)
    firefox_options.set_capability("ignore-certificate-errors", True)
    # driver = webdriver.Firefox(service=s, options=firefox_options)
    driver = webdriver.Firefox(options=firefox_options)
    return driver

    # return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

if __name__ == '__main__':
    counter = 1
    driver = rotate()
    while counter < 10:
        if counter % 2 == 0:
            driver = rotate()
        else:
            pass
        driver.delete_all_cookies()
        driver.fullscreen_window()
        driver.implicitly_wait(10)

        driver.get('https://www.showmyip.com/')
        myIP = driver.find_element(By.ID, "ipv4").text
        driver.get("https://www.whatismybrowser.com/")
        mybrowser = driver.find_element(By.CSS_SELECTOR, "div.string-major > a").text
        print(f"{counter} try")
        print(f"Proxy: {myIP}, Browser: {mybrowser}")
        driver.quit()
        counter += 1