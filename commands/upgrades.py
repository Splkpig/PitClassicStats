import discord
from discord import app_commands
from discord.ext import commands
from useful_things import pit_functions
from useful_things import formatting_functions
from useful_things.api_functions import getInfo
from collections import Counter

# Create lists of the formatted and functional upgrade names
keys = ["xp_boost0", "xp_boost1", "xp_boost2", "xp_boost3", "xp_boost4", "xp_boost5", "cash_boost0", "cash_boost1", "cash_boost2", "cash_boost3", "cash_boost4", "cash_boost5", "melee_damage0", "melee_damage1", "melee_damage2", "melee_damage3", "melee_damage4", "melee_damage5", "bow_damage0", "bow_damage1", "bow_damage2", "bow_damage3", "bow_damage4", "bow_damage5", "damage_reduction0", "damage_reduction1", "damage_reduction2", "damage_reduction3", "damage_reduction4", "damage_reduction5", "build_battler0", "build_battler1", "build_battler2", "build_battler3", "build_battler4", "build_battler5", "el_gato0", "el_gato1", "el_gato2", "el_gato3", "el_gato4", "el_gato5", "golden_heads", "fishing_rod", "lava_bucket", "strength_chaining", "free_blocks", "endless_quiver", "safety_first", "barbarian", "trickle_down", "lucky_diamond", "spammer", "bounty_hunter", "streaker", "assistant_streaker", "coop_cat", "conglomerate", "gladiator", "vampire", "recon", "overheal", "rambo", "olympus", "dirty", "first_strike", "soup", "marathon", "thick", "kung_fu_knowledge", "second_gapple", "extra_xp", "res_and_regen", "arquebusier", "khanate", "leech", "tough_skin", "fight_or_flight", "pungent", "speed_two", "withercraft", "feast", "counter_strike", "gold_nanofactory", "tactical_retreat", "glass_sword", "assured_strike", "shield_aura", "ice_cube", "super_streaker", "gold_stack", "xp_stack", "monster", "sponge_steve", "apostle", "overdrive", "beastmode", "hermit", "highlander", "grand_finale", "to_the_moon", "uberstreak"]
names = ["XP Boost 1", "XP Boost 2", "XP Boost 3", "XP Boost 4", "XP Boost 5", "XP Boost 6", 'Gold Boost 1', 'Gold Boost 2', 'Gold Boost 3', 'Gold Boost 4', 'Gold Boost 5', 'Gold Boost 6', "Melee Damage 1", "Melee Damage 2", "Melee Damage 3", "Melee Damage 4", "Melee Damage 5", "Melee Damage 6", "Bow Damage 1", "Bow Damage 2", "Bow Damage 3", "Bow Damage 4", "Bow Damage 5", "Bow Damage 6", "Damage Reduction 1", "Damage Reduction 2", "Damage Reduction 3", "Damage Reduction 4", "Damage Reduction 5", "Damage Reduction 6", "Build Battler 1", "Build Battler 2", "Build Battler 3", "Build Battler 4", "Build Battler 5", "Build Battler 6", "El Gato 1", "El Gato 2", "El Gato 3", "El Gato 4", "El Gato 5", "El Gato 6", "Golden Heads", "Fishing Rod", "Lava Bucket", "Strength-Chaining", "Mineman", "Bonk!", "Safety First", "Barbarian", "Trickle Down", "Lucky Diamond", "Spammer", "Bounty Hunter", "Streaker", "Assistant (to the) Streaker", "Co-op Cat", "Conglomerate", "Gladiator", "Vampire", "Recon", "Overheal", "Rambo", "Olympus", "Dirty", "First Strike", "Soup", "Marathon", "Thick", "Kung Fu Knowledge", "Second Gapple", "Explicious", "R&R", "Arquebusier", "Khanate", "Leech", "Tough Skin", "Fight or Flight", "Pungent", "Hero's Haste", "Rush", "Feast", "Counter-Strike", "Gold Nano-Factory", "Tactical Retreat", "Glass Pickaxe", "Assured Strike", "Aura of Protection", "Ice Cube", "Super Streaker", "Gold Stack", "XP Stack", "Monster", "Spongesteve", "Apostle to RNGesus", "Overdrive", "Beastmode", "Hermit", "Highlander", "Magnum Opus", "To the Moon", "Uberstreak"]
namesFormated = ['<:xpboost:1251035226008850473> XP Boost 1', '<:xpboost:1251035226008850473> XP Boost 2', '<:xpboost:1251035226008850473> XP Boost 3', '<:xpboost:1251035226008850473> XP Boost 4', '<:xpboost:1251035226008850473> XP Boost 5', '<:xpboost:1251035226008850473> XP Boost 6', '<:goldboost:1251035984293007440> Gold Boost 1', '<:goldboost:1251035984293007440> Gold Boost 2', '<:goldboost:1251035984293007440> Gold Boost 3', '<:xpboost:1251035226008850473> Gold Boost 4', '<:goldboost:1251035984293007440> Gold Boost 5', '<:goldboost:1251035984293007440> Gold Boost 6', "<:damagedealt:1248127865103585391> Melee Damage 1", "<:damagedealt:1248127865103585391> Melee Damage 2", "<:damagedealt:1248127865103585391> Melee Damage 3", "<:damagedealt:1248127865103585391> Melee Damage 4", "<:damagedealt:1248127865103585391> Melee Damage 5", "<:damagedealt:1248127865103585391> Melee Damage 6", "<:bowdamage:1251036153864388659> Bow Damage 1", "<:bowdamage:1251036153864388659> Bow Damage 2", "<:bowdamage:1251036153864388659> Bow Damage 3", "<:bowdamage:1251036153864388659> Bow Damage 4", "<:bowdamage:1251036153864388659> Bow Damage 5", "<:bowdamage:1251036153864388659> Bow Damage 6", "<:damagereceived:1248128029427892316> Damage Reduction 1", "<:damagereceived:1248128029427892316> Damage Reduction 2", "<:damagereceived:1248128029427892316> Damage Reduction 3", "<:damagereceived:1248128029427892316> Damage Reduction 4", "<:damagereceived:1248128029427892316> Damage Reduction 5", "<:damagereceived:1248128029427892316> Damage Reduction 6", "<:buildbattler:1251036278070186005> Build Battler 1", "<:buildbattler:1251036278070186005> Build Battler 2", "<:buildbattler:1251036278070186005> Build Battler 3", "<:buildbattler:1251036278070186005> Build Battler 4", "<:buildbattler:1251036278070186005> Build Battler 5", "<:buildbattler:1251036278070186005> Build Battler 6", "<:elgato:1251036569582829632> El Gato 1", "<:elgato:1251036569582829632> El Gato 2", "<:elgato:1251036569582829632> El Gato 3", "<:elgato:1251036569582829632> El Gato 4", "<:elgato:1251036569582829632> El Gato 5", "<:elgato:1251036569582829632> El Gato 6", "<:goldenhead:1248127570373775433> Golden Heads", "<:fishingrod:1248127083549556736> Fishing Rod", "<:lavabucket:1248126173074952222> Lava Bucket", "<:strengthchaining:1251037721724588162> Strength-Chaining", "<:diamondpickaxe:1248119046172446792> Mineman", "<:bonk:1251037940835029083> Bonk!", "<:safetyfirst:1251038090185674833> Safety First", "<:barbarian:1251038226597281793> Barbarian", "<:trickledown:1251038830241517650> Trickle Down", "<:luckydiamond:1251038963079188530> Lucky Diamond", "<:spammer:1251039108390850630> Spammer", "<:goldleggings:1248119482388316202> Bounty Hunter", "<:wheat:1248124503255420928> Streaker", "<:atts:1251039331955769385> Assistant (to the) Streaker", "<:coopcat:1251040069205360671> Co-op Cat", "<:conglomerate:1251040606160027679> Conglomerate", "<:gladiator:1251040731062341653> Gladiator", "<:fermentedspidereye:1248124676706926642> Vampire", "<:recon:1251040865850232903> Recon", "<:overheal:1251040981046919271> Overheal", "<:rambo:1251041176983703583> Rambo", "<:olympus:1251042140763721788> Olympus", "<:dirty:1251042306677542943> Dirty", "<:firststrike:1251042483811389474> First Strike", "<:mushroomstew:1248125413109141567> Soup", "<:marathon:1251043772200914944> Marathon", "<:thick:1251043923204243528> Thick", "<:kungfu:1251044013440630896> Kung Fu Knowledge", "<:goldenapple:1248127429084577913> Second Gapple", "<:xpboost:1251035226008850473> Explicious", "<:rr:1251044876703891516> R&R", "<:Arrow:1248117169653284926> Arquebusier", "<:goldenhelmet:1248126543553892443> Khanate", "<:leech:1251045967000633436> Leech", "<:toughskin:1251046230507782216> Tough Skin", "<:fightorflight:1251046419477954570> Fight or Flight", "<:fermentedspidereye:1248124676706926642> Pungent", "<:enchantedbook:1248119930155569222> Hero's Haste", "<:rush:1251046981405638706> Rush", "<:feast:1251047151333675038> Feast", "<:counterstrike:1251054076087504957> Counter-Strike", "<:trickledown:1251038830241517650> Gold Nano-Factory", "<:tacticalretreat:1251047854781497344> Tactical Retreat", "<:diamondpickaxe:1248119046172446792> Glass Pickaxe", "<:assuredstrike:1251048244155387935> Assured Strike", "<:auraofprot:1251048358617813123> Aura of Protection", "<:icecube:1251048590080475260> Ice Cube", "<:overheal:1251040981046919271> Super Streaker", "<:goldstack:1251048724424167445> Gold Stack", "<:xpstack:1251048813603586048> XP Stack", "<:thick:1251043923204243528> Monster", "<:spongesteve:1251048966582177802> Spongesteve", "<:aspostle:1251049079866392616> Apostle to RNGesus", "<:overdrive:1251049188763111447> Overdrive", "<:beastmode:1251049421236342887> Beastmode", "<:hermit:1251049608268742657> Hermit", "<:highlander:1251056305247092806> Highlander", "<:opus:1251049779400671272> Magnum Opus", "<:tothemoon:1251049903057010728> To the Moon", "<:uberstreak:1251050047014174793> Uberstreak"]

# Track the current page
currentPage = 0
globalPages = []


# Create the buttons to scroll through a player's most purchased upgrades
class simpleView(discord.ui.View):
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage

        if currentPage == 0:
            embed = globalPages[currentPage]
            view = simpleView(timeout=None)
        else:
            embed = globalPages[currentPage - 1]
            currentPage -= 1
            view = simpleView(timeout=None)

        embed.set_footer(text=f"Current Page: {currentPage + 1} / {len(globalPages)}")
        await interaction.response.edit_message(embed=embed, view=view) # noqa

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        global currentPage

        if currentPage == len(globalPages) - 1:
            embed = globalPages[currentPage]
            view = simpleView(timeout=None)
        else:
            embed = globalPages[currentPage + 1]
            currentPage += 1
            view = simpleView(timeout=None)

        embed.set_footer(text=f"Current Page: {currentPage + 1} / {len(globalPages)}")
        await interaction.response.edit_message(embed=embed, view=view) # noqa


class upgrades(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Create the upgrades command to show a player's most purchased Shop Upgrades, Perks, or Killstreaks
    @app_commands.command(name="upgrades", description="Shows a players most purchased upgrades")
    @app_commands.choices(upgrade_type=[app_commands.Choice(name='Shop Upgrades', value=1), app_commands.Choice(name='Perks', value=2), app_commands.Choice(name='Killstreak', value=3)])
    async def upgrades(self, interaction: discord.Interaction, player: str, upgrade_type: int = 0) -> None:
        """
        Args:
            player (str): A Minecraft username
            upgrade_type (int): A type of upgrade
        """
        pass

        urlPP: str = f"https://pitpanda.rocks/api/players/{player}"
        data = getInfo(urlPP)

        global keys
        global names
        global namesFormated
        global currentPage
        global globalPages

        currentPage = 0
        globalPages = []

        if not data["success"]:
            embedFail = discord.Embed(title="Player not found", color=discord.Color.red())

            await interaction.response.send_message(embed=embedFail, ephemeral=True)  # noqa

        else:
            prestiges = data["data"].get("prestiges", [0])
            prestigeUpgrades = []

            prestigeStat = len(data["data"].get("prestiges", [0])) - 1
            currentXP = data["data"]["xpProgress"]["displayCurrent"]
            currentLevel = pit_functions.xpToLevel(prestigeStat, currentXP)

            upgradeTypeEmbeds = ["Most purchased upgrades for ", "Most purchased shop upgrades for ", "Most purchased perks for ", "Most purchased killstreaks for "]
            embed = discord.Embed(title=f"{upgradeTypeEmbeds[upgrade_type]}[{formatting_functions.int_to_roman(prestigeStat)}{currentLevel}] {data['data']['name']}", color=pit_functions.calcBracketColor(prestigeStat))

            for prestige in prestiges:
                unlocks = prestige.get("unlocks", [0])
                upgradesList = []
                if upgrade_type == 0:
                    for unlock in unlocks:
                        if unlock["type"] != "Renown":
                            if "tier" in unlock:
                                upgradesList.append(unlock["key"] + str(unlock["tier"]))
                            else:
                                upgradesList.append(unlock["key"])
                    prestigeUpgrades.append(upgradesList)
                elif upgrade_type == 1:
                    for unlock in unlocks:
                        if unlock["type"] == "Upgrade":
                            upgradesList.append(unlock["key"] + str(unlock["tier"]))
                    prestigeUpgrades.append(upgradesList)
                elif upgrade_type == 2:
                    for unlock in unlocks:
                        if unlock["type"] == "Perk":
                            upgradesList.append(unlock["key"])
                    prestigeUpgrades.append(upgradesList)
                else:
                    for unlock in unlocks:
                        if unlock["type"] == "Killstreak":
                            upgradesList.append(unlock["key"])
                    prestigeUpgrades.append(upgradesList)

            combined = []
            for prestige in prestigeUpgrades:
                combined += prestige
            counts = Counter(combined).most_common()
            elements = []
            for item in counts:
                elements.append(item[0])
            pages = []

            for item in counts:
                if int(elements.index(item[0]) % 10) == 0 and elements.index(item[0]) != 0:
                    pages.append(embed)
                    embed = discord.Embed(title=f"{upgradeTypeEmbeds[upgrade_type]}[{formatting_functions.int_to_roman(prestigeStat)}{currentLevel}] {data['data']['name']}", color=pit_functions.calcBracketColor(prestigeStat))
                    embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")
                    embed.add_field(name=namesFormated[keys.index(item[0])], value=f"Purchased {item[1]} times", inline=False)
                else:
                    embed.add_field(name=namesFormated[keys.index(item[0])], value=f"Purchased {item[1]} times", inline=False)
                if elements.index(item[0]) == len(elements) - 1:
                    pages.append(embed)

            globalPages = pages
            embed = pages[0]
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{data['data']['uuid']}?format=webp")
            embed.set_footer(text=f"Current Page: {currentPage + 1} / {len(globalPages)}")
            view = simpleView(timeout=None)

            await interaction.response.send_message(embed=embed, view=view) # noqa


async def setup(client: commands.Bot) -> None:
    await client.add_cog(upgrades(client))
