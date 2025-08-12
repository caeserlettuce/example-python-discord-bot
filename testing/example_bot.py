# this is an example bot file.
# from https://discordpy.readthedocs.io/en/stable/intro.html

# This example required the 'message_content' intent.

import discord
import json
import copy

config_file = open('config.json', 'r')
config_json = copy.deepcopy(json.load(config_file))
config_file.close()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

client.run(config_json["token"])