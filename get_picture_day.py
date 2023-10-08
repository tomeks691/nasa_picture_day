import requests
import discord
import os
from deep_translator import GoogleTranslator
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
def send_to_discord(date, explanation, photo_url):
    load_dotenv(find_dotenv())
    discord_token = os.environ.get("DISCORD_BOT_TOKEN")
    channel_id = int(os.environ.get("DISCORD_CHANNEL_ID"))

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)

        if channel:
            embed = discord.Embed(title="NASA Astronomy Picture of the Day", url=photo_url, description=f"{date}\n{explanation}")
            embed.set_image(url=photo_url)
            await channel.send(embed=embed)

            await client.close()

    client.run(discord_token)

def translate_to_polish(text):
    translator = GoogleTranslator(source='auto', target='pl')
    return translator.translate(text)


api = os.environ.get("nasa_api")
r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api}")
photo_url = r.json()["url"]
explanation = translate_to_polish(r.json()["explanation"])
date = r.json()["date"]
send_to_discord(date, explanation, photo_url)
