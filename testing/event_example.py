# this is an example showing how events work.
# from https://discordpy.readthedocs.io/en/stable/intro.html

# This example requires the 'message_content' intent.
# [ remember: intents are something set in the discord developer portal,
#   and are the same idea as 'permissions'. ]

import discord
import json
import copy

config_file = open('config.json', 'r')
config_json = copy.deepcopy(json.load(config_file))
config_file.close()


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(config_json["token"])