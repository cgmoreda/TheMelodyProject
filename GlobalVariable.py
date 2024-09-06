import logging
import sys
import json

# Set up basic logging configuration
logging.basicConfig(
    stream=sys.stdout,  # Logs to standard output (stdout)
    level=logging.INFO,  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Example usage
logger = logging.getLogger(__name__)

#logger.info("This is an info message.")
#logger.error("This is an error message.")

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
YOUTUBE_API_KEY = ""
CHANNEL_ID = ""

def load_config():
    global CF_PASSWORD, CF_USERNAME, DISCORD_TOKEN, jsessionid, YOUTUBE_API_KEY, CHANNEL_ID

    with open("config.json") as config_file:
        config = json.load(config_file)

    CF_USERNAME = config["cf_username"]
    CF_PASSWORD = config["cf_password"]
    DISCORD_TOKEN = config["discord_token"]
    jsessionid = config["JSESSIONID"]
    YOUTUBE_API_KEY = config["youtube_api_key"]
    CHANNEL_ID = config["channel_id"]

def update_config_JSESSIONID(_jsessionid: str):
    global jsessionid

    with open("config.json") as config_file:
        config = json.load(config_file)

    config["JSESSIONID"] = _jsessionid

    with open("config.json", 'w') as f:
        json.dump(config, f, indent=4)

    load_config()


load_config()
