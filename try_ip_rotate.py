from random import choice
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

s = Service('C:/geckodriver-v0.31.0-win64/geckodriver.exe')

def rotate():
    proxy_string = "147.135.65.90:40014 147.135.65.90:40015	51.81.109.223:40012	51.81.109.223:40013	51.81.109.223:40014"
    proxy_list = proxy_string.split(sep="\t")
    proxy = choice(proxy_list)
    ua = UserAgent()
    useragent = ua.firefox
    firefox_options = Options()
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
    firefox_options.headless = True
    firefox_options.add_argument('--no-sandbox')
    firefox_options.set_preference("general.useragent.override", useragent)
    firefox_options.accept_insecure_certs = True

    return webdriver.Firefox(service=s, options=firefox_options)

if __name__ == '__main__':
    counter = 1
    driver = rotate()
    while counter < 10:
        if counter % 2 == 0:
            driver = rotate()
        else:
            pass
        driver.fullscreen_window()
        driver.implicitly_wait(10)
        driver.get('https://www.showmyip.com')
        myIP = driver.find_element(By.CSS_SELECTOR, "section.container.clearfix > h2").text
        driver.get("https://www.whatismybrowser.com/")
        mybrowser = driver.find_element(By.CSS_SELECTOR, "div.string-major > a").text
        print(f"{counter} try")
        print(f"Proxy: {myIP}, Browser: {mybrowser}")
        driver.quit()
        counter += 1