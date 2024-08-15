import random
import string

import requests

from APICores import CodeForcesAPI
from APICores.CodeForcesAPI import login_to_codeforces, check_code_on_codeforces
from GlobalVariable import ranks
from Melody import bot


def get_rank(rt):
    rating = int(rt)
    rank_index = (rating >= 1200) + (rating >= 1400) + (rating >= 1600) + (rating >= 1900) + \
                 (rating >= 2100) + (rating >= 2300) + (rating >= 2400) + (rating >= 2600) + (rating >= 3000)

    return ranks[rank_index]

# Generate a 32-character alphanumeric code
def generate_code():
    return 'I_love_Melody_' + ''.join(random.choices(string.ascii_letters + string.digits, k=32))


async def cfverify(ctx,handle):
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


async def CFrateof(ctx, handle):
    maxRate = await CodeForcesAPI.getMaxRate(handle)

    if (maxRate == -1):
        await ctx.send(f'Error fetching for handle {handle}.')
        return
    if (maxRate == 0):
        await ctx.send(f'No rating history found for handle {handle}.')
        return
    await ctx.send(f'The maximum rating for Codeforces handle `{handle}` is {maxRate}.')
    await ctx.send(f'`{handle}` is {get_rank(maxRate)}.')
