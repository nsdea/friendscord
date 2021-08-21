import socket
import discord

def color():
    return discord.Color(0x713afc)

def prefix():
    return '&'

def testing_mode():
    return socket.gethostname() in ['uwuntu']