import discord
from discord import app_commands
from discord.ext import commands

from useful_things import api_functions
from useful_things.api_functions import getInfo
from useful_things.discord_functions import footerDateGen


class fun(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="jenna", description="Compares your yapping to Jenna's")
    async def jenna(self, interaction: discord.Interaction, player: str):
        """My command description
        Args:
            player (str): A Minecraft username
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        dataPP = getInfo(urlPP)

        if not dataPP["success"]:
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa
        else:
            jennaUrl: str = "https://pitpanda.rocks/api/players/jennavote"
            jennaData = api_functions.getInfo(jennaUrl)

            jennaChatMessages = jennaData["data"]["doc"]["chatMessages"]
            jennaPlaytime = int((jennaData["data"]["playtime"]) / 60)

            playerName = dataPP['data']['name']
            playerChatMessages = dataPP["data"]["doc"]["chatMessages"]
            playerPlaytime = int((dataPP["data"]["playtime"]) / 60)

            if jennaChatMessages > playerChatMessages and jennaPlaytime > playerPlaytime:  # SweatySharkBers
                embed = discord.Embed(title="", color=discord.Color.purple())
                embed.add_field(name=f"As expected jenna has out yapped {playerName}", value=f"In {jennaPlaytime - playerPlaytime} more hours jenna has yapped {jennaChatMessages - playerChatMessages} more times than {playerName}")
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/aaea990d-8e10-4cbe-a9ee-836564dd19d0?format=webp")
                embed.set_footer(text=footerDateGen())

                await interaction.response.send_message(embed=embed) # noqa
            elif jennaChatMessages > playerChatMessages and jennaPlaytime < playerPlaytime:  # Splkpig
                embed = discord.Embed(title="", color=discord.Color.purple())
                embed.add_field(name=f"As expected jenna has out yapped {playerName}", value=f" In {playerPlaytime - jennaPlaytime} less hours jenna has yapped {jennaChatMessages - playerChatMessages} more times than {playerName}")
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/aaea990d-8e10-4cbe-a9ee-836564dd19d0?format=webp")
                embed.set_footer(text=footerDateGen())

                await interaction.response.send_message(embed=embed) # noqa
            elif jennaChatMessages < playerChatMessages and jennaPlaytime > playerPlaytime:  # nCry
                embed = discord.Embed(title="", color=discord.Color.purple())
                embed.add_field(name=f"WOW! {playerName} has out yapped jenna", value=f" In {jennaPlaytime - playerPlaytime} less hours {playerName} has yapped {playerChatMessages - jennaChatMessages} more times than jenna")
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{dataPP['data']['uuid']}?format=webp")
                embed.set_footer(text=footerDateGen())

                await interaction.response.send_message(embed=embed) # noqa
            elif jennaChatMessages < playerChatMessages and jennaPlaytime < playerPlaytime:
                embed = discord.Embed(title="", color=discord.Color.purple())
                embed.add_field(name=f"WOW! {playerName} has out yapped jenna", value=f"In {playerPlaytime - jennaPlaytime} more hours {playerName} has yapped {playerChatMessages - jennaChatMessages} more times than jenna")
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{dataPP['data']['uuid']}?format=webp")
                embed.set_footer(text=footerDateGen())

                await interaction.response.send_message(embed=embed) # noqa
            else:
                embed = discord.Embed(title="", color=discord.Color.purple())
                embed.add_field(name=f"you guys somehow tied", value=f"ping me so i can add functionality to this part")

                await interaction.response.send_message(embed=embed) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(fun(client))



