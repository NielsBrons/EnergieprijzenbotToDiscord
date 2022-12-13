import os
import discord
import requests
import json
from discord.ext import tasks
from dotenv import load_dotenv
from datetime import datetime

#f = open('test.json')

#data = json.load(f)




if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    CHANNEL = os.getenv('CHANNEL')
    API_USER = os.getenv('API_USER')
    API_KEY = os.getenv('API_KEY')

    response = requests.get(f'https://api.energieprijzenbot.nl/energy/api/v1.0/ha?user_id={API_USER}&api_key={API_KEY}')

    data = response.json()

    intents=discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    async def send_prices():

        now = datetime.now()
        t = now.replace(second=0, microsecond=0, minute=0)

        channel = client.get_channel(int(CHANNEL))
        
        for electric in data['data']['e']:
            if electric['datetime'] == t.isoformat():
                all_in_e = round(electric['all_in_price'], 3)

        for gas in data['data']['g']:
            if gas['datetime'] == t.isoformat():
                all_in_g = round(gas['all_in_price'], 3)

        await channel.send(f'{now.hour}:00 all-in prices: electricity :zap:: {all_in_e}, gas :fire:: {all_in_g}')
        await client.close()

    @client.event
    async def on_ready():
        await send_prices()


    client.run(TOKEN)