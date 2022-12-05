from random import choice
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.firefox.options import Options

def rotate():
    proxy_string = "147.135.65.90:10030	147.135.65.90:10032	51.81.109.223:10010"
    proxy_list = proxy_string.split(sep="\t")
    proxy = choice(proxy_list)
    ip, port = proxy.split(sep=':')
    ua = UserAgent()
    useragent = ua.firefox
    firefox_options = Options()

    firefox_options.headless = True
    firefox_options.add_argument('--no-sandbox')

    firefox_options.set_preference("general.useragent.override", useragent)
    firefox_options.set_preference('network.proxy.type', 1)
    firefox_options.set_preference('network.proxy.socks', ip)
    firefox_options.set_preference('network.proxy.socks_port', int(port))
    firefox_options.set_preference('network.proxy.socks_remote_dns', True)

    firefox_options.set_capability("acceptSslCerts", True)
    firefox_options.set_capability("acceptInsecureCerts", True)
    firefox_options.set_capability("ignore-certificate-errors", True)

    driver = webdriver.Firefox(options=firefox_options)
    return driver

def reset_ip():
    firefox_options = Options()
    # firefox_options.binary = r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
    firefox_options.proxy = Proxy(
        {
            'proxyType': ProxyType.SYSTEM
        }
    )
    driver = webdriver.Firefox(options=firefox_options)
    return driver

if __name__ == '__main__':
    counter = 1
    while counter < 10:
        # if counter % 2 == 0:
        #     driver = rotate()
        # else:
        #     pass
        driver = rotate()
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