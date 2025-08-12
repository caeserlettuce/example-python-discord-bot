

import discord
from discord import app_commands
from discord.ext.commands import Bot, Context

import json
import copy

config_file = open('config.json', 'r')
config_json = copy.deepcopy(json.load(config_file))
config_file.close()


MY_GUILD = discord.Object(id=config_json["guildId"])


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

        
    
    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # this copies the global commands over to your guild.
        await self.tree.sync()
        self.tree.copy_global_to(guild=MY_GUILD)
        # self.tree.clear_commands(guild=MY_GUILD)
        # self.tree.sync()
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'logged in as {client.user} (ID: {client.user.id})')
    print("------")









client.run(config_json["token"])