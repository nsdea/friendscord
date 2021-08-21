from .helpers import data
from .helpers import values

import discord

from discord.ext import commands, tasks

class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Tools(client))
