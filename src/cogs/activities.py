from .helpers import data
from .helpers import values

import discord

from discord.ext import commands

class Activities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['playing'], help='🔧Search for Game activities, or leave the argument blank get an overview.', usage='(<activity>)')
    async def games(self, ctx, *activity):
        if activity:
            activity = ' '.join(activity)
        
        activitiy_overview = {}
        already_saved_members = []

        for server in self.client.guilds:
            for user in server.members:
                if (not user.id in already_saved_members) and user.activity and (not user.bot) and (not isinstance(user.activity, discord.CustomActivity)):
                    name = user.activity.name

                    try:
                        activitiy_overview[name].append(f'{user.mention}')
                    except KeyError:
                        activitiy_overview[name] = [f'{user.mention}']
                    
                    already_saved_members.append(user.id)

        activitiy_overview = {k:v for k,v in sorted(activitiy_overview.items())}

        if not activity:
            embed = discord.Embed(title='Activities', color=values.color())

            for game in activitiy_overview.keys():
                embed.add_field(name=game, value=' '.join(activitiy_overview[game]), inline=False)

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='People playing ' + activity, color=values.color())
            try:
                embed.add_field(name='Playing now', value=' '.join(activitiy_overview[activity]), inline=False)
            except KeyError:
                embed.add_field(name='Playing now', value='*[nobody]*', inline=False)

            await ctx.send(embed=embed)

    @commands.command(aliases=['talking'], help='🔧Get an overview of voice channels.')
    async def voice(self, ctx):
        voice_overview = {}
        
        for server in self.client.guilds:
            for user in server.members:
                if user.voice and not user.bot and not isinstance(user.voice.channel, discord.DMChannel):
                    name = f'[{user.guild.name}] {user.voice.channel.name}'

                    try:
                        voice_overview[name].append(f'{user.mention}')
                    except KeyError:
                        voice_overview[name] = [f'{user.mention}']

        voice_overview = {k:v for k,v in sorted(voice_overview.items())}

        embed = discord.Embed(title='Voice channels', description='*[nobody feels like talking]*' if not voice_overview.keys() else '', color=values.color())

        for channel in voice_overview.keys():
            embed.add_field(name=channel, value=' '.join(voice_overview[channel]), inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Activities(client))
