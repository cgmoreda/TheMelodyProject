import logging
import sys
import os
import json

from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

# Set up basic logging configuration once
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Codeforces ranks (static list)
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

# Load configuration from config.json if it exists
config = {}
config_path = "config.json"
if os.path.isfile(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)

# Read each value from JSON first, then fall back to environment variables
DISCORD_TOKEN   = config.get("discord_token")   or os.getenv("discord_token", "")
CF_USERNAME     = config.get("cf_username")     or os.getenv("cf_username", "")
CF_PASSWORD     = config.get("cf_password")     or os.getenv("cf_password", "")
JSESSIONID      = config.get("JSESSIONID")      or os.getenv("JSESSIONID", "")
YOUTUBE_API_KEY = config.get("youtube_api_key") or os.getenv("youtube_api_key", "")
CHANNEL_ID      = config.get("channel_id")      or os.getenv("channel_id", "")

# Validate required settings
missing = []
if not DISCORD_TOKEN:
    missing.append("DISCORD_TOKEN (discord_token)")
if not CF_USERNAME:
    missing.append("CF_USERNAME (cf_username)")
if not CF_PASSWORD:
    missing.append("CF_PASSWORD (cf_password)")
if not YOUTUBE_API_KEY:
    missing.append("YOUTUBE_API_KEY (youtube_api_key)")

# JSESSIONID can be optional depending on your use case

if missing:
    logger.error("Missing configuration for: %s", ", ".join(missing))
    raise RuntimeError(f"Please set the following in config.json or environment: {', '.join(missing)}")

# Example usage:
# logger.info("Configuration loaded successfully.")
# logger.debug("Ranks list: %s", ranks)
# logger.debug("JSESSIONID: %s", JSESSIONID)
