import discord
from discord.ext import tasks, commands
import requests
import os

# Configuración
TOKEN = 'MTUwMTgwOTgxMTUwMTc0ODIzNA.GnSV-i.eXx0roM-3Ym10TZWEYMVqrOgLUMYYtQ9PtOEZE'
CHANNEL_ID = 1501803615029821451  # ID del canal de Discord donde avisará
YT_API_KEY = 'AIzaSyBFbIsKDGIqi4iVacdUh85GgzDmKrPrIKg'
YT_CHANNEL_ID = 'UCBi2l8X8-5UyWbP4ESoHltg'


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@tasks.loop(minutes=30)
async def check_youtube():
    # Pedimos a YouTube el último video
    url = f"https://www.googleapis.com/youtube/v3/search?key={YT_API_KEY}&channelId={YT_CHANNEL_ID}&part=snippet,id&order=date&maxResults=1"
    response = requests.get(url).json()
    
    if "items" in response and len(response["items"]) > 0:
        latest_video_id = response['items'][0]['id']['videoId']
        
        # Sistema de memoria para no repetir
        last_notified_id = ""
        if os.path.exists("last_video.txt"):
            with open("last_video.txt", "r") as f:
                last_notified_id = f.read().strip()

        if latest_video_id != last_notified_id:
            channel = bot.get_channel(CHANNEL_ID)
            video_url = f"https://www.youtube.com/watch?v={latest_video_id}"
            
            # Mensaje personalizado para tu comunidad
            await channel.send(f"¡Atención @everyone! Hay un nuevo video en el canal: {video_url}")
            
            with open("last_video.txt", "w") as f:
                f.write(latest_video_id)

@bot.event
async def on_ready():
    print(f'El bot de Gods Beloved está online como {bot.user}')
    check_youtube.start()

bot.run(TOKEN)
