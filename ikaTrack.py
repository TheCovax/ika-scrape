
from bs4 import BeautifulSoup

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


