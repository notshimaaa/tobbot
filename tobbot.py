import json
import os
import random
import re

import discord
from discord.ext import commands

# setting permissions for the bot
intents = discord.Intents.default()
intents.message_content = True

# defining your bot
tobbot = commands.Bot(command_prefix='.', intents=intents)

toby_emoji = "<:toby:1200591140437643275>"
ryan_emoji = "<:ryan:1200594423172583475>"
minson_emoji = "<:manmaru:1202815295434006648>"
mouse_gang = toby_emoji + ryan_emoji + minson_emoji

# ####################################
# ~~~~~~~~~ EVENTS ~~~~~~~~~~~~~~~~~~~
# ####################################

@tobbot.event
async def on_ready():
    """Runs everytime the bot starts"""
    print(f'We have logged in as {tobbot.user}')
    
    # tobbot.yap = True # default
    # tobbot.cage = False # default
    
    # the gang = {} # it's supposed to look like gang1: T, gang2: F, gang3: T
    # for (all of the servers tobbot is in):
    # append them to the gang dict, automatically assigning them to True
    #
    tobbot.yap_gang = {}  # this is a dictionary that will hold the yap status of different servers
    tobbot.cage_gang = {}  # this is a dictionary that will hold the cage status of different servers
    for guild in tobbot.guilds:
        print(guild.name, guild.id)
        tobbot.yap_gang[guild.id] = True
        tobbot.cage_gang[guild.id] = False
    print(tobbot.yap_gang)
    print(tobbot.cage_gang)
    await tobbot.change_presence(activity=discord.Game('does not do much, is just cute :)'))

@tobbot.event
async def on_message(msg):
    if msg.author == tobbot.user:
        return

    this_guilds_cage = tobbot.cage_gang[msg.guild.id]
    if this_guilds_cage == True:
        await tobbot.process_commands(msg)
        return

    if "toby" in msg.content.lower():
        if msg.content.lower() != ".toby":
            await toby_mention(msg)

    if "rat" in msg.content.lower():
        rat_count = msg.content.lower().count("rat")
        if rat_count > 10:
            await msg.reply("😡😡😡That's a lot of rats.😡😡😡")
        else:
            for _ in range(rat_count):
                await rat_fact(msg)

    # alternatives to the black magic below:
    # >>> if "mouse" in msg.content.lower() or "mice" in msg.content.lower():
    # or:
    # >>> for word in ("mouse", "mice"):
    # >>>     if word in msg.content.lower():
    if any(word in msg.content.lower() for word in ("mouse", "mice")):
        await mouse_fact(msg)

    if "rodent" in msg.content.lower():
        await msg.reply(":rat::rat::rat:")

    if "ray" in msg.content.lower():
        this_guilds_yap = tobbot.yap_gang[msg.guild.id]
        if this_guilds_yap == True:
            ray_rat = re.sub("[Rr][Aa][Yy]", "***rat***", msg.content)
            await msg.reply(f"*did you mean,* '{ray_rat}'?")
        elif this_guilds_yap == False:
            pass

    # after processing all the text in our custom way above...
    # process bot commands (messages starting with ".")
    await tobbot.process_commands(msg)
    
@tobbot.event
async def on_guild_join(guild):
    """
    Runs when the bot joins a new server. Sets the default values for the
    yap and cage switches to True and False respectively.
    """
    tobbot.yap_gang[guild.id] = True
    tobbot.cage_gang[guild.id] = False
    
# ####################################
# ~~~~~~~ HELPER FUNCTIONS ~~~~~~~~~~~
# ####################################

async def rat_fact(msg):
    # facts from https://github.com/RileyAbr/rat-facts-Discord-Bot/tree/main
    # import rat facts from json file in utf-8 format
    rat_facts = "./data/rat_facts.json"

    # to open a file (the old way!!)
    # file = open(rat_facts, "r", encoding="utf-8")
    # rat_facts = json.load(file)
    # file.close()

    # file open and close automatically
    with open(rat_facts, "r", encoding="utf-8") as file:
        rat_facts = json.load(file)

    # send a random rat fact
    await msg.reply(random.choice(rat_facts))

async def mouse_fact(msg):
    await msg.reply(f"Mice {toby_emoji} are {ryan_emoji} cute {minson_emoji}!")

async def toby_mention(msg):
    # upload a random toby image from the "./toby_photos" folder
    toby_photos_dir = "./data/toby_photos"
    toby_photos = os.listdir(toby_photos_dir)
    toby_photo = random.choice(toby_photos)

    # send the image
    await msg.reply(file=discord.File(f"{toby_photos_dir}/{toby_photo}"))

# ####################################
# ~~~~~~~ COMMANDS ~~~~~~~~~~~~~~~~~~~
# ####################################

@tobbot.command(aliases=['tobbot', 'tob','tobe'])
async def toby(ctx):
    await ctx.reply("use rodent-related words wisely. <:rat_tu_y:1214342472751259728>")

@tobbot.command()
async def invite(ctx):
    invite = ("https://discord.com/oauth2/authorize?client_id=1268249395304861717&"
              "scope=bot+applications.commands&permissions=412317240384")
    await ctx.reply(f"here you go - {invite}")

@tobbot.command()
async def yap(ctx):
    """toggle the autocorrect switch"""
    # get the server id from "ctx.guild.id"
    # ctx.guild = the guild that the command was sent in
    # ctx.guild.id = the id of the guild that the command was sent in

    tobbot.yap_gang[ctx.guild.id] = not tobbot.yap_gang[ctx.guild.id]

    # tobbot.yap = not tobbot.yap
    # we have tobbot.yap_gang to keep track of the yap status of different servers
    if tobbot.yap_gang[ctx.guild.id] == True:
        await ctx.reply("Prepare for trouble and make it double.")
    elif tobbot.yap_gang[ctx.guild.id] == False:
        await ctx.reply("sad mouse noises.")

@tobbot.command()
async def yapstat(ctx):
    """status update of the goofy spelling autocorrect"""
    yap = tobbot.yap_gang[ctx.guild.id]
    if yap == True:
        await ctx.reply("autocorrect is currently on.")
    elif yap == False:
        await ctx.reply("autocorrect is currently off.")
    print(ctx.guild.id, yap, tobbot.yap_gang)

@tobbot.command()
async def cage(ctx):
    """toggle the cage switch"""
    tobbot.cage_gang[ctx.guild.id] = not tobbot.cage_gang[ctx.guild.id]
    if tobbot.cage_gang[ctx.guild.id] == True:
        await ctx.reply("here he comes. :)")
    elif tobbot.cage_gang[ctx.guild.id] == True:
        await ctx.reply("there he goes. :(")

@tobbot.command()
async def cagestat(ctx):
    """is the mouse in the cage or not"""
    cage = tobbot.cage_gang[ctx.guild.id]
    if cage == True:
        await ctx.reply("shhh, he is currently sleeping. do you wish to wake him up?")
    elif cage == False:
        await ctx.reply("he is on the loose. he is among us.")

@tobbot.command()
async def vibe(ctx):
    """vibe check"""
    await ctx.reply(random.choice(["大吉: mouse vibrates excitedly <:rat_tu_y:1214342472751259728>",
                                   "大凶: mouse shakes in terror <a:mouseShake:1199964736234721280>",
                                   "末吉: mouse blinks in boredom <:bruh:1200584402271477842>"]))

# read api key from file called "api_key.txt"
with open("api_key.txt", "r") as f:
    api_key = f.read()

# run the bot with the api key
tobbot.run(api_key)
