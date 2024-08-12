import time
import discord
import requests
from discord.ext import commands, tasks
import random
import string
import aiohttp
import asyncio
import json
import requests
from bs4 import BeautifulSoup

###################################################################################################################################################
# Load configs
with open('config.json') as config_file:
    config = json.load(config_file)

# Initialize the bot
bot = commands.Bot(command_prefix='!')

CF_USERNAME = config['cf_username']
CF_PASSWORD = config['cf_password']
DISCORD_TOKEN = config['discord_token']

ranks = ["Newbie", "Pupil", "Specialist", "Expert", "Candidate Master",
         "Master", "International Master", "Grandmaster", "International Grandmaster",
         "Legendary Grandmaster"]


###################################################################################################################################################
def get_rank(rt):
    rating = int(rt)
    rank_index = (rating >= 1200) + (rating >= 1400) + (rating >= 1600) + (rating >= 1900) + \
                 (rating >= 2100) + (rating >= 2300) + (rating >= 2400) + (rating >= 2600) + (rating >= 3000)

    return ranks[rank_index]


###################################################################################################################################################


# Generate a 32-character alphanumeric code
def generate_code():
    return 'I_love_Melody_' + ''.join(random.choices(string.ascii_letters + string.digits, k=32))


###################################################################################################################################################

# Initialize the bot

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


############################################################################################################################
# online message
@bot.event
async def on_ready():
    print('Bot is online!')
    channel = bot.get_channel(11785991736800051701)  # Replace with your channel ID
    if channel:
        await channel.send('Hello, I am online!')
    else:
        print('Channel not found')


############################################################################################################################
# saying hello

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent loops
    if message.author == bot.user:
        return
    print(f"{message.author} sent ({message.content})")
    # Example: Reply to any message with "Hello!" if it contains the word "hi"
    # if 'hi' in message.content.lower():
    #    await message.channel.send('Hello!')

    # Process commands if you have any command handlers
    await bot.process_commands(message)


#################################################################################################################################

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


#################################################################################################################################
# getdetails of a handle
@bot.command()
async def rateof(ctx, handle: str):
    maxRate = await getMaxRate(handle)

    if (maxRate == -1):
        await ctx.send(f'Error fetching for handle {handle}.')
        return
    if (maxRate == 0):
        await ctx.send(f'No rating history found for handle {handle}.')
        return
    await ctx.send(f'The maximum rating for Codeforces handle `{handle}` is {maxRate}.')
    await ctx.send(f'`{handle}` is {get_rank(maxRate)}.')


##################################################################################################################
# log in

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


##################################################################################################################

async def assignRole(user_id, ctx, role_name):
    # Fetch the guild (server) object
    guild = ctx.guild
    # Fetch the member by ID
    # 620368287393513493
    member = guild.get_member(int(user_id))
    if member is None:
        await ctx.send(f'User with ID {user_id} not found in this server.')
        return

    for rl in ranks:
        role = discord.utils.get(guild.roles, name=rl)
        if role is not None:
            await member.remove_roles(role)

    role = discord.utils.get(guild.roles, name=role_name)
    # Check if role is found
    if role is None:
        await ctx.send(f'Role `{role_name}` not found.')
        return
    # Check if the bot has permission to manage roles
    if ctx.guild.me.guild_permissions.manage_roles:
        # Check if the role is lower in the hierarchy than the bot's highest role
        if role.position < ctx.guild.me.top_role.position:
            # Assign the role to the member
            await member.add_roles(role)
            await ctx.send(f'Assigned role `{role_name}` to {member.mention}.')
        else:
            await ctx.send('I cannot assign this role because it is higher than my highest role.')
    else:
        await ctx.send('I do not have permission to manage roles.')


##################################################################################################################

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


##################################################################################################################
@bot.command()
async def verify(ctx, handle: str):
    # Generate a 32-character alphanumeric code
    code = generate_code()

    # Send the code to the user
    await ctx.send(f'{ctx.author} your code for handle {handle} is: ```{code}``` \n'
                   f'send the code to: https://codeforces.com/profile/.Melody')

    # Store the code and handle
    bot.user_codes[ctx.author.id] = code
    bot.user_handles[ctx.author.id] = handle

    # Notify user that checking will start
    await ctx.send(f'Checking Codeforces for handle `{handle}`...')

    # Start checking Codeforces
    with requests.Session() as session:
        if login_to_codeforces(session):
            await check_code_on_codeforces(session, handle, code, ctx.author.id, ctx)
        else:
            await ctx.send('Failed to log in to Codeforces. try again later')



# Initialize bot state
bot.user_codes = {}
bot.user_handles = {}

#################################################################################################################

bot.run(DISCORD_TOKEN)
