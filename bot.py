import os
import requests
import discord
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = "https://player-api-production.up.railway.app/status"

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced!")

client = Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.tree.command(name="status", description="Shows the current player count")
async def status(interaction: discord.Interaction):
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        online = data.get("online", 0)

        await interaction.response.send_message(
            f"🟢 **Players Online:** {online}"
        )

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Couldn't contact the player API.\n```{e}```",
            ephemeral=True
        )

client.run(TOKEN)
