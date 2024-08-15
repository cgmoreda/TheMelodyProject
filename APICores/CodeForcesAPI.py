import asyncio
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from requests.api import request
from browsermobproxy import Server
from selenium.webdriver.common.proxy import Proxy, ProxyType

from GlobalVariable import CF_PASSWORD
from GlobalVariable import CF_USERNAME
import requests

server = Server("/path/to/browsermob-proxy")
server.start()
proxy = server.create_proxy()

# Set up Selenium WebDriver to use the proxy
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))

SESSION = webdriver.Chrome(options=chrome_options)

# Intercept and modify requests
proxy.blacklist(".*", 404)  # Block all requests as an example
proxy.headers({'If-None-Match': None})  # Remove specific header

async def get_max_rate(handle: str) -> int:
    # Codeforces API endpoint for rating history
    url = f"https://codeforces.com/api/user.rating?handle={handle}"

    try:
        # Make a request to the Codeforces API
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful
        if data["status"] == "OK":
            # Extract rating changes
            rating_changes = data["result"]
            if not rating_changes:
                return 0

            max_rating = max(change["newRating"] for change in rating_changes)
            return max_rating

    except BaseException as e:
        print(e)
    return -1


#######################################################################################################

LOGIN_URL = "http://localhost:3000"
TALK_URL = "https://codeforces.com/usertalk/with/"

# Define user-agent and other headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

DBG = False


def login_to_codeforces(session = SESSION):
    # Fetch the login page to get hidden inputs or CSRF tokens
    if DBG:
        print("Fetching login page...")
    response = session.get(LOGIN_URL) 
    # if DBG:
    #     print(f"Login page status code: {response.status_code}")
    #     print("Login page headers:", response.headers)
    #
    #     # Print the login page content (be cautious with sensitive data)
    #     print("Login page content snippet:", response.text[:1000])

    
    # soup = BeautifulSoup(session.page_source, "html.parser")
    #
    # # Extract hidden inputs from the login form
    # hidden_inputs = soup.find_all("input", type="hidden")
    # form_data = {input.get("name"): input.get("value") for input in hidden_inputs}
    #
    # # Add user credentials to the form data
    # form_data["handleOrEmail"] = CF_USERNAME
    # form_data["password"] = CF_PASSWORD
    # form_data["remember"] = "on"
    # if DBG:
    #     print("Submitting login form with data:", form_data)
    # # Submit the login form
    session.get(LOGIN_URL) 
    username = session.find_element(By.ID,"handleOrEmail")
    username.click()
    username.send_keys(CF_USERNAME)
    sleep(3)

    
    password = session.find_element(By.ID,"password")
    password.click()
    sleep(2)
    password.send_keys(CF_PASSWORD)
    sleep(1)
    remember = session.find_element(By.ID,"remember")
    remember.click()
    sleep(2)
    login_button = session.find_element(By.CLASS_NAME,"submit")
    login_button.click()
    # if DBG:
    #
    #     print(f"Login form submission status code: {response.status_code}")
    #     print("Login form submission headers:", response.headers)
    #
    #     # Print the response content (be cautious with sensitive data)
    #     print("Login form submission response snippet:", response.text[:1000])
    # Check the response
    if True:
        # Fetch a page that requires login to verify success
        if DBG:
            print("Fetching user-specific page...")
        response1 = session.get(LOGIN_URL)
        sleep(5)
            # Print the user-specific page content (be cautious with sensitive data)
        soup1 = BeautifulSoup(session.page_source, "html.parser")

        # Check for login success indicators
        if "Logout" in soup1.get_text() or ".Melody" in soup1.get_text():
            print("Login successful!")
            return True
        else:
            print(
                "Login failed or not detected properly. Response text snippet:",
                soup1.get_text(),
            )
        return False
    else:
        print("Login failed with status code:", response.status_code)
        print("Login response text snippet:", response.text)


#############################################################################################################################################


# Check for the code on Codeforces user talk page
async def check_code_on_codeforces(
     handle: str, code: str
) -> bool:
    url = TALK_URL + handle
    timeout = 120  # 2 minute

    for _ in range(timeout // 5):  # max 2 minute
        response = SESSION.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        if code in soup.get_text():
            return True
        await asyncio.sleep(5)  # Wait 10 seconds before checking again

    return False
login_to_codeforces(SESSION)
