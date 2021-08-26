from .helpers import data
from .helpers import values

import discord

from discord.ext import commands, tasks

class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='🔧An online counter! Add "server" to the command to only count your server.')
    async def online(self, ctx, mode='servers'):
        mode = mode.lower()

        if mode == 'server':
            minimum = len([m for m in ctx.guild.members if (str(m.status) == 'online' and (not m.bot))])
            maximum = len([m for m in ctx.guild.members if (not m.bot)])

        elif mode == 'bots':
            minimum = len([m for m in ctx.guild.members if (str(m.status) == 'online' and (m.bot))])
            maximum = len([m for m in ctx.guild.members if (m.bot)])

        else:
            pass
            # minimum = len([m for m in set(self.client.get_all_members()) if (str(m.status) == 'online' and (m.bot))])
            # maximum = len([m for m in set(self.client.get_all_members()) if (m.bot)])
        
        embed = discord.Embed(
            title=f'Online Percentage for {"Bots in " if mode == "bots" else ""}{"this Server" if mode != "servers" else "all Servers I have access to"}',
            description=f'> {minimum}/{maximum} (**{round(minimum/maximum*100)}%**)',
            color=values.color()
        ).set_footer(text=f'Bots are {"not" if mode != "bots" else "exclusively"} counted')

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Tools(client))
