import ikaWorld
import selenium
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless=new")
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = selenium.webdriver.Chrome(options=options)
world_view_url = "https://s305-en.ikariam.gameforge.com/?view=worldmap_iso"
driver.get(world_view_url)
driver.add_cookie({"name": "ikariam", "value": '142918_eec6df3defb8795ebe742f26de1f6f95'})

ikaWorld.getDriver(driver)

ikaWorld.scrape_island(66,81)
