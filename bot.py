import os
import requests
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = "https://YOUR-RAILWAY-URL/status"

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)


def get_online():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("online", "Unknown")
    except Exception:
        return "Offline"


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def online(ctx):
    online_players = get_online()
    await ctx.send(f"🟢 Players Online: **{online_players}**")

print("TOKEN:", TOKEN)
bot.run(TOKEN)
