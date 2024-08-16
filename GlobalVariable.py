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
jsessionid = ""


def load_config():
    global CF_PASSWORD, CF_USERNAME, DISCORD_TOKEN, jsessionid

    with open("config.json") as config_file:
        config = json.load(config_file)

    CF_USERNAME = config["cf_username"]
    CF_PASSWORD = config["cf_password"]
    DISCORD_TOKEN = config["discord_token"]
    jsessionid = config["JSESSIONID"]


def update_config_JSESSIONID(_jsessionid: str):
    global jsessionid

    with open("config.json") as config_file:
        config = json.load(config_file)

    config["JSESSIONID"] = _jsessionid

    with open("config.json", 'w') as f:
        json.dump(config, f, indent=4)

    load_config()


load_config()
