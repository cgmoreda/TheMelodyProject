import asyncio
import time

import requests
from bs4 import BeautifulSoup

from APICores.DiscordAPI import assignRole
from GlobalVariable import CF_PASSWORD
from LogicCores.CFHelpers import get_rank
from Melody import CF_USERNAME


async def getMaxRate(handle):
    # Codeforces API endpoint for rating history
    url = f'https://codeforces.com/api/user.rating?handle={handle}'

    try:
        # Make a request to the Codeforces API
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful
        if data['status'] == 'OK':
            # Extract rating changes
            rating_changes = data['result']
            if not rating_changes:
                return 0

            max_rating = max(change['newRating'] for change in rating_changes)
            return max_rating

    except Exception as e:
        print(e)
        return -1
#######################################################################################################

LOGIN_URL = 'https://codeforces.com/enter'
TALK_URL = 'https://codeforces.com/usertalk/with/'

# Define user-agent and other headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

DBG = 'false'


def login_to_codeforces(session):
    # Fetch the login page to get hidden inputs or CSRF tokens
    if (DBG != 'false'):
        print("Fetching login page...")
    response = session.get(LOGIN_URL, headers=HEADERS)
    if (DBG != 'false'):
        print(f"Login page status code: {response.status_code}")
        print("Login page headers:", response.headers)

        # Print the login page content (be cautious with sensitive data)
        print("Login page content snippet:", response.text[:1000])

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract hidden inputs from the login form
    hidden_inputs = soup.find_all('input', type='hidden')
    form_data = {input.get('name'): input.get('value') for input in hidden_inputs}

    # Add user credentials to the form data
    form_data['handleOrEmail'] = CF_USERNAME
    form_data['password'] = CF_PASSWORD
    form_data['remember'] = 'on'
    if (DBG != 'false'):
        print("Submitting login form with data:", form_data)
    # Submit the login form
    response = session.post(LOGIN_URL, data=form_data, headers=HEADERS)
    if (DBG != 'false'):
        print(f"Login form submission status code: {response.status_code}")
        print("Login form submission headers:", response.headers)

        # Print the response content (be cautious with sensitive data)
        print("Login form submission response snippet:", response.text[:1000])

    # Check the response
    if response.ok:
        # Fetch a page that requires login to verify success
        if (DBG != 'false'):
            print("Fetching user-specific page...")
        response1 = session.get(LOGIN_URL, headers=HEADERS)
        if (DBG != 'false'):
            print(f"User-specific page status code: {response1.status_code}")
            print("User-specific page headers:", response1.headers)

            # Print the user-specific page content (be cautious with sensitive data)
            print("User-specific page content snippet:", response1.text[:1000])

        soup1 = BeautifulSoup(response1.text, 'html.parser')

        # Check for login success indicators
        if 'Logout' in soup1.get_text() or '.Melody' in soup1.get_text():
            print("Login successful!")
            return True
        else:
            print("Login failed or not detected properly. Response text snippet:", soup1.get_text())
    else:
        print("Login failed with status code:", response.status_code)
        print("Login response text snippet:", response.text)

    return False


#############################################################################################################################################


# Check for the code on Codeforces user talk page
async def check_code_on_codeforces(session, handle, code, user_id, ctx):
    url = TALK_URL + handle
    start_time = time.time()
    timeout = 120  # 2 minute

    while time.time() - start_time < timeout:
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if code in soup.get_text():
            print(f"found {handle} for user {ctx.author}")
            await ctx.send(f'Verified successfully `{handle}`to {ctx.author}!')
            role = get_rank(await getMaxRate(handle))
            await assignRole(user_id, ctx, role)
            return

        await asyncio.sleep(5)  # Wait 10 seconds before checking again

    await ctx.send('Failed to verify.\nmake sure to send the code before 1 minute\n')


