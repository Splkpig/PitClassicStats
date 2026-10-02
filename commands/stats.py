import discord
from discord.ext import commands
from discord import app_commands
from useful_things.api_functions import getInfo
from useful_things import pit_functions
from useful_things import formatting_functions
from useful_things.discord_functions import footerDateGen
from useful_things.pit_functions import calcBracketColor


class compare(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Create the command to compare the stats of two players
    @app_commands.command(name='compare', description='Compares the stats of two players')
    async def compare(self, interaction: discord.Interaction, player1: str, player2: str):
        """my command description
        Args:
            player1 (str): A Minecraft username
            player2 (str): A Minecraft username
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player1}"
        player1Data = getInfo(urlPP)
        urlPP: str = f"https://pitpanda.rocks/api/players/{player2}"
        player2Data = getInfo(urlPP)

        if not (player1Data["success"] and player2Data["success"]):
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:
            prestige = len(player1Data["data"].get("prestiges", [0])) - 1

            xp_progress = player1Data["data"].get("xpProgress", {})
            display_current_xp = int(xp_progress.get("displayCurrent", 0))
            level = pit_functions.xpToLevel(prestige, display_current_xp)

            doc = player1Data["data"].get("doc", {})
            xp = doc.get("xp", 0)
            gold = doc.get("lifetimeGold", 0)
            kills = doc.get("kills", 0)
            deaths = doc.get("deaths", 0)
            kdr = doc.get("kdr", 0.0)
            timeplayed = doc.get("playtime", 0)

            player1DataList = [prestige, level, xp, gold, kills, deaths, kdr, timeplayed]

            prestige = len(player2Data["data"].get("prestiges", [0])) - 1

            xp_progress = player2Data["data"].get("xpProgress", {})
            display_current_xp = int(xp_progress.get("displayCurrent", 0))
            level = pit_functions.xpToLevel(prestige, display_current_xp)

            doc = player2Data["data"].get("doc", {})
            xp = doc.get("xp", 0)
            gold = doc.get("lifetimeGold", 0)
            kills = doc.get("kills", 0)
            deaths = doc.get("deaths", 0)
            kdr = doc.get("kdr", 0.0)
            timeplayed = doc.get("playtime", 0)

            player2DataList = [prestige, level, xp, gold, kills, deaths, kdr, timeplayed]

            winner = 0
            if player1DataList[0]/player1DataList[7] > player2DataList[0]/player2DataList[7]:
                winner = 1
                embed = discord.Embed(title=f"[{formatting_functions.int_to_roman(player1DataList[0])}{player1DataList[1]}] {player1Data['data']['name']} vs [{formatting_functions.int_to_roman(player2DataList[0])}{player2DataList[1]}] {player2Data['data']['name']}", color=calcBracketColor(player1DataList[0]))
            else:
                embed = discord.Embed(title=f"[{formatting_functions.int_to_roman(player1DataList[0])}{player1DataList[1]}] {player1Data['data']['name']} vs [{formatting_functions.int_to_roman(player2DataList[0])}{player2DataList[1]}] {player2Data['data']['name']}", color=calcBracketColor(player2DataList[0]))

            signs = []
            for i in range(0, len(player1DataList)):
                if player1DataList[i] < player2DataList[i]:
                    signs.append('<')
                elif player1DataList[i] > player2DataList[i]:
                    signs.append('>')
                else:
                    signs.append('=')

            embed.add_field(name="Prestige & Level:", value=f"[{formatting_functions.int_to_roman(player1DataList[0])}{player1DataList[1]}]    {signs[0]}    [{formatting_functions.int_to_roman(player2DataList[0])}{player2DataList[1]}]", inline=False)
            embed.add_field(name="<:xpbottle:1245974825865056276> Lifetime XP:", value=f"{formatting_functions.add_commas(player1DataList[2])} XP {signs[2]} {formatting_functions.add_commas(player2DataList[2])} XP", inline=False)
            embed.add_field(name="<:goldingot:1247391882968043652> Lifetime Gold:", value=f"{formatting_functions.add_commas(player1DataList[3])} G {signs[3]} {formatting_functions.add_commas(player2DataList[3])} G", inline=False)
            embed.add_field(name="<:ironsword:1247392632129323080> Kills:", value=f"{formatting_functions.add_commas(player1DataList[4])} {signs[4]} {formatting_functions.add_commas(player2DataList[4])}", inline=False)
            embed.add_field(name="<:ironchestplate:1247719811857907762> Deaths:", value=f"{formatting_functions.add_commas(player1DataList[5])} {signs[5]} {formatting_functions.add_commas(player2DataList[5])}", inline=False)
            embed.add_field(name="<:diamondsword:1247404240016773231> KDR:", value=f"{player1DataList[6]:.2f} {signs[6]} {player2DataList[6]:.2f}", inline=False)
            embed.add_field(name="<a:minecraftclock:1247400003786510479> Time Played:", value=f"{formatting_functions.format_playtime(int(player1DataList[7]))} {signs[7]} {formatting_functions.format_playtime(int(player2DataList[7]))}", inline=False)
            if winner == 1:
                embed.add_field(name=":first_place: Winner:", value=f"{player1Data['data']['name']} with {(player1DataList[0] / (player1DataList[7] / 1440)):.2f} Prestiges per Day", inline=False)
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{player1Data['data']['uuid']}?format=webp")
            else:
                embed.add_field(name=":first_place: Winner:", value=f"{player2Data['data']['name']} with {(player2DataList[0] / (player2DataList[7] / 1440)):.2f} Prestiges per Day", inline=False)
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{player2Data['data']['uuid']}?format=webp")
            embed.set_footer(text=footerDateGen())

            await interaction.response.send_message(embed=embed) # noqa

    # Create the command to show an overview of a player's stats
    @app_commands.command(name="overview", description='Shows an overview of a player\'s stats')
    async def overview(self, interaction: discord.Interaction, player: str):
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

            prestige = len(data["data"].get("prestiges", [0])) - 1

            xp_progress = data["data"].get("xpProgress", {})
            display_current_xp = int(xp_progress.get("displayCurrent", 0))
            level = pit_functions.xpToLevel(prestige, display_current_xp)

            doc = data["data"].get("doc", {})
            xp = doc.get("xp", 0)
            gold = doc.get("lifetimeGold", 0)
            kills = doc.get("kills", 0)
            deaths = doc.get("deaths", 0)
            kdr = str(doc.get("kdr", 0.0))
            kdr = kdr[:kdr.index(".") + 3] if "." in kdr else kdr
            timeplayed = doc.get("playtime", 0)
            timeplayed = formatting_functions.format_playtime(int(timeplayed))

            embed = discord.Embed(title=f"Player Stats for [{formatting_functions.int_to_roman(prestige)}{level}] {data['data']['name']}", color=calcBracketColor(int(prestige)))
            embed.add_field(name=f"{pit_functions.getBracketColorEmoji(prestige)} Prestige & Level:", value=f"[{formatting_functions.int_to_roman(prestige)}{level}]", inline=False)
            embed.add_field(name="<:xpbottle:1245974825865056276> Lifetime XP:", value=f"{formatting_functions.add_commas(xp)} XP", inline=False)
            embed.add_field(name="<:goldingot:1247391882968043652> Lifetime Gold:", value=f"{formatting_functions.add_commas(gold)} G", inline=False)
            embed.add_field(name="<:ironsword:1247392632129323080> Kills:", value=f"{formatting_functions.add_commas(kills)}", inline=False)
            embed.add_field(name="<:ironchestplate:1247719811857907762> Deaths:", value=f"{formatting_functions.add_commas(deaths)}", inline=False)
            embed.add_field(name="<:diamondsword:1247404240016773231> KDR:", value=f"{kdr}", inline=False)
            embed.add_field(name="<a:minecraftclock:1247400003786510479> Time Played:", value=f"{timeplayed}", inline=False)
            embed.set_footer(text=footerDateGen())
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")

            await interaction.response.send_message(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(compare(client))
