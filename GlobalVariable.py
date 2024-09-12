import logging
import sys

# Set up basic logging configuration
logging.basicConfig(
    stream=sys.stdout,  # Logs to standard output (stdout)
    level=logging.INFO,  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

import os

# Example usage
logger = logging.getLogger(__name__)

# logger.info("This is an info message.")
# logger.error("This is an error message.")

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

# CF_PASSWORD = ""
# CF_USERNAME = ""
# DISCORD_TOKEN = ""
#
# YOUTUBE_API_KEY = ""
# CHANNEL_ID = ""


CF_USERNAME = os.environ["cf_username"]
CF_PASSWORD = os.environ["cf_password"]
DISCORD_TOKEN = os.environ["discord_token"]
YOUTUBE_API_KEY = os.environ["youtube_api_key"]
CHANNEL_ID = os.environ["channel_id"]


