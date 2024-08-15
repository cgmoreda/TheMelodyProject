import time
from typing import ChainMap
import discord
import requests
from discord.ext import commands

from GlobalVariable import DISCORD_TOKEN
from LogicCores.CFHelpers import  CFrateof, get_cfverify

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1178599173680005170


@bot.event
async def on_ready():
    print("Bot is online!")
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

    await message.channel.send("Hello!")
    # Process commands if you have any command handlers
    await bot.process_commands(message)



bot.user_codes = {}
bot.user_handles = {}

bot.command()(CFrateof)
bot.command()(get_cfverify(bot))


# Initialize bot state
bot.run(DISCORD_TOKEN)
