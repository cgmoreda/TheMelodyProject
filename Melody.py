import discord
from discord.ext import commands
from APICores import CodeForcesAPI
from APICores.YoutubeAPI import check_new_video
from GlobalVariable import DISCORD_TOKEN
from LogicCores.CFHelpers import cf_rateof, get_cfverify

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1178599173680005170


@bot.event
async def on_ready():
    check_new_video.start(bot)
    print("Bot is online!")
    await CodeForcesAPI.ensure_login()
    channel = bot.get_channel(CHANNEL_ID)  # Replace with your channel ID
    if channel:
        await channel.send("Hello, I am online!")
    else:
        print("Channel not found")


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent loops
    if message.author == bot.user:
        return
    print(f"{message.author} sent ({message.content})")
    if 'melody' in message.content:
        await message.channel.send("Hello!")
    # Process commands if you have any command handlers
    await bot.process_commands(message)


m = {"user_codes": {}, "user_handles": {}}

bot.command()(cf_rateof)
bot.command()(get_cfverify(m))

# Initialize bot state
bot.run(DISCORD_TOKEN)
