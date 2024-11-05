import datetime
from bs4 import BeautifulSoup

import discord
from discord import app_commands
from discord.ext import tasks


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pytz, random, sys
import time as T

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)
        self.generalViewInterface = None
        self.generalViewStr = ""

    async def setup_hook(self):
        await self.tree.sync()
        self.update_message.start()

    async def on_ready(self):
        print(f'Logged in as {self.user.name} ({self.user.id})')
        print('------')

    @tasks.loop(seconds=30+random.uniform(0,60))
    async def update_message(self):
        try:
            if self.generalViewInterface:
                # Update the generalViewStr with new data
                await self.fetch_general_view()
                time = datetime.datetime.now(tz=pytz.timezone("Europe/Budapest")).strftime("%Y-%m-%d %H:%M:%S")
                print(f'Updating message at {time}')
                await self.generalViewInterface.edit(content=f"\n\n***General view: Attacks on alliance***\t({time})\n" + "```" + self.generalViewStr + "```")
        except Exception as e:
            print(e)
            T.sleep(5)
            if self.generalViewInterface:
                # Update the generalViewStr with new data
                await self.fetch_general_view()
                time = datetime.datetime.now(tz=pytz.timezone("Europe/Budapest")).strftime("%Y-%m-%d %H:%M:%S")
                print(f'Updating message at {time}')
                await self.generalViewInterface.edit(content=f". \n***General view: Attacks on alliance***\t({time})\n" + "```" + self.generalViewStr + "```")
        

    async def fetch_general_view(self):
        self.generalViewStr = ""
        cityIdStr = "87355"
        embassyPosStr = "13"
        driver.get(city_view_url.replace("city", f"embassyGeneralAttacksToAlly&cityId={cityIdStr}&position={embassyPosStr}&activeTab=tabEmbassy"))
        driver.find_element(By.ID, "embassyGeneralAttacksToAlly")
        embassyTable = driver.find_element(By.CLASS_NAME, "embassyTable").find_elements(By.TAG_NAME, "tr")
        for idx, row in enumerate(embassyTable):
            if idx > 0:
                self.generalViewStr += getGeneralViewRow(row.get_attribute("innerHTML")) + "\n"

def getGeneralViewRow(inner_html):
    soup = BeautifulSoup(inner_html, 'html.parser')

    cells = soup.findAll("td")
    rowString = "| "
    for c in cells:
        rowString = rowString + str(c.getText(strip=True)).strip().replace("  ","") + " | "

    print(rowString)
    return rowString


TOKEN = input("add discord token:")
intents = discord.Intents.all()
client = MyClient(intents=intents)

world_view_url = "https://s305-en.ikariam.gameforge.com/?view=worldmap_iso"
city_view_url = "https://s305-en.ikariam.gameforge.com/?view=city"
if len(sys.argv) > 1:
    ika_cookie = sys.argv[1]
else:
    ika_cookie = "142918_2617d359f2ee0c9b8106ab4b3cb06b4a"

options = Options()
options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get(world_view_url)
driver.add_cookie({"name": "ikariam", "value": ika_cookie})


@client.tree.command(name='general-view')
async def general_view(interaction: discord.Interaction):
    await interaction.response.defer()
    await client.fetch_general_view()
    
    await interaction.followup.send(" .\nGeneral view: Attacks on alliance:\n" + "```" + client.generalViewStr + "```")
    client.generalViewInterface = await interaction.original_response()


client.run(TOKEN)