import ikaWorld
import selenium
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless=new")
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = selenium.webdriver.Chrome(options=options)
world_view_url = "https://s305-en.ikariam.gameforge.com/?view=worldmap_iso"
driver.get(world_view_url)
driver.add_cookie({"name": "ikariam", "value": '142918_5107f48d66527cbc8e314804b2238f7e'})

ikaWorld.getDriver(driver)

ikaWorld.scrape_island(67,83)
#ikaWorld.scrape_player(134637)