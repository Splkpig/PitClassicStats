import time
import discord
from discord import app_commands
from discord.ext import commands
from useful_things import file_functions
from useful_things import pit_functions
from useful_things import formatting_functions
from useful_things import discord_functions
from useful_things.api_functions import getInfo

# formatting for stored session
# {player}:{userID}:{xp}:{gold}:{kills}:{deaths}:{playtime}:{timeUNIX}


class sessions(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Create the command to start a session
    @app_commands.command(name='session-start', description="Start a new stat tracking session")
    async def start_session(self, interaction: discord.Interaction, player: str):
        """
        Args:
            player (str): A Minecraft username
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        data = getInfo(urlPP)

        if not data["success"]:
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:
            if file_functions.hasSession(interaction.user.id):
                embedFail = discord.Embed(title="Player already has a session", color=discord.Color.red())
                embedFail.add_field(name="", value="Use /session to view your in progression session or /session-end to end it")

                await interaction.response.send_message(embed=embedFail, ephemeral=True) # noqa
            else:
                doc = data["data"]["doc"]
                xp = doc.get("xp", 0)
                currentXP = data["data"]["xpProgress"]["displayCurrent"]
                gold = doc.get("lifetimeGold", 0)
                kills = doc.get("kills", 0)
                deaths = doc.get("deaths", 0)
                playtime = data["data"]["playtime"]

                prestige = len(data["data"].get("prestiges", [0])) - 1
                currentLevel = pit_functions.xpToLevel(prestige, currentXP)

                userID = interaction.user.id

                file_functions.startSession(player, userID, xp, gold, kills, deaths, playtime)

                embed = discord.Embed(title=f"Session started for [{formatting_functions.int_to_roman(prestige)}{currentLevel}] {data['data']['name']}", color=pit_functions.calcBracketColor(prestige))
                embed.add_field(name="", value=f"Session started at <t:{int(time.time())}:f>", inline=False)
                embed.add_field(name="", value=f"This session will expire <t:{int(time.time()) + 86400}:R>", inline=False)
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")
                embed.set_footer(text=discord_functions.footerDateGen())

                file_functions.checkSessions()

                await interaction.response.send_message(embed=embed) # noqa

    # Create the command to the view the stats of a current session
    @app_commands.command(name="session", description="View your current session's stats")
    async def session(self, interaction: discord.Interaction):
        infoString = file_functions.viewSession(interaction.user.id)

        if infoString is None:
            embedFail = discord.Embed(title="Session not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa
        else:
            parts = infoString.split(":")
            player = parts[0]
            userID = parts[1]
            xp = int(parts[2])
            gold = int(parts[3])
            kills = int(parts[4])
            deaths = int(parts[5])
            playtime = int(parts[6])
            timeUNIX = int(parts[7])

            urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
            data = getInfo(urlPP)

            doc = data["data"]["doc"]
            xp = doc.get("xp", 0) - xp
            gold = doc.get("lifetimeGold", 0) - gold
            kills = doc.get("kills", 0) - kills
            deaths = doc.get("deaths", 0) - deaths
            if deaths == 0:
                kdr = kills
            else:
                kdr = kills / deaths
            playtime = data["data"]["playtime"] - playtime

            prestige = len(data["data"].get("prestiges", [0])) - 1
            currentXP = data["data"]["xpProgress"]["displayCurrent"]
            currentLevel = pit_functions.xpToLevel(prestige, currentXP)

            embed = discord.Embed(title=f"Session for [{formatting_functions.int_to_roman(prestige)}{currentLevel}] {data['data']['name']}", color=pit_functions.calcBracketColor(prestige))
            embed.add_field(name="<:xpbottle:1245974825865056276> XP Grinded:", value=f"{formatting_functions.add_commas(xp)}", inline=False)
            embed.add_field(name="<:goldingot:1247391882968043652> Gold Grinded:", value=f"{formatting_functions.add_commas(gold)}", inline=False)
            embed.add_field(name="<:ironsword:1247392632129323080> Kills:", value=formatting_functions.add_commas(kills), inline=False)
            embed.add_field(name="<:ironchestplate:1247719811857907762> Deaths:", value=formatting_functions.add_commas(deaths), inline=False)
            embed.add_field(name="<:diamondsword:1247404240016773231> KDR:", value=f"{kdr:.2f}", inline=False)
            embed.add_field(name="<a:minecraftclock:1247400003786510479> Time Played:", value=formatting_functions.format_playtime(playtime), inline=False)
            embed.add_field(name="<:wheat:1248124503255420928> Rates:", value=f"{int(xp / (playtime / 60))} XP per hour\n{int(gold / (playtime / 60))} Gold per hour", inline=False)
            embed.add_field(name=":regional_indicator_i: Session Info:", value=f"Session started at <t:{timeUNIX}:f>\nThis session will expire <t:{timeUNIX + 86400}:R>", inline=False)
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")
            embed.set_footer(text=discord_functions.footerDateGen())

            file_functions.checkSessions()

            await interaction.response.send_message(embed=embed) # noqa

    # Create the command to end a session
    @app_commands.command(name="session-end", description="Stop your current session")
    async def end_session(self, interaction: discord.Interaction):
        infoString = file_functions.viewSession(interaction.user.id)

        if infoString is None:
            embedFail = discord.Embed(title="Session not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa
        else:
            parts = infoString.split(":")
            player = parts[0]
            userID = parts[1]
            xp = int(parts[2])
            gold = int(parts[3])
            kills = int(parts[4])
            deaths = int(parts[5])
            playtime = int(parts[6])
            timeUNIX = int(parts[7])

            urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
            data = getInfo(urlPP)

            doc = data["data"]["doc"]
            xp = doc.get("xp", 0) - xp
            gold = doc.get("lifetimeGold", 0) - gold
            kills = doc.get("kills", 0) - kills
            deaths = doc.get("deaths", 0) - deaths

            if deaths == 0:
                kdr = kills
            else:
                kdr = kills / deaths

            playtime = data["data"]["playtime"] - playtime

            prestige = len(data["data"].get("prestiges", [0])) - 1
            currentXP = data["data"]["xpProgress"]["displayCurrent"]
            currentLevel = pit_functions.xpToLevel(prestige, currentXP)

            file_functions.endSession(interaction.user.id)

            embed = discord.Embed(title=f"End of session for [{formatting_functions.int_to_roman(prestige)}{currentLevel}] {data['data']['name']}", color=pit_functions.calcBracketColor(prestige))
            embed.add_field(name="<:xpbottle:1245974825865056276> XP Grinded:", value=f"{formatting_functions.add_commas(xp)}", inline=False)
            embed.add_field(name="<:goldingot:1247391882968043652> Gold Grinded:", value=f"{formatting_functions.add_commas(gold)}", inline=False)
            embed.add_field(name="<:ironsword:1247392632129323080> Kills:", value=formatting_functions.add_commas(kills), inline=False)
            embed.add_field(name="<:ironchestplate:1247719811857907762> Deaths:", value=formatting_functions.add_commas(deaths), inline=False)
            embed.add_field(name="<:diamondsword:1247404240016773231> KDR:", value=f"{kdr:.2f}", inline=False)
            embed.add_field(name="<a:minecraftclock:1247400003786510479> Time Played:", value=formatting_functions.format_playtime(playtime), inline=False)
            embed.add_field(name="<:wheat:1248124503255420928> Rates:", value=f"{int(xp / (playtime / 60))} XP per hour\n{int(gold / (playtime / 60))} Gold per hour", inline=False)
            embed.add_field(name=":regional_indicator_i: Session Info:", value=f"Session started at <t:{timeUNIX}:f>\nThis session ended at <t:{int(time.time())}:f>", inline=False)
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")

            file_functions.checkSessions()

            await interaction.response.send_message(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(sessions(client))
