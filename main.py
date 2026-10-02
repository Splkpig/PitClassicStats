import json
import discord
from discord.ext import commands

# Create a client with the Cog commands from the files
class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

        self.commandsList = ["commands.pitpanda_signatures", "commands.prestige_calculations", "commands.fun", "commands.basic", "commands.stats", "commands.map_quests", "commands.leaderboards", "commands.session_tracking", "commands.upgrades", "commands.discord_features"]

    async def setup_hook(self):
        for ext in self.commandsList:
            await self.load_extension(ext)
            print(f"Synced {ext.title()}")

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        synced = await self.tree.sync()

# Grab bot key and start a session
with open("../PitStats/tokens_and_keys/TOKEN.json", 'r') as f:
    data = json.load(f)
    TOKEN = data['TOKEN']

client = Client()

client.run(TOKEN)
