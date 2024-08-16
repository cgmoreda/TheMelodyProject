import json

ranks = [
    "Newbie",
    "Pupil",
    "Specialist",
    "Expert",
    "Candidate Master",
    "Master",
    "International Master",
    "Grandmaster",
    "International Grandmaster",
    "Legendary Grandmaster",
]

CF_PASSWORD = ""
CF_USERNAME = ""
DISCORD_TOKEN = ""
YOUTUBE_API_KEY = ""
CHANNEL_ID = ""


def loadjson():
    global CF_PASSWORD, CF_USERNAME, DISCORD_TOKEN, YOUTUBE_API_KEY, CHANNEL_ID

    with open("config.json") as config_file:
        config = json.load(config_file)

    CF_USERNAME = config["cf_username"]
    CF_PASSWORD = config["cf_password"]
    DISCORD_TOKEN = config["discord_token"]
    YOUTUBE_API_KEY = config["youtube_api_key"]
    CHANNEL_ID = config["channel_id"]


loadjson()
