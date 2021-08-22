from .helpers import data
from .helpers import values

import discord

from discord.ext import commands, tasks

class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='🔧An online counter! Add "server" to the command to only count your server.')
    async def online(self, ctx, mode='all servers'):
        if mode == 'server':
            minimum = 
            maximum =
        else:
            minimum = 
            maximum = 
        
        embed = discord.Embed(
            title=f'Online Percentage for mode "{mode.title()}"',
            description=f'> {minimum}/{maximum} (**{minimum/maximum*100}%**)',
            color=values.color())
        await ctx.send(embed=embed)

    @commands.command()

def setup(client):
    client.add_cog(Tools(client))
