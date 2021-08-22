from cogs.helpers import data
from cogs.helpers import values

import os
import json
import random
import discord
import asyncio
import repldiscordpy # my own package :)

from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord_components import Button, Select, SelectOption, ComponentsBot

load_dotenv()

intents = discord.Intents.all()
client = ComponentsBot(
    command_prefix=commands.when_mentioned_or(values.prefix()),
    intents=intents,
    help_command=None,
)
# ComponentsBot(client)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
   
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'Starting...  {values.prefix()}help'))
    change_status.start()

status = discord.cycle(['coded by ONLIX#1662', f'{values.prefix()}help :)'])

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_command_error(ctx, error):
    # error: 'error message'
    error_messages = {
        commands.CheckFailure: 'There was a problem with a check.',
        commands.UserInputError: 'There was a problem with your input.',
        commands.CommandNotFound: f'Command not found. Use **`{values.prefix()}help`** for a list of commands.',
        commands.MissingRequiredArgument: f'Oops, I think you [*forgo**r*** 💀](https://i.redd.it/mc9ut2313b571.jpg) an argument, go check it using **`{values.prefix()}help {ctx.message.content.replace(values.prefix(), "").split()[0]}`**', # the f-string generates the help-command for the command
        commands.TooManyArguments: f'You gave too many arguments, use this command for help: **`{values.prefix()}help {ctx.message.content.replace(values.prefix(), "").split()[0]}`**', # the f-string generates the help-command for the command
        commands.Cooldown: 'Please be patient :)',
        # commands.MessageNotFound: 'This message could not be found.',
        # commands.ChannelNotFound: 'This channel could not be found.',
        commands.NoPrivateMessage: 'This does not work in DM channels.',
        commands.MissingPermissions: 'Sorry, you don\'t have the following permission(s) to do this:',
        commands.BotMissingPermissions: 'Sorry, I don\'t have the following permission(s) to do this:',
        commands.ExtensionError: 'This is probably a bug you can\'t do anything about, but there was a problem with an extension.',
        commands.BadArgument: f'There was a problem converting one of the argument\'s type, use this command for help: **`{values.prefix()}help {ctx.message.content.replace(values.prefix(), "").split()[0]}`**', # the f-string generates the help-command for the command
    }

    error_msg = 'Unknown error.'

    # create the error message using the dict above
    for e in error_messages.keys():
        if isinstance(error, e):
            error_msg = error_messages[e]

    # other errors:
    # - too long
    if 'Invalid Form Body' in str(error):
        error_msg = 'Sorry, I can\'t send messages that long due to Discord limitations.'

    # - bug
    if 'Command raised an exception' in str(error):
        error_msg = 'Oops, our developers maybe messed up here. This is probably a bug.'

    # add detailed info
    if isinstance(error, commands.MissingPermissions) or isinstance(error, commands.BotMissingPermissions):
        error_msg += f'\n**`{", ".join(error.missing_perms)}`**\n'

    # add full error description formatted as a code text
    error_msg += '\n\n__Error message:__\n```\n' + str(error) + '\n```'

    # create a cool embed
    embed = discord.Embed(
        title='Command Error',
        description=error_msg,
        color=0xff0000
    )
    
    # send it
    await ctx.send(embed=embed)
    if values.testing_mode() or error_msg == 'Unknown error.':
        raise error # if this is a testing system, show the full error in the console

@client.command(name='commandinfo', aliases=['command', 'commands', 'help'], help='📃Display info about commands.', usage='(<command name>)')
async def commandinfo(ctx, name=None):
    if name:
        for c in client.commands:
            if name.lower() == c.name or name.lower() in list(c.aliases):
                text = f'''
                **Help:** {c.help if c.help else ' - '}
                **Usage:** {c.usage if c.usage else ' - '}
                **Aliases:** {', '.join(c.aliases) if c.aliases else ' - '}
                '''
                embed = discord.Embed(title='Command ' + c.name, color=values.color(), description=text)
                await ctx.send(embed=embed)

                return

        embed = discord.Embed(title='Command not found', color=values.color(), description='This command does not exist...')
        await ctx.send(embed=embed)
   
    else:
        def sortkey(x):
            return x.name
        
        categories = {'💡': 'Main commands', '📃': 'Information and help', '🔧': 'Tools and utilities', '🔩': 'Other and misc'}
        
        text = ''
        for category in categories.keys():
            text += f'\n{category} **{categories[category]}**\n'
            for command in sorted(client.commands, key=sortkey):
                if command.help:
                    if command.help.startswith(category):
                        if command.aliases:
                            text += f'{command.name} *({"/".join(command.aliases)})*\n'
                        else:
                            text += f'{command.name}\n'
                    # continue
                # if category == '✨' and command.help[0] not in categories.keys():
                #   if command.aliases:
                #     text += f'{command.name} *({"/".join(command.aliases)})*\n'
                #   else:
                #     text += f'{command.name}\n'

            # text += f'`{c.name}` {c.help[:50] if c.help else empty}{"..." if len(c.help) > 50 else empty}\n'

        embed = discord.Embed(title='Commands', color=values.color(), description=text)
        embed.set_footer(text='Run &help <command> for detailed info on a command')
        await ctx.send(embed=embed)

@client.command(aliases=['support'], help='🔒Invite this bot to your server!')
async def invite(ctx):
    await ctx.send(embed=discord.Embed(title='Please add me to your server :)', description='It just takes about 10 seconds and would help me out a lot! Thank you.\n\n<https://discord.com/api/oauth2/authorize?client_id=859528281257672704&permissions=3072&scope=bot>', color=values.color()))

@client.command(help='📃General Bot information.')
async def info(ctx):
    await ctx.send(embed=discord.Embed(title='FriendsCord Bot', description=f'**[Ping:](https://www.youtube.com/watch?v=bxqLsrlakK8)** {round(client.latency*1000, 2)}\n**[Source code:](https://github.com/nsde/friendscord)** open source, on my GitHub\n**[Creator(s):](https://onlix.me)** Made with <3 by onlix#1662', color=values.color()))

@client.event
async def on_message(message):
    await client.process_commands(message)

repldiscordpy.keep_alive.keep_alive(port=6969)

# load cogs
# credit: https://youtu.be/vQw8cFfZPx0

ld = ''
try:
    ld = os.listdir(os.getcwd() + '/src/cogs/')
except FileNotFoundError:
    ld = os.listdir(os.getcwd() + '/cogs/')

for filename in ld:
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv('DISCORD_TOKEN'))