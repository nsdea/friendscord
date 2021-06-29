import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

client = commands.Bot(commands=commands.when_mentioned_or('&'))

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.command(help='Search for activities, or leave the argument blank get an overview.', usage='(<activity>)')
async def activities(ctx, *activity):
    activity = ' '.join(activity)
    activitiy_overview = {}

    for user in ctx.guild:
        if user.activity:
            name = user.activity.name

            try:
                activitiy_overview[].append
            except KeyError:
                
            

client.run(os.getenv('TOKEN'))
