import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import PySimpleGUI as sg

from file_operations import write_to_file

from ikaTrack import parse_ms_from_source
from gui import login_layout, create_main_layout
from ikaWorld import find_island, refresh_local_map
from IkaNoti import *


def set_offset_param(offset):
    url = "&offset=" + str(offset)
    return url

def fetch_military_hs(top, progressbar):
    full_data = "Position;Player Name;Alliance;Points\n"

    print("Fetching data:")
    for i in range(0,top,50):
        print("\tfetching positions "+str(i+1)+"-"+str(i+50)+"...")
        progressbar.UpdateBar(i+50)
        params=highscore_military_score_param + set_offset_param(i)
        driver.get(highscore_url+params)
            
        full_data+=(parse_ms_from_source(driver.page_source) + "\n") 
            
    print("Fetching Done!")
    out_file = str(time.localtime().tm_year)+"_"+str(time.localtime().tm_mon)+"_"+str(time.localtime().tm_mday) +"_"+str(time.localtime().tm_hour) +"_"+str(time.localtime().tm_min)+".csv"

    write_to_file(full_data,out_file)

def cook_ships():
    print("cooking...\n")

    navy = [0,0,0,0,0,0,0,0,0,0,0]

    driver.get(city_view_url)
    currentCity = driver.find_element(By.ID, "js_citySelectContainer").find_element(By.TAG_NAME,"a").click()
    dropdown = driver.find_element(By.ID,"dropDown_js_citySelectContainer")
    cities = dropdown.find_elements(By.CLASS_NAME, "ownCity")
    print(cities)
    for idx, i in enumerate(cities):
        print("84:"+i.text)
        i.click()
        print("87:"+i.text,i.tag_name)

        troops_in_town_button = driver.find_element(By.CLASS_NAME,"military")
        #dropdown_button = driver.find_element(By.ID, "js_citySelectContainer").find_element(By.TAG_NAME,"a").click()
        #dropdown_button.
        
def check_attacks():
    print("Checking for attacks...\n")
    cityIdStr = "87355"
    embassyPosStr = "13"
    driver.get(city_view_url.replace("city","embassyGeneralAttacksToAlly&cityId="+cityIdStr+"&position="+embassyPosStr+"&activeTab=tabEmbassy"))

    driver.find_element(By.ID,"embassyGeneralAttacksToAlly") #general_window = 
    embassyTable = driver.find_element(By.CLASS_NAME, "embassyTable").find_elements(By.TAG_NAME,"tr")
    generalViewString = "General view: Attacks on alliance\n"
    for idx,row in enumerate(embassyTable) :
        if idx > 0:
            generalViewString =  generalViewString + getGeneralViewRow(row.get_attribute("innerHTML")) + "\n"

    payloadToTxt()
    #sendDcNoti()


world_view_url = "https://s305-en.ikariam.gameforge.com/?view=worldmap_iso"
highscore_url = "https://s305-en.ikariam.gameforge.com/index.php?view=highscore"
city_view_url = "https://s305-en.ikariam.gameforge.com/?view=city"

highscore_military_score_param = "&highscoreType=army_score_main"
highscore_offset_param = set_offset_param(0)

lobby_url = "https://lobby.ikariam.gameforge.com/en_GB"

url = world_view_url

options = Options()
options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

trade_goods = [
    "Wine",
    "Marble",
    "Crystal Glass",
    "Sulphur",
    "none"
]
miracles = [
    "Hephaistos' Forge",
    "Hades' Holy Grove",
    "Demeter's Gardens",
    "Temple of Athene",
    "Temple of Hermes",
    "Ares' Stronghold",
    "Temple of Poseidon",
    "Colossus"
]


login_window = sg.Window("Ika-Scrape",login_layout)
auth_mode = 0
active_layout = "login"
while True:  #login loop
    
    event, values = login_window.read()
    if event == sg.WIN_CLOSED or 'Cancel' in event: # if user closes window or clicks cancel
        break
    elif event == "Select":
        login_window[f'login'].update(visible=False)
        if values[0]:
            active_layout = "cookie"
            login_window[f'cookie'].update(visible=True)
            continue
        elif values[1]:
            active_layout = "email"
            login_window[f'email'].update(visible=True)
            continue
    elif "Ok" in event and active_layout == "cookie":
        
        active_layout = "w84auth"
        login_window[f'cookie'].update(visible=False)
        login_window[f'w84auth'].update(visible=True)
        
        login_window.refresh()
        ika_cookie = values[2]
        driver.get(url)
        driver.add_cookie({"name": "ikariam", "value": ika_cookie})
        break
    elif "Ok" in event and active_layout == "email":
        active_layout = "w84auth"
        login_window[f'email'].update(visible=False)
        login_window[f'w84auth'].update(visible=True)
        event, values = login_window.read(10)
        driver.get(lobby_url)
        
        time.sleep(2)
        
        login_tab = driver.find_element(By.XPATH, "//ul[@class='tabsList']/li[text()='Log in']")
        register_tab = driver.find_element(By.XPATH, "//ul[@class='tabsList']/li[text()='Register']")
        login_tab.click()
        
        logintab = driver.find_element(By.ID, "loginTab")
        email_field = logintab.find_element(By.NAME,"email")
        pw_field = logintab.find_element(By.NAME,"password")
        
        time.sleep(1)
        
        email_in = values[3]
        password_in = values[4]
        
        email_field.send_keys(email_in)
        pw_field.send_keys(password_in)
        time.sleep(3)
        
        driver.find_element(By.CLASS_NAME, "button-lg").click()
        time.sleep(3)
        driver.get(lobby_url+"/accounts")
        time.sleep(1)
        
        pangaia5 = driver.find_element(By.XPATH, "//div[contains(text(), 'Pangaia 5')]")
        pangaia5.click() 
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "btn-primary").click()
        break
    
    #print(event, values)

if active_layout == "email":
    time.sleep(5)
    
driver.get(world_view_url)
logged_in = driver.find_element(By.CLASS_NAME, "noViewParameters").text

login_window.close()

xcoord_min = 1
xcoord_max = 100
ycoord_min = 1
ycoord_max = 100
citymax = 17
citymin = 0
is_ally = 0

toggle_btn_off = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAED0lEQVRYCe1WTWwbRRR+M/vnv9hO7BjHpElMKSlpqBp6gRNHxAFVcKM3qgohQSqoqhQ45YAILUUVDRxAor2VAweohMSBG5ciodJUSVqa/iikaePEP4nj2Ovdnd1l3qqJksZGXscVPaylt7Oe/d6bb9/svO8BeD8vA14GvAx4GXiiM0DqsXv3xBcJU5IO+RXpLQvs5yzTijBmhurh3cyLorBGBVokQG9qVe0HgwiXLowdy9aKsY3g8PA5xYiQEUrsk93JTtjd1x3siIZBkSWQudUK4nZO1w3QuOWXV+HuP/fL85klAJuMCUX7zPj4MW1zvC0Ej4yMp/w++K2rM9b70sHBYCjo34x9bPelsgp/XJksZ7KFuwZjr3732YcL64ttEDw6cq5bVuCvgy/sje7rT0sI8PtkSHSEIRIKgCQKOAUGM6G4VoGlwiqoVd2Za9Vl8u87bGJqpqBqZOj86eEHGNch+M7otwHJNq4NDexJD+59RiCEQG8qzslFgN8ibpvZNsBifgXmFvJg459tiOYmOElzYvr2bbmkD509e1ylGEZk1Y+Ssfan18n1p7vgqVh9cuiDxJPxKPT3dfGXcN4Tp3dsg/27hUQs0qMGpRMYjLz38dcxS7Dm3nztlUAb38p0d4JnLozPGrbFfBFm79c8hA3H2AxcXSvDz7/+XtZE1kMN23hjV7LTRnKBh9/cZnAj94mOCOD32gi2EUw4FIRUMm6LGhyiik86nO5NBdGRpxYH14bbjYfJteN/OKR7UiFZVg5T27QHYu0RBxoONV9W8KQ7QVp0iXdE8fANUGZa0QAvfhhXlkQcmjJZbt631oIBnwKmacYoEJvwiuFgWncWnXAtuVBBEAoVVXWCaQZzxmYuut68b631KmoVBEHMUUrJjQLXRAQVSxUcmrKVHfjWWjC3XOT1FW5QrWpc5IJdQhDKVzOigEqS5dKHMVplnNOqrmsXqUSkn+YzWaHE9RW1FeXL7SKZXBFUrXW6jIV6YTEvMAUu0W/G3kcxPXP5ylQZs4fa6marcWvvZfJu36kuHjlc/nMSuXz+/ejxgqPFpuQ/xVude9eu39Jxu27OLvBGoMjrUN04zrNMbgVmOBZ96iPdPZmYntH5Ls76KuxL9NyoLA/brav7n382emDfHqeooXyhQmARVhSnAwNNMx5bu3V1+habun5nWdXhwJZ2C5mirTesyUR738sv7g88UQ0rEkTDlp+1wwe8Pf0klegUenYlgyg7bby75jUTITs2rhCAXXQ2vwxz84vlB0tZ0wL4NEcLX/04OrrltG1s8aOrHhk51SaK0us+n/K2xexBxljcsm1n6x/Fuv1PCWGiKOaoQCY1Vb9gWPov50+fdEqd21ge3suAlwEvA14G/ucM/AuppqNllLGPKwAAAABJRU5ErkJggg=='
toggle_btn_on = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAD+UlEQVRYCe1XzW8bVRCffbvrtbP+2NhOD7GzLm1VoZaPhvwDnKBUKlVyqAQ3/gAkDlWgPeVQEUCtEOIP4AaHSI0CqBWCQyXOdQuRaEFOk3g3IMWO46+tvZ+PeZs6apq4ipON1MNafrvreTPzfvub92bGAOEnZCBkIGQgZOClZoDrh25y5pdjruleEiX+A+rCaQo05bpuvJ/+IHJCSJtwpAHA/e269g8W5RbuzF6o7OVjF8D3Pr4tSSkyjcqfptPDMDKSleW4DKIggIAD5Yf+Oo4DNg6jbUBlvWLUNutAwZu1GnDjzrcXzGcX2AHw/emFUV6Sfk0pqcKpEydkKSo9q3tkz91uF5aWlo1Gs/mYc+i7tz4//19vsW2AU9O381TiioVCQcnlRsWeQhD3bJyH1/MiFLICyBHiuzQsD1arDvypW7DR9nzZmq47q2W95prm+I9fXfqXCX2AF2d+GhI98Y8xVX0lnxvl2UQQg0csb78ag3NjEeD8lXZ7pRTgftmCu4864OGzrq+5ZU0rCa3m+NzXlzvoAoB3+M+SyWQuaHBTEzKMq/3BMbgM+FuFCDBd9kK5XI5PJBKqLSev+POTV29lKB8rT0yMD0WjUSYLZLxzNgZvIHODOHuATP72Vwc6nQ4Uiw8MUeBU4nHS5HA6TYMEl02wPRcZBJuv+ya+UCZOIBaLwfCwQi1Mc4QXhA+PjWRkXyOgC1uIhW5Qd8yG2TK7kSweLcRGKKVnMNExWWBDTQsH9qVmtmzjiThQDs4Qz/OUSGTwcLwIQTLW58i+yOjpXDLqn1tgmDzXzRCk9eDenjo9yhvBmlizrB3V5dDrNTuY0A7opdndStqmaQLPC1WCGfShYRgHdLe32UrV3ntiH9LliuNrsToNlD4kruN8v75eafnSgC6Luo2+B3fGKskilj5muV6pNhk2Qqg5v7lZ51nBZhNBjGrbxfI1+La5t2JCzfD8RF1HTBGJXyDzs1MblONulEqPDVYXgwDIfNx91IUVbAbY837GMur+/k/XZ75UWmJ77ou5mfM1/0x7vP1ls9XQdF2z9uNsPzosXPNFA5m0/EX72TBSiqsWzN8z/GZB08pWq9VeEZ+0bjKb7RTD2i1P4u6r+bwypo5tZUumEcDAmuC3W8ezIqSGfE6g/sTd1W5p5bKjaWubrmWd29Fu9TD0GlYlmTx+8tTJoZeqYe2BZC1/JEU+wQR5TVEUPptJy3Fs+Vkzgf8lemqHumP1AnYoMZSwsVEz6o26i/G9Lgitb+ZmLu/YZtshfn5FZDPBCcJFQRQ+8ih9DctOFvdLIKHH6uUQnq9yhFu0bec7znZ+xpAGmuqef5/wd8hAyEDIQMjAETHwP7nQl2WnYk4yAAAAAElFTkSuQmCC'

main_layout = create_main_layout(trade_goods, miracles, xcoord_max, xcoord_min, ycoord_max, ycoord_min, citymax, citymin, toggle_btn_off,user=logged_in)
main_window = sg.Window("Ika-Scrape",main_layout)

while True: #main loop
    
    event, values = main_window.read()
    #print(event, values)
    if event == sg.WIN_CLOSED or 'Cancel' in event: # if user closes window or clicks cancel
        break
    elif event == "Ok" and values[0]: #fetch ms
        main_window[f'main_menu'].update(visible=False)
        main_window[f'fetch_ms'].update(visible=True)
        main_window.read(10)
        fetch_military_hs(2000,main_window["fetching_progress"])
        main_window[f'fetch_ms'].update(visible=False)
        main_window[f'main_menu'].update(visible=True)
        main_window.read(10)
        
    elif event == "Ok" and values[1]: #refresh map
        main_window[f'main_menu'].update(visible=False)
        main_window[f'refresh_map'].update(visible=True)
        main_window.read(10)
        refresh_local_map(main_window['map_progress'])
        main_window[f'refresh_map'].update(visible=False)
        main_window[f'main_menu'].update(visible=True)
        main_window.read(10)
    elif event == "Ok" and values[2]: #search island
        main_window[f'main_menu'].update(visible=False)
        main_window[f'island_search'].update(visible=True)
        main_window[f'island_results'].update(visible=True)
        while event != 'Back':
            
            event, values = main_window.read()
            
            xcoord_min = values['xmin_slider']
            xcoord_max = values['xmax_slider']
            ycoord_min = values['ymin_slider']
            ycoord_max = values['ymax_slider']
            citymin = values['citymin_slider']
            citymax = values['citymax_slider']
            main_window.refresh()
            
            if 'Ok' in event:
                ml = main_window.find_element("island_res_ml")
                miracle_select = []
                for m in miracles:
                    if values[m]:
                        miracle_select.append(m)
                if(len(miracle_select) == 0):
                    miracle_select.append("none")
                    
                good_select = values['goods_combo']
                
                find_island(values,miracle_select,main_window,is_ally=is_ally)
                ml.print("--------------------------------------------------")
            elif event == '-TOGGLE-GRAPHIC-':  # if the graphical button that changes images
                main_window['-TOGGLE-GRAPHIC-'].metadata = not main_window['-TOGGLE-GRAPHIC-'].metadata
                main_window['-TOGGLE-GRAPHIC-'].update(image_data=toggle_btn_on if main_window['-TOGGLE-GRAPHIC-'].metadata else toggle_btn_off)
                if is_ally:
                    is_ally = 0
                else: is_ally = 1
                
        main_window[f'island_search'].update(visible=False)
        main_window[f'island_results'].update(visible=False)
        main_window[f'main_menu'].update(visible=True)
        main_window.read(10)
    elif event == "Ok" and values[3]: #ship_cook
        main_window[f'main_menu'].update(visible=False)
        main_window[f'ship_cook'].update(visible=True)
        main_window.read(10)
        cook_ships()
        main_window[f'ship_cook'].update(visible=False)
        main_window[f'main_menu'].update(visible=True)
        main_window.read(10)
    elif event == "Ok" and values[4]: #check_attacks
        main_window[f'main_menu'].update(visible=False)
        main_window[f'check_attacks'].update(visible=True)
        main_window.read(10)
        check_attacks()
        main_window[f'ship_cook'].update(visible=False)
        main_window[f'check_attacks'].update(visible=True)
        main_window.read(10)
main_window.close()  
driver.quit()
    

    


