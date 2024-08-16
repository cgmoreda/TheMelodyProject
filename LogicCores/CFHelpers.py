import random
import string

import discord
from discord.ext.commands import Bot
import requests

from APICores.DiscordAPI import assignRole

from APICores import CodeForcesAPI
from APICores.CodeForcesAPI import login_to_codeforces, check_code_on_codeforces, check_login
from GlobalVariable import ranks


def get_rank(rating: int):
    rank_index = (
            +(rating >= 1200)
            + (rating >= 1400)
            + (rating >= 1600)
            + (rating >= 1900)
            + (rating >= 2100)
            + (rating >= 2300)
            + (rating >= 2400)
            + (rating >= 2600)
            + (rating >= 3000)
    )

    return ranks[rank_index]


# Generate a 32-character alphanumeric code
def generate_code():
    return "I_love_Melody_" + "".join(
        random.choices(string.ascii_letters + string.digits, k=32)
    )


def get_cfverify(bot):
    async def cfverify(ctx, handle):
        nonlocal bot

        # Generate a 32-character alphanumeric code
        code = generate_code()

        # Send the code to the user
        await ctx.send(
            f"""{ctx.author} your code for handle {handle} is: ```{code}``` \n
            send the code to: https://codeforces.com/profile/.Melody"""
        )

        # Store the code and handle
        bot["user_codes"][ctx.author.id] = code
        bot["user_handles"][ctx.author.id] = handle

        # Notify user that checking will start
        await ctx.send(f"Checking Codeforces for handle `{handle}`...")

        login_to_codeforces()

        if check_login():
            if await check_code_on_codeforces(
                    handle,
                    code,
            ):
                print(f"found {handle} for user {ctx.author}")
                await ctx.send(f"Verified successfully `{handle}`to {ctx.author}!")
                role = get_rank(await CodeForcesAPI.get_max_rate(handle))
                user_id = ctx.author.id
                await assignRole(user_id, ctx, role)
            else:
                await ctx.send(
                    "Failed to verify.\nmake sure to send the code before 1 minute"
                )
        else:
            await ctx.send("Failed to log in to Codeforces. try again later")

    return cfverify


async def cf_rateof(ctx, handle):
    maxRate = await CodeForcesAPI.get_max_rate(handle)

    if maxRate == -1:
        await ctx.send(f"Error fetching for handle {handle}.")
        return
    if maxRate == 0:
        await ctx.send(f"No rating history found for handle {handle}.")
        return
    await ctx.send(f"The maximum rating for Codeforces handle `{handle}` is {maxRate}.")
    await ctx.send(f"`{handle}` is {get_rank(maxRate)}.")
