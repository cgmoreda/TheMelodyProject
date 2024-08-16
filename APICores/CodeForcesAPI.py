import asyncio
from selenium import webdriver
from GlobalVariable import CF_PASSWORD, update_config_JSESSIONID
from GlobalVariable import CF_USERNAME
from GlobalVariable import jsessionid
import cloudscraper
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


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

LOGIN_URL = "https://codeforces.com/enter"
TALK_URL = "https://codeforces.com/usertalk/with/"


def check_login() -> bool:
    # Initialize Chrome options
    options = uc.ChromeOptions()
    options.headless = False  # Set to True if you want to run in headless mode

    # Start the driver
    driver = uc.Chrome(options=options)

    # Navigate to the login page
    driver.get(LOGIN_URL)

    # Wait for the page to load completely before setting the cookie
    driver.implicitly_wait(10)  # Adjust wait time if needed

    # Set the JSESSIONID cookie
    driver.add_cookie({'name': 'JSESSIONID', 'value': jsessionid,
                       'domain': '.codeforces.com'})  # Use '.codeforces.com' for subdomains

    # Refresh the page to apply the cookie
    driver.refresh()

    # Wait for the page to load completely
    driver.implicitly_wait(10)  # Adjust wait time if needed

    # Parse the page source
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Close the driver
    driver.quit()

    # Check if "Logout" is in the page text
    if "Logout" in soup.get_text():
        return True
    else:
        return False


def login_to_codeforces():
    # Start a Chrome session with undetected-chromedriver
    if check_login():
        print("Already logged in!")
        return
    try:
        options = uc.ChromeOptions()
        options.headless = False
        driver = uc.Chrome(options=options)
        driver.get(LOGIN_URL)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        if "Logout" in soup.get_text() or ".Melody" in soup.get_text():
            print("Login successful!")
            return True
        # Wait for the username field to be present
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "handleOrEmail"))
        )
        username.click()
        username.send_keys(CF_USERNAME)

        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password.click()
        password.send_keys(CF_PASSWORD)

        remember = driver.find_element(By.ID, "remember")
        remember.click()

        login_button = driver.find_element(By.CLASS_NAME, "submit")
        login_button.click()

        time.sleep(5)  # Wait for page to load

        # Check if login was successful
        soup = BeautifulSoup(driver.page_source, "html.parser")
        if "Logout" in soup.get_text() or ".Melody" in soup.get_text():

            cookies = driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'JSESSIONID':
                    update_config_JSESSIONID(cookie['value'])
                    break
            print("Login successful!")
            return True
        else:
            print("Login failed or not detected properly.")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        driver.quit()


#############################################################################################################################################


# Check for the code on Codeforces user talk page
async def check_code_on_codeforces(
        handle: str, code: str
) -> bool:
    session = requests.Session()
    session.cookies.set('JSESSIONID', jsessionid)
    url = TALK_URL + handle
    timeout = 120  # 2 minute

    for _ in range(timeout // 5):  # max 2 minute
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        if code in soup.get_text():
            return True
        await asyncio.sleep(5)  # Wait 10 seconds before checking again

    return False


login_to_codeforces()
