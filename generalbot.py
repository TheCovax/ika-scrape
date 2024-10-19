import requests
import json
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import sys
import time
import pytz
import random
import re

attacksOnAlliesList = []
oldAttacksList = []

def extract_city_id(cell_content):
    city_id_match = re.search(r'cityId=(\d+)', str(cell_content))
    if city_id_match:
        return city_id_match.group(1)
    return None

def getGeneralViewRowAsList(inner_html):
    contents = []
    res_list = []
    soup = BeautifulSoup(inner_html,'html.parser')
    cells = soup.find_all("td")
    if len(cells) > 1:
        for c in cells:
            contents.append(c.contents)



        period = str(contents[0])
        enddate_match = re.search(r'enddate:\s*(\d+)', period)
        if enddate_match:
            period = int(enddate_match.group(1))
        else:
            print("End Epoch Time not found")

        res_list.append(period)                         #time period of action
        res_list.append(contents[1][0])                 #Type of action
        res_list.append(contents[2][0])                          #Number of attacking units
        res_list.append(extract_city_id(contents[3]))   #Attacker City ID
        res_list.append(extract_city_id(contents[4]))   #Ally City ID
        
        return res_list
    else:
        return None

def getGeneralViewRowStr(inner_html, verbose=False):
    soup = BeautifulSoup(inner_html, 'html.parser')

    cells = soup.find_all("td")
    rowString = "| "
    for c in cells:
        rowString = rowString + str(c.getText(strip=True)).strip().replace("  ", "") + " | "

    if verbose:
        print(rowString)
        
    return rowString

def refreshGeneralViewStr(driver):
    global attacksOnAlliesList, oldAttacksList
    url = city_view_url.replace("city", f"embassyGeneralAttacksToAlly&cityId={cityIdStr}&position={embassyPosStr}&activeTab=tabEmbassy")
    res = ""
    try:
        driver.get(url)
        embassyTable = driver.find_element(
            By.CLASS_NAME, "embassyTable").find_elements(By.TAG_NAME, "tr")
    except NoSuchElementException as e:
        print("Element not found!")
        return e
    except TimeoutException as e:
        return e
    except Exception as e:
        return e
    oldAttacksList = list(attacksOnAlliesList)
    attacksOnAlliesList = []
    for idx, row in enumerate(embassyTable):
        if idx > 0:
            res += getGeneralViewRowStr(row.get_attribute("innerHTML")) + "\n"
            attacksOnAlliesList.append(getGeneralViewRowAsList)
    return res

verbose = True
ikariam_cookie_path = "ikariam_cookie.txt"

if len(sys.argv) > 1:
    #ika_cookie = sys.argv[1]
    for i in sys.argv:
        if "-v" in str(i):
            verbose = True
        if str(i) == "-c" and len(sys.argv)>i+1:
            ika_cookie = sys.argv[i+1]
else:
    ika_cookie = open(ikariam_cookie_path).readline().strip()
    
world_view_url = "https://s305-en.ikariam.gameforge.com/?view=worldmap_iso"
city_view_url = "https://s305-en.ikariam.gameforge.com/?view=city"
options = Options()
options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get(world_view_url)
driver.add_cookie({"name": "ikariam", "value": ika_cookie})


generalViewStr = ""
cityIdStr = "133455"
embassyPosStr = "9"
webhook_url = "https://discord.com/api/webhooks/1264720303918026763/COT-4RFFU2_xdb6LZk1q7tUAMKSp_-0gP_BNYhfv2NALPHVrpHNaj0eyjY_DGSxE33g4"
params = "?wait=true"

data = {
    "content": "Loading General View..."
}

allowedMentions = {
    "users": ["508044939863523329", "396715532101091329", "380488161538867200"]   
}

response = requests.post(webhook_url+params, json=data)
message_id = json.loads(response.text)["id"]
driver.get(city_view_url)



run = True
while run:
    try:
        
        lastGeneralViewStr = generalViewStr
        generalViewStr = str(refreshGeneralViewStr(driver)).strip()
        if verbose:
            print("\nold: ",str(oldAttacksList),"\n")
            print("new: ",str(attacksOnAlliesList),"\n")
        for event in attacksOnAlliesList:
            if verbose:
                print(event)
            if event not in oldAttacksList and generalViewStr not in "| No members of your alliance are being attacked at the moment. | ":
                requests.post("https://discord.com/api/webhooks/1286092006275158037/3wBws9InBkjQtXLhcJOZng_0qqeLmANeBeuPaJr-NYU5BfEJ0g6ubLWJSFOghOlFeQ_-",
                            json={
                                "content":"<@508044939863523329> <@396715532101091329> <@380488161538867200>\nAlly under attack!",
                                "allowed_mentions": {
                                        "parse": [],
                                        "users": allowedMentions["users"]
                                    }
                                }
                            )
    except NoSuchElementException:
        generalViewStr = "page didn't load, retrying..."
    except Exception as e:
        print(e)
        generalViewStr = "@ Covax please "
        data["content"] = "<@396715532101091329>"
        
    currentTime = datetime.datetime.now(tz=pytz.timezone("Europe/Budapest")).strftime("%Y-%m-%d %H:%M:%S")
    
    if verbose:
        print("\n"+currentTime + "-" +generalViewStr+"\n")

    data["content"] = "GENERAL VIEW - Attacks on Alliance\t(" + \
        currentTime+")\n"+"```"+generalViewStr+"```"

    try:
        requests.patch(webhook_url+"/messages/"+message_id+params, json=data)
    except Exception:
        time.sleep(60)

    time.sleep(random.random()*17+34)
    #time.sleep(3)
