import time
import os
import ast

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

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

def fetch_military_hs(top):
    full_data = "Position;Player Name;Alliance;Points\n"

    print("Fetching data:")
    for i in range(0,top,50):
        print("\tfetching positions "+str(i+1)+"-"+str(i+50)+"...")
            
        params=highscore_military_score_param + set_offset_param(i)
        driver.get(highscore_url+params)
            
        full_data+=(parse_ms_from_source(driver.page_source) + "\n") 
            
    print("Fetching Done!")
    out_file = str(time.localtime().tm_year)+"_"+str(time.localtime().tm_mon)+"_"+str(time.localtime().tm_mday) +"_"+str(time.localtime().tm_hour) +"_"+str(time.localtime().tm_min)+".csv"

    write_to_file(full_data,out_file)

def refresh_local_map():
    
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

def find_island(miracle_filter="none", tgood_filter="none", x_min_filter = 1, x_max_filter=100, y_min_filter=1, y_max_filter=100, max_cities_filter = 15, min_cities_filter = 1):
    
    f = open("island.txt","r")
    
    islands = [["x" for x in range(1,101)] for y in range(1,101)]
    
    
    
    for row in islands:
        row_str = f.readline()
        row = row_str.split(";")
        for i in row:
            if len(i) >1 :
                i = ast.literal_eval(i)
                if min_cities_filter <= int(i[5]) <= max_cities_filter:
                    if i[1] == miracle_filter or miracle_filter == "none":
                        if i[2] == tgood_filter or tgood_filter == "none":
                            if x_min_filter <= i[3] <= x_max_filter:
                                if y_min_filter <= i[4] <= y_max_filter:
                                    print(i[0],i[1],i[2],i[5],sep=", ")
    
    

world_view_url = "https://s305-en.ikariam.gameforge.com/?view=worldmap_iso"
highscore_url = "https://s305-en.ikariam.gameforge.com/index.php?view=highscore"

highscore_military_score_param = "&highscoreType=army_score_main"
highscore_offset_param = set_offset_param(0)

lobby_url = "https://lobby.ikariam.gameforge.com/en_GB"

url = world_view_url



all_csv = []

if True:
    players = []
    
    for (root,dirs,files) in os.walk('.',topdown=True):
        print("Files: ")
        for f in files:
            if f[-4:] ==".csv":
                all_csv.append(f)
    
    
    
        for file in all_csv:
            with open(file, 'r', encoding='utf-8') as f:
                f.readline()
                csv_str = f.read()

options = Options()
#options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

while True:
    auth_mode = input("select authentication mode:\n(1) Cookie\n(2) Login (email + password) (BETA)\n___________________\n:")
    if auth_mode == "1":
        ika_cookie = input("Please provide a valid 'ikariam' cookie:")
        
        driver.get(url)
        driver.add_cookie({"name": "ikariam", "value": ika_cookie})
        driver.refresh()
        
        print("Authenticating...")
        break
    elif auth_mode == "2":
       
        
        driver.get(lobby_url)
        
        time.sleep(2)
        
        login_tab = driver.find_element(By.XPATH, "//ul[@class='tabsList']/li[text()='Log in']")
        register_tab = driver.find_element(By.XPATH, "//ul[@class='tabsList']/li[text()='Register']")
        login_tab.click()
        
        logintab = driver.find_element(By.ID, "loginTab")
        email_field = logintab.find_element(By.NAME,"email")
        pw_field = logintab.find_element(By.NAME,"password")
        
        email_in = input("Email:")
        password_in = input("Password:")
        
        email_field.send_keys(email_in)
        pw_field.send_keys(password_in)
        
        time.sleep(1)
        
        driver.find_element(By.CLASS_NAME, "button-primary").click()
        
        time.sleep(3)
        
        driver.get(lobby_url+"/accounts")
        
        time.sleep(3)
        
        pangaia5 = driver.find_element(By.XPATH, "//div[contains(text(), 'Pangaia 5')]")
        
        time.sleep(1)
        pangaia5.click() 
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "btn-primary").click()
        
        print("Authenticating...")
        break
    else:
        print("unknown command")
        
        
    




input("wait")

logged_in_as = BeautifulSoup(driver.page_source, 'html.parser').find(class_="avatarName")
if type(logged_in_as) == "NoneType":
    print("\n!!!Authentication failed!!!")
else:
    print(type(logged_in_as))
    logged_in_as = logged_in_as.find("a",class_="noViewParameters")["title"]

if logged_in_as == "None":
    
    print("\n!!!Authentication failed!!!")
    
else: print("\nProgram logged in as: "+logged_in_as)

while True:
    print("Please choose from the following options what you would like to do.")
    
    options = [
        "(1) Fetch top 2000 Military Scores\n",
        "(2) Refresh local map\n",
        "(3) Search Island\n",
        "(q - quit) Quit program\n"
    ]
    
    for o in options:
        print(o)
    print("___________________\n:")
    
    
    select = input()
    if select == "1":
        #get military scores
        fetch_military_hs(2000)
        
    elif select == "2":
        refresh_local_map()
    
    elif select == "3":
        miracle_filter = "none"
        tradegood_filter = "none"
        x_filter = (1,100)
        y_filter = (1,100)
        cities_filter = (0,17)
        
        miracles = [
            "Hephaistos' Forge",
            "Hades' Holy Grove",
            "Demeter's Gardens",
            "Temple of Athene",
            "Temple of Hermes",
            "Ares' Stronghold",
            "Temple of Poseidon",
            "Colossus",
            "none"
        ]
        
        trade_goods = [
            "Wine",
            "Marble",
            "Crystal Glass",
            "Sulphur",
            "none"
        ]
        
        print("What miracle would you like to search for?")
        for idx, miracle in enumerate(miracles):
            print("("+str(idx+1)+") "+miracle)
        miracle_select = int(input(":"))
            
        print("What luxury good would you like to search for?")
        for idx, good in enumerate(trade_goods):
            print("("+str(idx+1)+") "+good)
        good_select = int(input(":"))
        
        
        
        
        find_island(miracles[miracle_select-1],trade_goods[good_select-1],45,70,30,55,15,0)
        

    
    
    elif select == "quit" or select =="q":
        print("Quitting program...")
        driver.quit()
        exit()
    
    else:
        print("unknown command.")
    
    



