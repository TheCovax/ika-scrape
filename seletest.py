import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
#options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
zps = "https://zombie-pirates.website"
ika_lobby_url = "https://lobby.ikariam.gameforge.com/"
driver.get(ika_lobby_url)
#print(driver.page_source)

DISCONNECTED_MSG = 'Unable to evaluate script: no such window: target window already closed\nfrom unknown error: web view not found\n'


while True:
    logdict = driver.get_log("driver")
    if len(logdict) > 0:
        if logdict[0]["message"] == DISCONNECTED_MSG:
            break
    time.sleep(1)
