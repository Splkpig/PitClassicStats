import discord
from discord.ext import commands
from discord import app_commands
from useful_things.pit_functions import calcBracketColor
from useful_things.api_functions import getInfo
from useful_things.discord_functions import footerDateGen
from useful_things.owner_functions import isOwnerAccount


class pitpandaSignatures(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # Create the PitPanda prestige and level embed command
    @app_commands.command(name="prestige-level", description="Displays Pitpanda prestige and level signature")
    async def prestige_level(self, interaction: discord.Interaction, player: str):
        """my command description
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
            currentPrestige = len(dataPP["data"]["prestiges"]) - 1

            embed = discord.Embed(title="Prestige & Level", color=calcBracketColor(int(currentPrestige)))

            if isOwnerAccount(player) == 1:
                embed.set_footer(text="splk op", icon_url="https://cdn.discordapp.com/avatars/688203642695581717/a_76a39f85528f655d756e6a0973326b35.gif?size=1024")
            elif isOwnerAccount(player) == 2:
                embed.set_footer(text="rey op", icon_url="https://images-ext-1.discordapp.net/external/0c2WqP3aimB2oJi9q0YGq53fHtQTMpP1qz_eF35kN-U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/774915176888533015/39000c6479818cf02aa14e4ba9271eb4.png?format=webp&quality=lossless&width=702&height=702")
            else:
                embed.set_footer(text=footerDateGen())

            embed.set_image(url=f"https://pitpanda.rocks/api/images/level/{player}")

            await interaction.response.send_message(embed=embed)  # noqa

    # Create the PitPanda profile embed command
    @app_commands.command(name="profile", description="Display Pitpanda Profile Signature")
    async def profile(self, interaction: discord.Interaction, player: str):
        """my command description
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
            currentPrestige = len(dataPP["data"]["prestiges"]) - 1

            embed = discord.Embed(title="Prestige & Level", color=calcBracketColor(int(currentPrestige)))

            if isOwnerAccount(player) == 1:
                embed.set_footer(text="splk op", icon_url="https://cdn.discordapp.com/avatars/688203642695581717/a_76a39f85528f655d756e6a0973326b35.gif?size=1024")
            elif isOwnerAccount(player) == 2:
                embed.set_footer(text="rey op", icon_url="https://images-ext-1.discordapp.net/external/0c2WqP3aimB2oJi9q0YGq53fHtQTMpP1qz_eF35kN-U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/774915176888533015/39000c6479818cf02aa14e4ba9271eb4.png?format=webp&quality=lossless&width=702&height=702")
            else:
                embed.set_footer(text=footerDateGen())

            embed.set_image(url=f"https://pitpanda.rocks/api/images/profile/{player}")

            await interaction.response.send_message(embed=embed)  # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(pitpandaSignatures(client))
