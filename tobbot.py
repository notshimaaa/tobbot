import json
import os
import random

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


@tobbot.event
async def on_ready():
    """Runs everytime the bot starts"""
    print(f'We have logged in as {tobbot.user}')
    tobbot.annoy = True # default
    await tobbot.change_presence(activity=discord.Game('does not do much, is just cute :)'))

@tobbot.event
async def on_message(msg):
    if msg.author == tobbot.user:
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

    if any(word in msg.content.lower() for word in ("mouse", "mice")):
        await mouse_fact(msg)

    if "rodent" in msg.content.lower():
        await msg.reply(":rat::rat::rat:")

    if "ray" in msg.content.lower():
        if tobbot.annoy == True:
            ray_rat = msg.content.replace("ray", "***rat***")
            await msg.reply(f"*did you mean,* '{ray_rat}'?")
        elif tobbot.annoy == False:
            pass

    # after processing all the text in our custom way above...
    # process bot commands (messages starting with ".")
    await tobbot.process_commands(msg)

async def rat_fact(msg):
    # facts from https://github.com/RileyAbr/rat-facts-Discord-Bot/tree/main
    # import rat facts from json file in utf-8 format
    rat_facts = "./data/rat_facts.json"
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

@tobbot.command(aliases=['tobbot'])
async def toby(ctx, arg1=None, arg2=None, arg3=None):
    await ctx.reply(f"{toby_emoji} squeak {ctx.author.mention}! squeak squeak squeak. squeak. {ryan_emoji}")

@tobbot.command()
async def invite(ctx):
    invite = ("https://discord.com/oauth2/authorize?client_id=1268249395304861717&"
              "scope=bot+applications.commands&permissions=412317240384")
    await ctx.reply(invite)

@tobbot.command()
async def annoy(ctx):
    """toggle the ray-rat switch"""
    tobbot.annoy = not tobbot.annoy
    if tobbot.annoy == True:
        await ctx.reply("Prepare for trouble and make it double.")
    elif tobbot.annoy == False:
        await ctx.reply("sad mouse noises.")

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
