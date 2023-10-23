import time
import os
import ast

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import PySimpleGUI as sg

def is_island_tile(tag):
    return tag.name == 'div' and 'islandTile' in tag.get('class', [])

def is_wonder_attr(tag):
    return 'wonder' in tag.get('class', [])

def is_tradegood_attr(tag):
    return 'tradegood' in tag.get('class', [])

def parse_islands_from_source(full_source): #gets worldview with 22x22 islands (1/25th of the whole map) returns matrix of the islands where cells are lists: [name,miracle,goods,x,y,cities]
    soup = BeautifulSoup(full_source, 'html.parser')
    map = soup.find(id="map1")
    
    islands = [[0 for x in range(22)] for y in range(22)]
    
    for i in range(0,22):
        for j in range(0,22):
            tile_scheme_str = "tile_"+str(j)+"_"+str(i)
            island = map.find(is_island_tile,id=tile_scheme_str)
            if island:
                island_data = []
                island_name = island.get("title")
                island_data.append(island_name)
                x = 0
                y = 0
                if island_name.index(":") - len(island_name) == -3: #[ :y]
                    if island_name[-6:-5] == "[":                   #[xx:y]
                        x = int(island_name[-5:-3])
                        y = int(island_name[-2:-1])
                    elif island_name[-5:-4] == "[":                 #[x:y]
                        x = int(island_name[-4:-3])
                        y = int(island_name[-2:-1])
                    elif island_name[-7:-6] == "[":                 #[xxx:y]
                        x = int(island_name[-6:-3])
                        y = int(island_name[-2:-1])    
                        
                elif island_name.index(":") - len(island_name) == -4: #[ :yy]
                    if island_name[-7:-6] == "[":                     #[xx:yy]
                        x = int(island_name[-6:-4])
                        y = int(island_name[-3:-1])
                    elif island_name[-6:-5] == "[":                   #[x:yy]
                        x = int(island_name[-5:-4])
                        y = int(island_name[-3:-1])
                    elif island_name[-8:-7] == "[":                   #[xxx:yy]
                        x = int(island_name[-7:-4])
                        y = int(island_name[-3:-1])
                    
                        
                elif island_name.index(":") - len(island_name) == -5: #[ :yyy]
                    if island_name[-8:-7] == "[":                     #[xx:yyy]
                        x = int(island_name[-6:-5])
                        y = int(island_name[-4:-1])
                    elif island_name[-7:-6] == "[":                   #[x:yyy]
                        x = int(island_name[-7:-5])
                        y = int(island_name[-4:-1])
                    elif island_name[-9:-8] == "[":                   #[xxx:yyy]
                        x = int(island_name[-8:-5])
                        y = int(island_name[-4:-1])
                
                
                island_wonder_tag = island.find(is_wonder_attr) 
                island_wonder = island_wonder_tag.get('class',[])[1]
                if island_wonder == "wonder1":
                    island_wonder = "Hephaistos' Forge"
                elif island_wonder == "wonder2":
                    island_wonder = "Hades' Holy Grove"
                elif island_wonder == "wonder3":
                    island_wonder = "Demeter's Gardens"
                elif island_wonder == "wonder4":
                    island_wonder = "Temple of Athene"
                elif island_wonder == "wonder5":
                    island_wonder = "Temple of Hermes"
                elif island_wonder == "wonder6":
                    island_wonder = "Ares' Stronghold"
                elif island_wonder == "wonder7":
                    island_wonder = "Temple of Poseidon"
                elif island_wonder == "wonder8":
                    island_wonder = "Colossus"
                    
                island_data.append(island_wonder)
                
                island_good_tag = island.find(is_tradegood_attr)
                island_good = island_good_tag.get('class',[])[1]
                
                if island_good == "tradegood1":
                    island_good = "Wine"
                elif island_good == "tradegood2":
                    island_good = "Marble"
                elif island_good == "tradegood3":
                    island_good = "Crystal Glass"
                elif island_good == "tradegood4":
                    island_good = "Sulphur"
                    
                island_data.append(island_good)
                
                island_data.append(x)
                island_data.append(y)
                
                island_city_nr = island.find(class_ = "cities")
                island_data.append(island_city_nr.text)
                
                owner = island.find(class_ = "ownerState") 
                owner = owner.get('class',[])
                
                if len(owner) == 2:
                    if owner[1] == "own":
                        island_data.append(2)
                    elif owner[1] == "ally":
                        island_data.append(1)
                    else:
                        island_data.append(0)
                else:
                    island_data.append(0)
                
                
                
                islands[i][j] = island_data
            else:
                islands[i][j] = "x"
    
    return islands

def parse_ms_from_source(full_source):
    res = ""
    
    soup = BeautifulSoup(full_source, 'html.parser')
    hs_tab = soup.find(id="tab_highscore")   
    table = hs_tab.find(class_="table01 highscore")
    rows = table.find_all("tr")
    
    place = ""
    player = ""
    alliance = ""
    points = ""

    for r in rows:
        places = r.find_all("td",class_="place")
        players = r.find_all(class_="avatarName")
        alliances = r.find_all(class_="allyLink")
        pointss = r.find_all("td",class_="score")
        
        for i in places:
            place = i.get_text(strip=True)
        for i in players:
            player = i.get_text(strip=True)
        for i in alliances:
            alliance = i.get_text(strip=True)
        for i in pointss:
            points = i.get_text(strip=True)
        
        if player == "":
            continue 
        
        res += place + ';' + player +';' + alliance +';' + points + "\n"
        
    return res.strip()

def write_to_file(str,filename="tmp.txt"):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str)
    file.close()

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

def refresh_local_map(progressbar):
    
    islands = [["x" for x in range(1,101)] for y in range(1,101)]
    
    island_x_param = "&islandX="
    island_y_param = "&islandY="
    x_coord = 11
    progress = 0
    
    islandstr = ''
    
    while x_coord < 100:
        y_coord = 11
        while y_coord < 100:
            driver.get(world_view_url+island_x_param+str(x_coord)+island_y_param+str(y_coord))

            vquinto = parse_islands_from_source(driver.page_source)
            
            progress += 1
            print("Scanning Islands",progress*100/25 ,"%\n")
            progressbar.UpdateBar(progress+1)
            
            for j in vquinto:
                for i in j:
                    if i != "x":
                        islands[i[4]-1][i[3]-1] = i
            y_coord += 22
        x_coord+=22
    
    for x in islands:
        for y in x:
            islandstr += str(y) + ";"
        islandstr += "\n" 
    
    write_to_file(islandstr,"island.txt")

def find_island(filters,miracle_select, window, is_ally = 0):
    
    f = open("island.txt","r")
    
    islands = [["x" for x in range(1,101)] for y in range(1,101)]
    
    
    
    for row in islands:
        row_str = f.readline()
        row = row_str.split(";")
        for i in row:
            if len(i) >1 :
                i = ast.literal_eval(i)
                if filters["citymin_slider"] <= int(i[5]) <= filters["citymax_slider"]:
                    if i[1] in miracle_select or "none" in miracle_select:
                        if i[2] in filters["goods_combo"] or "none" in filters["goods_combo"]:
                            if filters["xmin_slider"] <= i[3] <= filters["xmax_slider"]:
                                if filters["ymin_slider"] <= i[4] <= filters["ymax_slider"]:
                                    if i[6] >= is_ally:
                                        sg.cprint_set_output_destination(window,'island_res_ml')
                                        sg.cprint(i[0],i[1],i[2],i[5],sep=", ")
    
def ms_compare(): #TODO add ms compare feature
    all_csv = []

    if True:
        players = []
        
        for (root,dirs,files) in os.walk('.',topdown=True):
            for f in files:
                if f[-4:] ==".csv":
                    all_csv.append(f)
        
        
        
            for file in all_csv:
                with open(file, 'r', encoding='utf-8') as f:
                    f.readline()
                    csv_str = f.read()

world_view_url = "https://s305-en.ikariam.gameforge.com/?view=worldmap_iso"
highscore_url = "https://s305-en.ikariam.gameforge.com/index.php?view=highscore"

highscore_military_score_param = "&highscoreType=army_score_main"
highscore_offset_param = set_offset_param(0)

lobby_url = "https://lobby.ikariam.gameforge.com/en_GB"

url = world_view_url

options = Options()
options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)


modeselect_layout  = [  
    [sg.Text('Select authentication mode:')],
    [sg.Radio(f'Cookie', 1)],
    [sg.Radio(f'Login with email and password (BETA)', 1)    ],
    [sg.Button('Select'), sg.Button('Cancel')]  
]

cookie_layout = [
    [sg.Text("Please provide a valid 'ikariam' cookie:"), sg.InputText()],
    [sg.Button('Ok'), sg.Button('Cancel')]  
]

email_layout = [
    [sg.Text("Email:"), sg.InputText()],
    [sg.Text("Password:"), sg.InputText()],
    [sg.Button('Ok'), sg.Button('Cancel')]  
]

w84auth_layout = [
    [sg.Text("Authenticating, Please wait...")]
]

login_layout = [
    [sg.Column(modeselect_layout,visible=True, key="login"),
     sg.Column(cookie_layout,visible=False, key="cookie"),
     sg.Column(email_layout,visible=False, key="email"),
     sg.Column(w84auth_layout,visible=False, key="w84auth")]
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

main_menu_layout = [
    [sg.Text("You are logged in as "+logged_in)],
    [sg.Text("")],
    [sg.Text("Please choose from the following options what you would like to do.")],
    [sg.Radio(f"Fetch top 2000 Military Scores", 1)],
    [sg.Radio(f'Refresh local map', 1)    ],
    [sg.Radio(f'Search Island', 1)    ],
    [sg.Button('Ok'), sg.Button('Cancel')] 
]

fetch_ms_layout = [
    [sg.Text("Fetching Military scores...")],
    [sg.ProgressBar(2000, orientation='h', size=(20,20), key='fetching_progress')]
]

refresh_map_layout = [
    [sg.Text("Refreshing local map...")],
    [sg.ProgressBar(25, orientation='h', size=(20,20), key='map_progress')]
]

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

island_search_layout = [
    [sg.Combo(trade_goods, default_value="none",enable_events=True,s=(20,5),k='goods_combo')],
    [sg.Checkbox(miracles[i],key=miracles[i]) for i in range(0,2)],
    [sg.Checkbox(miracles[i],key=miracles[i]) for i in range(2,5)],
    [sg.Checkbox(miracles[i],key=miracles[i]) for i in range(5,8)],
    [sg.Text("X coordinate min and max"), sg.Slider((1,xcoord_max),default_value=xcoord_min, orientation='h', s=(10,15),k='xmin_slider'), sg.Slider((xcoord_min,100),default_value=xcoord_max, orientation='h', s=(10,15),k='xmax_slider')],
    [sg.Text("Y coordinate min and max"), sg.Slider((1,ycoord_max),default_value=ycoord_min, orientation='h', s=(10,15),k='ymin_slider'), sg.Slider((ycoord_min,100),default_value=ycoord_max, orientation='h', s=(10,15),k='ymax_slider')],
    [sg.Text("Minimum and maximum number of cities"), sg.Slider((0,citymax),default_value=citymin, orientation='h', s=(10,15),k='citymin_slider'),sg.Slider((citymin,17),default_value=citymax, orientation='h', s=(10,15),k='citymax_slider')],
    [sg.Text("Show only ally cities"), sg.Button(image_data=toggle_btn_off, key='-TOGGLE-GRAPHIC-', button_color=(sg.theme_background_color(), sg.theme_background_color()),border_width=0, metadata=False)],
    [sg.Button('Ok'), sg.Button('Back')] 
]

island_results_layout = [
    [sg.Text("Island Name, Miracle, Trade Good, Number of cities")],
    [sg.Multiline(size=(50,15),k='island_res_ml')]
]

main_layout = [
    [sg.Column(main_menu_layout,visible=True,key='main_menu'),
     sg.Column(fetch_ms_layout,visible=False, key='fetch_ms'),
     sg.Column(refresh_map_layout, visible=False, key='refresh_map'),
     sg.Column(island_search_layout, visible=False, key='island_search'),
     sg.Column(island_results_layout, visible=False, key='island_results'),
     ]
]

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
                #print(event,values)
                for m in miracles:
                    if values[m]:
                        miracle_select.append(m)
                        #print(m)
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
                #print(is_ally)
                
        main_window[f'island_search'].update(visible=False)
        main_window[f'island_results'].update(visible=False)
        main_window[f'main_menu'].update(visible=True)
        main_window.read(10)
        
     
main_window.close()  
driver.quit()
    

    


