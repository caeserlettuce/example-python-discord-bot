# from https://discordpy.readthedocs.io/en/stable/intro.html

# This example required the 'message_content' intent.


import discord
from discord.ext import commands
import json
import copy

config_file = open('config.json', 'r')
config_json = copy.deepcopy(json.load(config_file))
config_file.close()

description = 'An example bot to showcase the discord.ext.commands extension module.'


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="?", description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):

    print(message.content)

    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')










bot.run(config_json["token"])