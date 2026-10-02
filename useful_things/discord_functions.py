import discord
from datetime import datetime

# Generate the current time to be placed in an embed's footer
def footerDateGen():
    now = datetime.now()
    formatted_now = now.strftime("%m/%d/%Y %I:%M %p")
    formatted_now = formatted_now.replace(" 0", " ")
    return formatted_now

# Return the role object that corresponds to a certain prestige
def getPrestigeRole(prestige: int, interaction):
    if prestige == 0:
        return discord.utils.get(interaction.guild.roles, name="Grey Brackets")
    elif int(prestige / 5) == 0:
        return discord.utils.get(interaction.guild.roles, name="Blue Brackets")
    elif int(prestige / 5) == 1:
        return discord.utils.get(interaction.guild.roles, name="Yellow Brackets")
    elif int(prestige / 5) == 2:
        return discord.utils.get(interaction.guild.roles, name="Orange Brackets")
    elif int(prestige / 5) == 3:
        return discord.utils.get(interaction.guild.roles, name="Red Brackets")
    elif int(prestige / 5) == 4:
        return discord.utils.get(interaction.guild.roles, name="Purple Brackets")
    elif int(prestige / 5) == 5:
        return discord.utils.get(interaction.guild.roles, name="Pink Brackets")
    elif int(prestige / 5) == 6:
        return discord.utils.get(interaction.guild.roles, name="White Brackets")
    elif int(prestige / 5) == 7:
        return discord.utils.get(interaction.guild.roles, name="Aqua Brackets")
    elif int(prestige / 5) == 8:
        return discord.utils.get(interaction.guild.roles, name="Dark Blue Brackets")
    elif prestige == 45 or prestige == 46 or prestige == 47:
        return discord.utils.get(interaction.guild.roles, name="Black Brackets")
    elif prestige == 48 or prestige == 49:
        return discord.utils.get(interaction.guild.roles, name="Dark Red Brackets")
    else:
        return discord.utils.get(interaction.guild.roles, name="Dark Grey Brackets")
