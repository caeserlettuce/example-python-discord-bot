

import discord
from discord import app_commands
from discord.ext.commands import Bot, Context
from PIL import Image, ImageDraw
import requests

import json
import copy

config_file = open('config.json', 'r')
config_json = copy.deepcopy(json.load(config_file))
config_file.close()

wl_file = open('burrito.json', 'r')
burrito = copy.deepcopy(json.load(wl_file))
whitelist = burrito["whitelist"]
wl_file.close()

debug = True

def deb(msg):
    if debug == True:
        print(msg)


def png2jpg(file_name:str, trans_color: tuple):
    """
    convert png file to jpg file
    :param file_name: png file name
    :param trans_color: set transparent color in jpg image
    :return:
    """
    with file_name as im:
        image = im.convert("RGBA")
        datas = image.getdata()
        newData = []
        for item in datas:
            if item[3] == 0:  # if transparent
                newData.append(trans_color)  # set transparent color in jpg
            else:
                newData.append(tuple(item[:3]))
        image = Image.new("RGB", im.size)
        image.getdata()
        image.putdata(newData)
        return image

def listin(string_in, list_in):
    return_value = False
    for phrase in list_in:
        if phrase in string_in:
            return_value = True
    return return_value


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
intents.message_content = True
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'logged in as {client.user} (ID: {client.user.id})')
    print("------")



@client.event
async def on_message(message):

    if message.author == client.user: # if its NOT the bot
        return

    if str(message.channel) == "general":   # if its in general
        deb("channel passed")
    else:
        return

    if str(message.author) in whitelist:    # if the sender is authorized
        deb("whitelist passed")
    else:
        return

    if str(message.content) == 'hello':
        print("message is hello")
        await message.channel.send('bello ppoy banana ... .')

    if "|" in str(message.content):
        # text message to appeario

        msg_split = str(message.content).split("|")
        name_in = msg_split[0]
        msg_split.pop(0)
        msg = "|".join(msg_split)

        # text MESSAGE!!!



        return

    contains_name = False
    for name in burrito["names"]:
        if name in str(message.content):
            contains_name = name
    
    if contains_name != False:
        # message CONTAINS A NAME!!
        if len(message.attachments) > 0:
            # message contains an ATTACHMENT!!
            msg_str = str(message.content)
            msg = msg_str.split(" ")
            img_url = str(message.attachments[0].url)
            scaler = "fit"     #default is crop
            cropr = 2

            if listin(msg, ["stretch", "crop", "preserve", "fit"]):
                if "stretch" in msg:
                    scaler = "stretch"
                elif "crop" in msg:
                    scaler = "crop"
                elif "preserve" in msg or "fit" in msg:
                    scaler = "preserve"
            if listin(msg, ["top", "left", "center", "bottom", "right"]):
                if "top" in msg or "left" in msg:
                    cropr = 1
                elif "center" in msg:
                    cropr = 2
                elif "bottom" in msg or "right" in msg:
                    cropr = 3

            # IMAGE OPERATIONS

            bg = Image.new("RGBA", burrito["resolution"], (0, 0, 0, 255))
            im = Image.open(requests.get(img_url, stream=True).raw)
            im = im.convert("RGBA")
            
            og_w, og_h = im.size


            if scaler == "stretch":
                im = im.resize(burrito["resolution"])
                # im.show()
            elif scaler == "crop":
                
                bg_big = 0
                bg_sma = 0
                og_big = 0
                og_sma = 0
                scale_height = 0

                bg_ratio = burrito["resolution"][0] / burrito["resolution"][1]
                og_ratio = og_w / og_h

                print(bg_ratio)
                print(og_ratio)

                # if og ratio is smaller than bg ratio, image is taller than bg
                # if og ratio is bigger than bg ratio, image is wider than bg

                
                # michael reeves:    2.13846153 \ wider ratio \ scale by height
                # LANDSCAPE 800x480: 1.66666666
                # hammond ranger:    1.33333333 \ taller ratio \ scale by width

                
                # hammond ranger:    1.33333333 \ wider ratio \ scale by height
                # gravity falls:     0.66666666 \ wider ratio \ scale by height
                # PORTRAIT 480x800:  0.6
                # nick hi:           0.11991869 \ taller ratio \ scale by width
                
                if og_ratio > bg_ratio: # wider ratio, scale by height
                    scale_height = True
                    bg_big = burrito["resolution"][1]
                    bg_sma = burrito["resolution"][0]
                    og_big = og_h
                    og_sma = og_w
                else:                   # taller ratio, scale by width
                    scale_height = False
                    bg_big = burrito["resolution"][0]
                    bg_sma = burrito["resolution"][1]
                    og_big = og_w
                    og_sma = og_h

                # for these variables, "big" is the axis being scaled on. (the side that is NOT cropped)
                # "sma" (small) is the other axis. (the side that IS cropped)


                # ======   SCALING   ======


                scale_factor = bg_big / og_big      # get the scale factor

                new_big = int(og_big * scale_factor)
                new_sma = int(og_sma * scale_factor)

                if new_sma % 2 != 0:
                    new_sma = new_sma + 1   # prevent odd numbers from messin things up

                resize_resolution = (new_big, new_sma)  # this is assuming its scaled by width
                if scale_height == True:
                    resize_resolution = (new_sma, new_big)  # this corrects that if it isn't

                im = im.resize(resize_resolution)

                # ======   CROPPING   ======

                crop_removal = int((new_sma - bg_sma) / 2)

                crop_shift = 0  # this is for if you select top or bottom or left or right

                if cropr == 1: # top/left
                    crop_shift = 0 - crop_removal
                elif cropr == 3: # bottom/right
                    crop_shift = crop_removal

                crop_points = (0, crop_removal + crop_shift, new_big, new_sma - crop_removal + crop_shift)    # this is again assuming its scaled by width
                if scale_height == True:
                    crop_points = (crop_removal + crop_shift, 0, new_sma - crop_removal + crop_shift, new_big)    # this is again un-assuming that assumption

                im = im.crop(crop_points)

                im = im.resize(burrito["resolution"])
                
                # just to make sure its exactly the right size (like if the size is one pixel off or something)
            elif scaler == "preserve" or scaler == "fit":
                
                bg_big = 0
                bg_sma = 0
                og_big = 0
                og_sma = 0
                
                bg_ratio = burrito["resolution"][0] / burrito["resolution"][1]
                og_ratio = og_w / og_h

                taller = False

                if og_ratio > bg_ratio: # wider ratio, scale by width
                    taller = True
                    bg_big = burrito["resolution"][0]
                    bg_sma = burrito["resolution"][1]
                    og_big = og_w
                    og_sma = og_h
                else:                   # taller ratio, scale by height
                    taller = False
                    bg_big = burrito["resolution"][1]
                    bg_sma = burrito["resolution"][0]
                    og_big = og_h
                    og_sma = og_w

                # ======   SCALING   ======

                scale_factor = bg_big / og_big      # get the scale factor

                new_big = int(og_big * scale_factor)
                new_sma = int(og_sma * scale_factor)

                if new_sma % 2 != 0:
                    new_sma = new_sma + 1   # prevent odd numbers from messin things up

                resize_resolution = (new_sma, new_big)  # this is assuming its scaled by height
                if taller == True:
                    resize_resolution = (new_big, new_sma)  # this corrects that if it isn't

                im = im.resize(resize_resolution)

                center_tm = (int( (burrito["resolution"][0] / 2) - (resize_resolution[0] / 2)), int( (burrito["resolution"][1] / 2) - (resize_resolution[1] / 2)) )

                fg = Image.new("RGBA", burrito["resolution"], (0, 0, 0, 255))
                fg.paste(im, center_tm)

                im = fg.resize(burrito["resolution"]) # just to be sure
                


            im = im.convert("RGBA")
            bg = bg.convert("RGBA")




            im = Image.alpha_composite(bg, im)
            # im.show()

            im = im.convert("RGB")
            im.save("image.jpg")

        await message.channel.send(file=discord.File('image.jpg'))
        # await message.channel.send("f")
    






client.run(config_json["token"])