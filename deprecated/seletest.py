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
ika_cityview = "https://s305-en.ikariam.gameforge.com/?view=city"
cookie = "156929_19b25e7f4aa8f58e6937de53654e3fa5"
f=open("cookie.txt")
cookie = f.readline()
print("cookie:"+cookie, type(cookie))
f.close()


driver.get(ika_cityview)
driver.add_cookie({"name":"ikariam","value":cookie})
driver.get(ika_cityview)

#print(driver.page_source)
#time.sleep(10)
DISCONNECTED_MSG = 'Unable to evaluate script: no such window: target window already closed\nfrom unknown error: web view not found\n'

''''''
while True:
    logdict = driver.get_log("driver")
    if len(logdict) > 0:
        if logdict[0]["message"] == DISCONNECTED_MSG:
            break
    new_cookie = driver.get_cookie("ikariam")["value"]
    f = open("cookie.txt","w")
    #print(new_cookie)
    if type(new_cookie) == type("asd"):	
    	f.write(new_cookie)
    f.close()
    time.sleep(5)
''''''
 
