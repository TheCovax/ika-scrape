
from ast import literal_eval
from bs4 import BeautifulSoup

from file_operations import write_to_file
from gui import print_island_res

import re

world_view_url = "https://s305-en.ikariam.gameforge.com/?view=worldmap_iso"
island_view_url = "https://s305-en.ikariam.gameforge.com/?view=island"


driver = None

def getDriver(maindriver):
    global driver
    driver = maindriver

def isl_island_tile(tag):
    return tag.name == 'div' and 'islandTile' in tag.get('class', [])

def isl_wonder_attr(tag):
    return 'wonder' in tag.get('class', [])

def isl_tradegood_attr(tag):
    return 'tradegood' in tag.get('class', [])


def extract_coordinates(island_name):
    # Pattern matches "Name [x:y]" where x and y can be one to three digits
    pattern = r'\[(\d{1,3}):(\d{1,3})\]'
    match = re.search(pattern, island_name)
    
    if match:
        x, y = int(match.group(1)), int(match.group(2))
        return x, y
    else:
        raise ValueError("Invalid island name format")

def parse_mapislands_from_source(full_source): #gets worldview with 22x22 islands (1/25th of the whole map) returns matrix of the islands where cells are lists: [name,miracle,goods,x,y,cities]
    soup = BeautifulSoup(full_source, 'html.parser')
    map = soup.find(id="map1")
    
    islands = [[0 for x in range(22)] for y in range(22)]
    
    for i in range(0,22):
        for j in range(0,22):
            tile_scheme_str = "tile_"+str(j)+"_"+str(i)
            island = map.find(isl_island_tile,id=tile_scheme_str)
            if island:
                island_data = []
                island_name = island.get("title")
                island_data.append(island_name)
                x = 0
                y = 0
                '''if island_name.index(":") - len(island_name) == -3: #[ :y]
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
                        y = int(island_name[-4:-1])'''
                x,y = extract_coordinates(island_name)

                
                island_wonder_tag = island.find(isl_wonder_attr) 
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
                
                island_good_tag = island.find(isl_tradegood_attr)
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

            vquinto = parse_mapislands_from_source(driver.page_source)
            
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
                i = literal_eval(i)
                if filters["citymin_slider"] <= int(i[5]) <= filters["citymax_slider"]:
                    if i[1] in miracle_select or "none" in miracle_select:
                        if i[2] in filters["goods_combo"] or "none" in filters["goods_combo"]:
                            if filters["xmin_slider"] <= i[3] <= filters["xmax_slider"]:
                                if filters["ymin_slider"] <= i[4] <= filters["ymax_slider"]:
                                    if i[6] >= is_ally:
                                        print_island_res(i,window)

def scrape_island(x_pos,y_pos):
    driver.get(island_view_url+"&xcoord={}&ycoord={}".format(x_pos,y_pos))
    res=[]

    page_source = driver.page_source
    soup = BeautifulSoup(page_source,'html.parser')
    island_soup = soup.find("div",{"id":"cities"})
    islandcity_re = re.compile(r"cityLocation[0-9][0-9]\Z|cityLocation[0-9]\Z")
    city_soup = island_soup.find_all("div",{"id":islandcity_re})

    cities = []
    for c in city_soup:
        if "city" in c['class']:
            current_city=[]
            cca = c.find("a",{"class":"island_feature_img"})
            ccl = re.findall("level([0-9][0-9]|[0-9])",str(c))[0]
            current_city.append(str(cca["href"]).split("=")[-1])
            current_city.append(str(cca["title"]))
            current_city.append(ccl)
            cities.append(current_city)
        #print(c,"\n")

    wonder_soup = island_soup.find("div",{"id":"islandwonder"})
    #wonder = wonder_soup["class"](r"wonder[0-9]")

