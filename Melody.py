import time
import discord
import requests
from discord.ext import commands

from GlobalVariable import DISCORD_TOKEN
from LogicCores.CFHelpers import cfverify, CFrateof

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Bot is online!')
    channel = bot.get_channel(11785991736800051701)  # Replace with your channel ID
    if channel:
        await channel.send('Hello, I am online!')
    else:
        print('Channel not found')


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent loops
    if message.author == bot.user:
        return
    print(f"{message.author} sent ({message.content})")

    await message.channel.send('Hello!')
    # Process commands if you have any command handlers
    await bot.process_commands(message)


@bot.command()
async def rateof(ctx, handle: str):
    await CFrateof(ctx, handle)


@bot.command()
async def verify(ctx, handle: str):
    await cfverify(ctx, handle)


# Initialize bot state
bot.user_codes = {}
bot.user_handles = {}
bot.run(DISCORD_TOKEN)
