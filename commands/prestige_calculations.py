import discord
from discord.ext import commands
from discord import app_commands
from useful_things.api_functions import getInfo
from useful_things.discord_functions import footerDateGen
from useful_things import formatting_functions
from useful_things.file_functions import read_specific_line
from useful_things import pit_functions

globalPrestige = 0
globalLevel = 0
globalPlayer = ""

# Create the button to show more information about a player's xp until
class simpleView(discord.ui.View):

    @discord.ui.button(label="View data breakdown", style=discord.ButtonStyle.blurple)
    async def showDataBreakdown(self, interaction: discord.Interaction, button: discord.ui.Button):
        global globalPrestige
        global globalLevel
        global globalPlayer

        urlPP: str = f"https://pitpanda.rocks/api/players/{globalPlayer}"
        dataPP = getInfo(urlPP)
        docData = dataPP["data"]["doc"]

        currentXP = docData["xp"]
        goalXP = float(read_specific_line("../PitStats/useful_things/pitdata/xp_sums.txt", globalPrestige - 1))
        goalXPFromFinalPrestige = pit_functions.calculateXPForLevel(globalPrestige, globalLevel)
        goalXP += goalXPFromFinalPrestige
        currentPrestige = len(dataPP["data"]["prestiges"]) - 1
        currentLevel = formatting_functions.extract_substring(dataPP['data']['formattedLevel'])

        neededXP = goalXP - currentXP

        embed = discord.Embed(title=f"XP until for {dataPP['data']['name']}", color=pit_functions.calcBracketColor(globalPrestige))
        embed.set_footer(text=footerDateGen())
        embed.add_field(name=f"[{formatting_functions.int_to_roman(globalPrestige)}{globalLevel}]:",
                        value=f"{formatting_functions.add_commas(goalXP)} XP required", inline=False)
        embed.add_field(name=f"[{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {dataPP['data']['name']} currently has:",
                        value=f"{formatting_functions.add_commas(currentXP)} XP", inline=False)
        embed.add_field(name=f"To reach [{formatting_functions.int_to_roman(globalPrestige)}{globalLevel}]: ",
                        value=f"{formatting_functions.add_commas(neededXP)} XP required", inline=False)
        embed.add_field(name=f"At {formatting_functions.add_commas(int(dataPP['data']['doc']['xpHourly']))} XP per hour:", value=f"{formatting_functions.add_commas(neededXP)} XP will take {formatting_functions.add_commas(int(neededXP / dataPP['data']['doc']['xpHourly']))} hours", inline=False)

        await interaction.response.send_message(embed=embed)  # noqa
        self.stop()


class prestigeCalculations(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # Create the show a player's prestige info command
    @app_commands.command(name="prestige-info", description="Shows XP and Gold info for current prestige")
    async def prestige_info(self, interaction: discord.Interaction, player: str):
        """my command description
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

            currentPrestige = len(data["data"].get("prestiges", [0])) - 1

            xpProgress = data["data"].get("xpProgress", {})
            display_current_xp = int(xpProgress.get("displayCurrent", 0))
            currentLevel = pit_functions.xpToLevel(currentPrestige, display_current_xp)

            goldProgress = data["data"].get("goldProgress", {})
            currentXP = xpProgress["displayCurrent"]
            prestigeGoalXP = xpProgress["displayGoal"]
            currentGoldGrinded = goldProgress["displayCurrent"]
            prestigeGoalGold = goldProgress["displayGoal"]
            neededXP = prestigeGoalXP - currentXP
            neededGold = prestigeGoalGold - currentGoldGrinded

            embed = discord.Embed(title=f"Prestige Info for [{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] {data['data']['name']}", color=pit_functions.calcBracketColor(currentPrestige))
            embed.set_footer(text=footerDateGen())
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")

            if currentLevel != '120':
                embed.add_field(name=f"<:xpbottle:1245974825865056276> XP Breakdown", value=f"{formatting_functions.add_commas(currentXP)} XP / {formatting_functions.add_commas(prestigeGoalXP)} XP \n{int(100 * (currentXP/prestigeGoalXP))}% grinded \nThis will take {formatting_functions.add_commas(int(neededXP / data['data']['doc']['xpHourly']))} hours", inline=False)
            else:
                embed.add_field(name=f"<:xpbottle:1245974825865056276> XP Breakdown", value=f"{formatting_functions.add_commas(currentXP)} XP / {formatting_functions.add_commas(prestigeGoalXP)} XP \n100% grinded", inline=False)

            if currentGoldGrinded < prestigeGoalGold:
                embed.add_field(name=f"<:goldingot:1247391882968043652> Gold Breakdown", value=f"{formatting_functions.add_commas(currentXP)} G / {formatting_functions.add_commas(prestigeGoalGold)} G \n{int(100 * (currentGoldGrinded/prestigeGoalGold))}% grinded \nThis will take {formatting_functions.add_commas(int(neededGold / data['data']['doc']['goldHourly']))} hours", inline=False)
            else:
                embed.add_field(name=f"<:goldingot:1247391882968043652> Gold Breakdown", value=f"{formatting_functions.add_commas(currentGoldGrinded)} G / {formatting_functions.add_commas(prestigeGoalGold)} G \n{int(100 * (currentGoldGrinded/prestigeGoalGold))}% grinded",inline=False)

            await interaction.response.send_message(embed=embed)  # noqa

    # Create the xp until calculation command
    @app_commands.command(name="xp-until", description="XP needed to reach a certain prestige and level")
    async def xp_until(self, interaction: discord.Interaction, player: str, prestige: int, level: int):
        """my command description
        Args:
            player (str): A Minecraft username
            prestige (int): A prestige
            level (int): A level
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        data = getInfo(urlPP)

        global globalPrestige
        global globalLevel
        global globalPlayer

        globalPrestige = prestige
        globalLevel = level
        globalPlayer = player

        if not data["success"]:
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:

            failed = False

            if not (0 <= prestige <= 50) or not (0 <= level <= 120):
                embedPrestigeFail = discord.Embed(title="Enter a valid prestige and level combination", color=discord.Color.red())
                failed = True

                await interaction.response.send_message(embed=embedPrestigeFail, ephemeral=True) # noqa

            currentPrestige = len(data["data"].get("prestiges", [0])) - 1

            xp_progress = data["data"].get("xpProgress", {})
            display_current_xp = int(xp_progress.get("displayCurrent", 0))
            currentLevel = pit_functions.xpToLevel(currentPrestige, display_current_xp)

            doc = data["data"].get("doc", {})
            xp = doc.get("xp", 0)

            goalXP = float(read_specific_line("../PitStats/useful_things/pitdata/xp_sums.txt", prestige - 1))
            goalXPFromFinalPrestige = pit_functions.calculateXPForLevel(prestige, level)
            goalXP += goalXPFromFinalPrestige

            neededXP = goalXP - xp

            if (prestige == currentPrestige and level <= int(currentLevel)) or (prestige < currentPrestige) and not failed:
                embedPrestigeFail = discord.Embed(title="Enter a prestige and level combination greater than your current prestige", color=discord.Color.red())
                failed = True

                await interaction.response.send_message(embed=embedPrestigeFail, ephemeral=True) # noqa

            embed = discord.Embed(title=f"XP until for {data['data']['name']}", color=pit_functions.calcBracketColor(prestige))
            embed.set_footer(text=footerDateGen())

            embed.add_field(name=f"[{formatting_functions.int_to_roman(currentPrestige)}{currentLevel}] ---> [{formatting_functions.int_to_roman(prestige)}{level}]:", value=f"<:xpbottle:1245974825865056276> {formatting_functions.add_commas(neededXP)} XP required")
            embed.add_field(name=f"", value=f"<a:minecraftclock:1247400003786510479> This will take {formatting_functions.add_commas(int(neededXP / data['data']['doc']['xpHourly']))} hours", inline=False)
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")

            view = simpleView(timeout=None)

            if not failed:
                await interaction.response.send_message(embed=embed, view=view)  # noqa
                await view.wait()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(prestigeCalculations(client))
