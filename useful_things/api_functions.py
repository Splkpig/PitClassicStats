import requests
import json

# Get the Hypixel API key
def getKey():
    API_FILE = open("../PitStats/tokens_and_keys/API_KEY.json", "r")
    API_KEY = json.loads(API_FILE.read())["API_KEY"]
    return API_KEY

# Get the info from an API
def getInfo(call):
    r = requests.get(call)
    return r.json()

