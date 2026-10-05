import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from useful_things.api_functions import getInfo
from useful_things import pit_functions
from useful_things import formatting_functions
from useful_things.discord_functions import footerDateGen
from useful_things.pit_functions import calcBracketColor, calculateXPForLevel


class compare(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Create the command to show an overview of a player's stats
    @app_commands.command(name="overview", description='Shows an overview of a player\'s stats')
    async def overview(self, interaction: discord.Interaction, player: str):
        """
        Args:
            player (str): A Minecraft username
        """
        await interaction.response.defer()

        player = player.strip()
        url: str = f"https://classic.pitpal.rocks/remake-api/api/player/{player}"
        data = await asyncio.to_thread(getInfo, url)

        if data.get("message", "") != "":
            embedFail = discord.Embed(title=f"{player} not found", color=discord.Color.red())

            await interaction.followup.send(embed=embedFail)  # noqa

        else:
            player_data = data["data"]["player"]
            prestige = player_data["prestige"]
            level = player_data["level"]
            current_xp = player_data["total_xp"]
            gold = int(player_data.get("cash_earned", 0))
            kills = player_data.get("kills", 0)
            deaths = player_data.get("deaths", 0)
            kdr = str(kills / deaths) if deaths != 0 else kills
            kdr = kdr[:kdr.index(".") + 3] if "." in kdr else kdr
            timeplayed = player_data.get("playtime_minutes", 0)
            timeplayed = formatting_functions.format_playtime(int(timeplayed))

            embed = discord.Embed(title=f"Player Stats for [{formatting_functions.int_to_roman(prestige)}{level}] {player_data['ign']}", color=calcBracketColor(int(prestige)))
            embed.add_field(name=f"{pit_functions.getBracketColorEmoji(prestige)} Prestige & Level:", value=f"[{formatting_functions.int_to_roman(prestige)}{level}]", inline=False)
            embed.add_field(name="<:xpbottle:1245974825865056276> Lifetime XP:", value=f"{formatting_functions.add_commas(current_xp)} XP", inline=False)
            embed.add_field(name="<:goldingot:1247391882968043652> Lifetime Gold:", value=f"{formatting_functions.add_commas(gold)} G", inline=False)
            embed.add_field(name="<:ironsword:1247392632129323080> Kills:", value=f"{formatting_functions.add_commas(kills)}", inline=False)
            embed.add_field(name="<:ironchestplate:1247719811857907762> Deaths:", value=f"{formatting_functions.add_commas(deaths)}", inline=False)
            embed.add_field(name="<:diamondsword:1247404240016773231> KDR:", value=f"{kdr}", inline=False)
            embed.add_field(name="<a:minecraftclock:1247400003786510479> Time Played:", value=f"{timeplayed}", inline=False)
            embed.set_footer(text=footerDateGen())
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{player_data['uuid']}?format=webp")

            await interaction.followup.send(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(compare(client))
