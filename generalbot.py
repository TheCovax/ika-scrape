import requests
import json
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import sys
import time
import pytz
import random


def getGeneralViewRow(inner_html, verbose=False):
    soup = BeautifulSoup(inner_html, 'html.parser')

    cells = soup.findAll("td")
    rowString = "| "
    for c in cells:
        rowString = rowString + \
            str(c.getText(strip=True)).strip().replace("  ", "") + " | "

    if verbose:
        print(rowString)
        
    return rowString

def refreshGeneralViewStr(driver,url):
    res = ""
    driver.get(url)
    try:
        # generalVIEW = driver.find_element(By.ID, "embassyGeneralAttacksToAlly")
        embassyTable = driver.find_element(
            By.CLASS_NAME, "embassyTable").find_elements(By.TAG_NAME, "tr")
    except NoSuchElementException as e:
        print("Element not found!")
        return e
    for idx, row in enumerate(embassyTable):
        if idx > 0:
            res += getGeneralViewRow(row.get_attribute("innerHTML")) + "\n"
    return res

verbose = False
ikariam_cookie_path = "ikariam_cookie.txt"

if len(sys.argv) > 1:
    ika_cookie = sys.argv[1]
    for i in sys.argv:
        if "-v" in str(i):
            verbose = True
else:
    ika_cookie = open(ikariam_cookie_path).readline().strip()
    
world_view_url = "https://s305-en.ikariam.gameforge.com/?view=worldmap_iso"
city_view_url = "https://s305-en.ikariam.gameforge.com/?view=city"
options = Options()
#options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get(world_view_url)
driver.add_cookie({"name": "ikariam", "value": ika_cookie})


generalViewStr = ""
cityIdStr = "133455"
embassyPosStr = "9"
webhook_url = "https://discord.com/api/webhooks/1264720303918026763/COT-4RFFU2_xdb6LZk1q7tUAMKSp_-0gP_BNYhfv2NALPHVrpHNaj0eyjY_DGSxE33g4"
# old: "https://discord.com/api/webhooks/1260238289743511644/cXYGPvAeZVhjmGlOQ8txKTVkgABwPcYV4Bre1YlSeM147qfeSq9r4kcxV0HPWd1-IsNO"
params = "?wait=true"

data = {
    "content": "Loading General View..."
}

allowedMentions = {
        
    }

response = requests.post(webhook_url+params, json=data)
print(response.text)
message_id = json.loads(response.text)["id"]
driver.get(city_view_url)

run = True
while run:
    try:
        attacksToAllyUrl = city_view_url.replace("city", f"embassyGeneralAttacksToAlly&cityId={cityIdStr}&position={embassyPosStr}&activeTab=tabEmbassy")
        lastGeneralViewStr = generalViewStr
        generalViewStr = str(refreshGeneralViewStr(driver,attacksToAllyUrl))
        if not (generalViewStr == lastGeneralViewStr or generalViewStr in lastGeneralViewStr or generalViewStr in "| No members of your alliance are being attacked at the moment. | "):
            requests.post("https://discord.com/api/webhooks/1286092006275158037/3wBws9InBkjQtXLhcJOZng_0qqeLmANeBeuPaJr-NYU5BfEJ0g6ubLWJSFOghOlFeQ_-",
                          json={
                              "content":"<@508044939863523329> <@396715532101091329> <@380488161538867200>",
                              "allowed_mentions": { "users": ["508044939863523329, 396715532101091329, 380488161538867200"] }   
                              }
                          )
    except NoSuchElementException:
        generalViwStr = "page didn't load, retrying..."
    else:
        generalViwStr = "@ Covax please "
        data["content"] = "<@396715532101091329>"
        
    currentTime = datetime.datetime.now(tz=pytz.timezone(
        "Europe/Budapest")).strftime("%Y-%m-%d %H:%M:%S")
    
    if verbose:
        print(currentTime)

    data["content"] = "GENERAL VIEW - Attacks on Alliance\t(" + \
        currentTime+")\n"+"```"+generalViewStr+"```"

    try:
        requests.patch(webhook_url+"/messages/"+message_id+params, json=data)
    except:
        time.sleep(60)

    time.sleep(random.random()*17+34)
