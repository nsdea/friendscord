import os
import json
import discord
import asyncio

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

COLOR = discord.Color(0x713afc)

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('&'), intents=intents, help_command=None)

def get_data(path, key=None):
    data = {}

    try:
        open(path)
        data = json.loads(open(path).read())
    except FileNotFoundError:
        open(path, 'w').write(json.dumps({}))
    except json.decoder.JSONDecodeError:
        open(path, 'w').write(json.dumps({}))
    
    if key:
        try:
            return data[key]
        except KeyError:
            try:
                return data[str(key)]
            except:
                return 0
    else:
        return data

def set_data(path, value, key=None):
  data = get_data(path=path)

  if key:
    data[key] = value
  else:
    data = value

  open(path, 'w').write(json.dumps(data))
  return value

def change_data(path, value, key=None):
    # if get_data(path=path, key=key):
    set_data(path=path, value=(get_data(path=path, key=key)+value), key=key)
    # else:
        # set_data(path=path, value=value, key=key)

def parse_boolean(text: str):
    '''Translates human language yes/no/do/dont into a boolean to improve usability'''

    if text.lower() in ['no', 'don\'t', 'dont', 'off', 'stop', '0', 'false', 'inactive', 'offline']:
        return False
    return text 

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

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
        embed = discord.Embed(title='Command ' + c.name, color=COLOR, description=text)
        await ctx.send(embed=embed)

        return

    embed = discord.Embed(title='Command not found', color=COLOR, description='This command does not exist...')
    await ctx.send(embed=embed)
   
  else:
    def sortkey(x):
      return x.name
    
    categories = {'💡': 'Main commands', '📃': 'Information and help', '🔧': 'Tools and utilities', '🔒': 'Friends', '🔩': 'Other and misc', '✨': 'New and experimental'}
    
    text = ''
    for category in categories.keys():
      text += f'\n{category} **{categories[category]}**\n'
      for command in sorted(client.commands, key=sortkey):
        if command.help.startswith(category):
          if command.aliases:
            text += f'{command.name} *({"/".join(command.aliases)})*\n'
          else:
            text += f'{command.name}\n'
          continue
        if category == '✨' and command.help[0] not in categories.keys():
          if command.aliases:
            text += f'{command.name} *({"/".join(command.aliases)})*\n'
          else:
            text += f'{command.name}\n'

      # text += f'`{c.name}` {c.help[:50] if c.help else empty}{"..." if len(c.help) > 50 else empty}\n'

    embed = discord.Embed(title='Commands', color=COLOR, description=text)
    embed.set_footer(text='Run &help <command> for detailed info on a command')
    await ctx.send(embed=embed)

@client.command(aliases=['playing'], help='🔧Search for Game activities, or leave the argument blank get an overview.', usage='(<activity>)')
async def games(ctx, *activity):
    if activity:
        activity = ' '.join(activity)
    
    activitiy_overview = {}

    for server in client.guilds:
        for user in server.members:
            if user.activity and not user.bot and not isinstance(user.activity, discord.CustomActivity):
                name = user.activity.name

                try:
                    activitiy_overview[name].append(f'{user.mention}')
                except KeyError:
                    activitiy_overview[name] = [f'{user.mention}']

    if not activity:
        embed = discord.Embed(title='Activities', color=COLOR)

        for game in activitiy_overview.keys():
            embed.add_field(name=game, value=' '.join(activitiy_overview[game]), inline=False)

        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='People playing ' + activity, color=COLOR)
        try:
            embed.add_field(name='Playing now', value=' '.join(activitiy_overview[activity]), inline=False)
        except KeyError:
            embed.add_field(name='Playing now', value='*[nobody]*', inline=False)

        await ctx.send(embed=embed)

@client.command(aliases=['talking'], help='🔧Get an overview of voice channels.')
async def voice(ctx):
    voice_overview = {}
    
    for server in client.guilds:
        for user in server.members:
            if user.voice and not user.bot and not isinstance(user.voice.channel, discord.DMChannel):
                name = f'[{user.guild.name}] {user.voice.channel.name}'

                try:
                    voice_overview[name].append(f'{user.mention}')
                except KeyError:
                    voice_overview[name] = [f'{user.mention}']

    embed = discord.Embed(title='Voice channels', description='*[nobody feels like talking]*' if not voice_overview.keys() else '', color=COLOR)

    for channel in voice_overview.keys():
        embed.add_field(name=channel, value=' '.join(voice_overview[channel]), inline=False)

    await ctx.send(embed=embed)

@client.command(aliases=['addfriend'], help='💡Send someone a friend request.', usage='(<userping/mention>)')
async def friend(ctx, user: discord.Member):
    if ctx.author == user:
        msg = await ctx.send(embed=discord.Embed(title='You successfully (not) made friends with yourself', description=f'Do you also wish to merry yourself and make kids?', color=COLOR))
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'

        try:
            await client.wait_for('reaction_add', check=check, timeout=20)
        except asyncio.TimeoutError:
            pass
        else:
            await msg.edit(embed=discord.Embed(title='Great', description=f'What am I programming at this moment', color=COLOR).set_footer(text='pls help!!11'))
        return

    try:
        already_friends = ctx.author.id in get_data('friends.json', key=user.id) and user.id in get_data('friends.json', value=ctx.author.id)
    except TypeError:
        already_friends = False

    try:
        requested = ctx.author.id in get_data('friends.json', key=user.id)
    except TypeError:
        requested = False

    if already_friends:
        await ctx.send(embed=discord.Embed(title='You\'re already friends', description=f'{user.mention} & {ctx.author.mention} are already friends.', color=COLOR).add_footer(text=f'If you don\'t like each other, do **.unfriend @{user.name}**'))       

    elif requested:
        if not get_data('friends.json').get(ctx.author.id):
            set_data('friends.json', value=[], key=ctx.author.id)

        value = get_data('friends.json', key=ctx.author.id)
        value.append(user.id)
        set_data('friends.json', value=value, key=ctx.author.id)

        await ctx.send(embed=discord.Embed(title='Accepted friend request', description=f'{user.mention} is now your friend!', color=COLOR))       
    
    else:
        if not get_data('friends.json').get(ctx.author.id):
            set_data('friends.json', value=[], key=ctx.author.id)

        value = get_data('friends.json', key=ctx.author.id)
        value.append(user.id)
        set_data('friends.json', value=value, key=ctx.author.id)

        await ctx.send(embed=discord.Embed(title='Sent friend request', description=f'{user.mention} has to accept your friend request using `&friend @{ctx.author.name}` .', color=COLOR))


@client.command(aliases=['friendlist'], help='💡List a user\'s friends.')
async def friends(ctx, user: discord.Member=None):
    if not user:
        user = ctx.author
    
    text = ''
    if get_data('friends.json', key=user.id):
        for friend in get_data('friends.json', key=user.id):
            try:
                text += f'> {client.get_user(friend).name}\n'
            except:
                pass
    else:
        text = 'Lonely like a Wumpus :('

    await ctx.send(embed=discord.Embed(title=f'{user.name}\'s friends', description=text, color=COLOR))

@client.command(aliases=['removefriend'], help='💡Remove someone as a friend.')
async def unfriend(ctx, user: discord.Member):
    try:
        already_friends = ctx.author.id in get_data('friends.json', key=user.id) and user.id in get_data('friends.json', value=ctx.author.id)
    except TypeError:
        already_friends = False
   
    if already_friends:
        await ctx.send(embed=discord.Embed(title='Please add me to your server :)', description='It just takes about 10 seconds and would help me out a lot! Thank you.\n\n<https://discord.com/api/oauth2/authorize?client_id=859528281257672704&permissions=3072&scope=bot>', color=COLOR))
    else:
        await ctx.send(embed=discord.Embed(title='You\'re not even friends', description='How am I supposed to remove you then?', color=COLOR))

@client.command(aliases=['support'], help='🔒Invite this bot to your server!')
async def invite(ctx):
    await ctx.send(embed=discord.Embed(title='Please add me to your server :)', description='It just takes about 10 seconds and would help me out a lot! Thank you.\n\n<https://discord.com/api/oauth2/authorize?client_id=859528281257672704&permissions=3072&scope=bot>', color=COLOR))

@client.command(help='📃General Bot information.')
async def info(ctx):
    await ctx.send(embed=discord.Embed(title='FriendsCord Bot', description=f'**[Ping:](https://www.youtube.com/watch?v=bxqLsrlakK8)** {round(client.latency*1000, 2)}\n**[Source code:](https://github.com/nsde/friendscord)** open source, on my GitHub\n**[Creator(s):](https://onlix.me)** Made with <3 by onlix#1662', color=COLOR))

@client.event
async def on_message(message):
    await client.process_commands(message)

client.run(os.getenv('TOKEN'))