from useful_things.file_functions import read_specific_line
from useful_things.api_functions import getInfo
from useful_things import formatting_functions

import json

# Return the hex color for a prestige's corresponding bracket
def calcBracketColor(prestige: int):
    if prestige == 0:
        return 0xAAAAAA
    elif int(prestige / 5) == 0:
        return 0x5555FF
    elif int(prestige / 5) == 1:
        return 0xFFFF55
    elif int(prestige / 5) == 2:
        return 0xFFAA00
    elif int(prestige / 5) == 3:
        return 0xFF5555
    elif int(prestige / 5) == 4:
        return 0xAA00AA
    elif int(prestige / 5) == 5:
        return 0xFF55FF
    elif int(prestige / 5) == 6:
        return 0xffffff
    elif int(prestige / 5) == 7:
        return 0x55FFFF
    elif int(prestige / 5) == 8:
        return 0x0000AA
    elif prestige == 45 or prestige == 46 or prestige == 47:
        return 0x000000
    elif prestige == 48 or prestige == 49:
        return 0xAA0000
    else:
        return 0x555555


# Return the emoji that corresponds to a bracket color for a certain prestige
def getBracketColorEmoji(prestige: int):
    if prestige == 0:
        return "<:pit_grey_circle:1247720645769560074>"
    elif int(prestige / 5) == 0:
        return "<:pit_blue_circle:1247721141821374509>"
    elif int(prestige / 5) == 1:
        return "<:pit_yellow_circle:1247721236063322184>"
    elif int(prestige / 5) == 2:
        return "<:pit_orange_circle:1247721318397247570>"
    elif int(prestige / 5) == 3:
        return "<:pit_red_circle:1247721415021694977>"
    elif int(prestige / 5) == 4:
        return "<:pit_purple_circle:1247721495296475187>"
    elif int(prestige / 5) == 5:
        return "<:pit_pink_circle:1247721621788299324>"
    elif int(prestige / 5) == 6:
        return ":white_circle:"
    elif int(prestige / 5) == 7:
        return "<:pit_aqua_circle:1247721742919536690>"
    elif int(prestige / 5) == 8:
        return "<:pit_dark_blue_circle:1247721862318915585>"
    elif prestige == 45 or prestige == 46 or prestige == 47:
        return "<:pit_black_circle:1247722002429775872>"
    elif prestige == 48 or prestige == 49:
        return "<:pit_dark_red_circle:1247720152103911504>"
    else:
        return "<:pit_dark_grey_circle:1247722113553399828>"


# Calculate the xp needed for a certain level within a prestige
def calculateXPForLevel(prestige: int, level: int):
    prestigeMultiplier = float(read_specific_line("../PitStats/useful_things/pitdata/xp_multipliers.txt", prestige))
    levelTensChunk = int(level / 10)
    levelsAfterTen = level - (levelTensChunk * 10)

    totalXP = 0
    for i in range(0, levelTensChunk):
        totalXP += (prestigeMultiplier * int(
            read_specific_line("../PitStats/useful_things/pitdata/base_level_xp.txt", i))) * 10

    totalXP += (prestigeMultiplier * int(
        read_specific_line("../PitStats/useful_things/pitdata/base_level_xp.txt", levelTensChunk))) * levelsAfterTen

    return totalXP


# Calculate the current level within a prestige based off a player's total xp
def xpToLevel(prestige: int, xp: int):
    prestigeMultiplier = float(read_specific_line("../PitStats/useful_things/pitdata/xp_multipliers.txt", prestige))
    xpOfPrestige: int = 0

    for i in range(0, 13):
        for j in range(0, 10):
            xpOfPrestige += int(
                read_specific_line("../PitStats/useful_things/pitdata/base_level_xp.txt", i)) * prestigeMultiplier
            if xpOfPrestige > xp:
                return i * 10 + j
    return 120


# Calculate a player's faction tier based off their points
def calculateFactionTier(points: int):
    pointsBreakdown = [30, 100, 250, 700, 1500, 4000, 7000]

    for pointCategory in pointsBreakdown:
        if pointCategory > points:
            return pointsBreakdown.index(pointCategory)

    return 7


# Get the players from a certain leaderboard page and length
def getLeaderboardData(lb: str, players: int, page: int):
    with open("../PitStats/tokens_and_keys/PP_API_KEY.json", 'r') as f:
        data = json.load(f)
        key = data['TOKEN']

    while True:
        urlPP: str = f"https://pitpanda.rocks/api/leaderboard/{lb}?page={page}&pageSize={players}&{key}"
        leaderboard = getInfo(urlPP)

        players = []

        if not leaderboard["success"]:
            print(urlPP)
            try:
                print(leaderboard["error"])
            except KeyError:
                print("invalid url")
            return
        else:
            leaderboard = leaderboard["leaderboard"]

            for lbPlayer in leaderboard:
                players.append(formatting_functions.extract_name(lbPlayer["name"]))

        return players

# Get the first 10 players of a certain leaderboard
def getLeaderboardDataAll(lb: str, players: int):
    with open("../PitStats/tokens_and_keys/PP_API_KEY.json", 'r') as f:
        data = json.load(f)
        key = data['TOKEN']

    while True:
        urlPP: str = f"https://pitpanda.rocks/api/leaderboard/{lb}?page=0&pageSize={players}&{key}"
        leaderboard = getInfo(urlPP)

        players = []

        if not leaderboard["success"]:
            print(urlPP)
            try:
                print(leaderboard["error"])
            except KeyError:
                print("invalid url")
            return
        else:
            leaderboard = leaderboard["leaderboard"]

            for lbPlayer in leaderboard:
                players.append(formatting_functions.extract_name(lbPlayer["name"]))

        return players




