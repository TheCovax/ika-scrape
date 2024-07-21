import requests
import json
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys,time,pytz

def getGeneralViewRow(inner_html):
    soup = BeautifulSoup(inner_html, 'html.parser')

    cells = soup.findAll("td")
    rowString = "| "
    for c in cells:
        rowString = rowString + str(c.getText(strip=True)).strip().replace("  ","") + " | "

    print(rowString)
    return rowString

world_view_url = "https://s305-en.ikariam.gameforge.com/?view=worldmap_iso"
city_view_url = "https://s305-en.ikariam.gameforge.com/?view=city"
if len(sys.argv) > 1:
    ika_cookie = sys.argv[1]
else:
    ika_cookie = "156929_1bbc7871d9f8eca5cce97f185780a2e5"

options = Options()
options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get(world_view_url)
driver.add_cookie({"name": "ikariam", "value": ika_cookie})


generalViewStr = ""
cityIdStr = "133455"
embassyPosStr = "9"
asd = "https://discord.com/api/webhooks/1264720303918026763/COT-4RFFU2_xdb6LZk1q7tUAMKSp_-0gP_BNYhfv2NALPHVrpHNaj0eyjY_DGSxE33g4"
webhook_url = asd#"https://discord.com/api/webhooks/1260238289743511644/cXYGPvAeZVhjmGlOQ8txKTVkgABwPcYV4Bre1YlSeM147qfeSq9r4kcxV0HPWd1-IsNO"
params = "?wait=true"

def refreshGeneralViewStr(driver):
    res = ""
    driver.get(city_view_url.replace("city", f"embassyGeneralAttacksToAlly&cityId={cityIdStr}&position={embassyPosStr}&activeTab=tabEmbassy"))
    driver.find_element(By.ID, "embassyGeneralAttacksToAlly")
    embassyTable = driver.find_element(By.CLASS_NAME, "embassyTable").find_elements(By.TAG_NAME, "tr")
    for idx, row in enumerate(embassyTable):
        if idx > 0:
            res += getGeneralViewRow(row.get_attribute("innerHTML")) + "\n"
    return res

data = {
                "content": "General view"
            }

response = requests.post(webhook_url+params,json=data)
#print(response.text)
message_id = json.loads(response.text)["id"]
#print(message_id)
driver.get(city_view_url)
#time.sleep(10)
run = True
while run:
    generalViewStr = refreshGeneralViewStr(driver)
    currentTime = datetime.datetime.now(tz=pytz.timezone("Europe/Budapest")).strftime("%Y-%m-%d %H:%M:%S")
    print(currentTime)
    data = {
                "content": "GENERAL VIEW - Attacks on Alliance\t("+currentTime+")\n"+"```"+generalViewStr+"```"
            }
    
    requests.patch(webhook_url+"/messages/"+message_id+params,json=data)

    time.sleep(37)
