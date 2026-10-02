import discord
from discord.ext import commands
from discord import app_commands
from useful_things.api_functions import getInfo
from useful_things import pit_functions
from useful_things import formatting_functions
from useful_things.discord_functions import footerDateGen
from useful_things.pit_functions import calcBracketColor


class mapQuests(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Create the genesis command
    @app_commands.command(name='genesis', description='Shows a player\'s genesis progress')
    async def genesis(self, interaction: discord.Interaction, player: str):
        """
        Args:
            player (str): A Minecraft username
        """
        pass

        failed = False

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        data = getInfo(urlPP)

        if not data["success"]:
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:
            prestige = len(data["data"]["prestiges"]) - 1
            level = pit_functions.xpToLevel(prestige, int(data["data"]["xpProgress"]["displayCurrent"]))

            doc = data["data"].get("doc", ())
            points = doc.get("genesisPoints", 0)
            allegiance = doc.get("allegiance", )
            tier = pit_functions.calculateFactionTier(points)

            demonRewards = ["Deal +0.5♥︎ damage to players in the Angel faction.", "Unlock the Demon spawn.", "The Mystic Well costs 1/3 of the price.", "Deal +0.5♥︎ damage to players wearing diamond armor.", "Accumulate +50% gold on your bounties. Earn +1 renown when earning renown from events.", "Earn Armageddon Boots.", "Permanently gain +0.2g from kills. Can be claimed up to 15 times."]
            angelRewards = ["Deal +0.5♥︎ damage to players in the Demon faction.", "Unlock the Angel spawn.", "Diamond items cost 1/3 of the price.", "	Deal +0.25♥︎ damage to players wearing leather armor.", "Accumulate +50% gold on your bounties. Earn +1 renown when earning renown from events.", "Earn Archangel Chestplate.", "Permanently gain +1% XP from kills. Can be claimed up to 15 times."]

            embed = discord.Embed(title=f"Genesis points for [{formatting_functions.int_to_roman(prestige)}{level}] {data['data']['name']}", color=calcBracketColor(48))
            embed.add_field(name="Allegiance:", value=f"{allegiance}", inline=False)
            embed.add_field(name="Points:", value=f"{points}", inline=False)
            embed.add_field(name="Tier:", value=f"{tier}", inline=False)
            embed.add_field(name="Earned rewards:", value="")

            if allegiance == "DEMON":
                for i in range(0, tier):
                    embed.add_field(name="", value=f":white_check_mark: {demonRewards[i]}", inline=False)

                embed.add_field(name="Unearned rewards:", value="")

                for i in range(tier, 7):
                    embed.add_field(name="", value=f":x: {demonRewards[i]}", inline=False)

            elif allegiance == "ANGEL":
                for i in range(0, tier):
                    embed.add_field(name="", value=f":white_check_mark: {angelRewards[i]}", inline=False)

                embed.add_field(name="Unearned rewards:", value="")

                for i in range(tier, 7):
                    embed.add_field(name="", value=f":x: {angelRewards[i]}", inline=False)
            else:
                embed = discord.Embed(title=f"{data['data']['name']} has not participated in a Genesis Faction", color=discord.Color.red())

                failed = True

                await interaction.response.send_message(embed=embed, ephemeral=True) # noqa

            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")

            if not failed:
                await interaction.response.send_message(embed=embed) # noqa

    # Create the kings quest command
    @app_commands.command(name="kings-quest", description="Determines what level completing the King's Quest will grant")
    async def kingsQuest(self, interaction: discord.Interaction, player: str):
        """
        Args:
            player (str): A Minecraft username
        """
        pass

        failed = False

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        dataPP = getInfo(urlPP)

        if not dataPP["success"]:
            embed = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embed, ephemeral=True)  # noqa

        else:
            currentPrestige = len(dataPP["data"]["prestiges"]) - 1
            currentPrestigeRomanNum = formatting_functions.int_to_roman(currentPrestige)
            playerName = dataPP['data']['name']

            if currentPrestige == 0:
                embed = discord.Embed(title=f"{playerName} is unable to do kings", color=discord.Color.red())

                failed = True

                await interaction.response.send_message(embed=embed, ephemeral=True) # noqa

            currentXP = dataPP["data"]["xpProgress"]["displayCurrent"]
            prestigeGoalXP = dataPP["data"]["xpProgress"]["displayGoal"]
            afterKingsXP = int(prestigeGoalXP / 3) + currentXP
            resultingLevel = pit_functions.xpToLevel(currentPrestige, afterKingsXP)

            if resultingLevel == 120:
                grantedXP = prestigeGoalXP - currentXP
            else:
                grantedXP = int(prestigeGoalXP / 3)

            embed = discord.Embed(title=f"Kings Quest for {playerName}", color=pit_functions.calcBracketColor(currentPrestige))
            embed.add_field(name=f"[{currentPrestigeRomanNum}{formatting_functions.extract_substring(dataPP['data']['formattedLevel'])}] ---> [{currentPrestigeRomanNum}{resultingLevel}]:", value=f"<:xpbottle:1245974825865056276> {formatting_functions.add_commas(grantedXP)} XP granted")
            embed.set_footer(text=footerDateGen())
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{dataPP['data']['uuid']}?format=webp")

            if not failed:
                await interaction.response.send_message(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(mapQuests(client))
