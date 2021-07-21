import re
import discord
from discord.ext import commands
import datetime, time
import hmtai
from dotenv import load_dotenv

load_dotenv()
import os

import anime_images_api
from discord_components import *


client = commands.Bot(command_prefix=";")
anime = anime_images_api.Anime_Images()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=";help"))
    DiscordComponents(client)

@client.command()
async def test(ctx):
    await ctx.send("test Command")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! Bot Latency is {round(client.latency*1000)} ms")

@client.command()
async def hug(ctx,member:discord.Member=None):
    if not member:
        return await ctx.send("Please specify A Member to hug!")

    em = discord.Embed(title=f"{ctx.author.display_name} hugs {member.display_name}! <3").set_image(url=anime.get_sfw("hug"))
    await ctx.send(embed=em)

@client.command()
async def cuddle(ctx,member:discord.Member=None):
    if not member:
        return await ctx.send("Please specify A Member to cuddle with!")

    em = discord.Embed(title=f"{ctx.author.display_name} cuddles with {member.display_name}! How Cute!").set_image(url=anime.get_sfw("hug"))
    await ctx.send(embed=em)


@client.command()
async def hentai(ctx):
    em = discord.Embed(title=f"There ya go!").set_image(url=anime.get_nsfw("hentai"))
    if ctx.channel.is_nsfw():
        await ctx.send(embed=em)
    else:
        await ctx.send(f"BONK! Go to Horny Jail (And maybe run this Command in an NSFW Channel next Time)")



class uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 
        global startTime #global variable to be used later in cog
        startTime = time.time() # snapshot of time when listener sends on_ready

    #create a command in the cog
    @commands.command(name='uptime')
    async def uptime(self,ctx):

        # what this is doing is creating a variable called 'uptime' and assigning it
        # a string value based off calling a time.time() snapshot now, and subtracting
        # the global from earlier
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        await ctx.send(uptime)

@client.command()
async def userinfo(ctx,member:discord.Member=None):
    if not member: member = ctx.author

    em = discord.Embed(title=f"User Info for {member}",color=member.color)
    em.add_field(name="Name",value=member.display_name)
    em.add_field(name="ID",value=member.id)
    em.set_thumbnail(url=member.avatar_url)
    em.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar_url)

    await ctx.send(embed=em)

client.add_cog(uptime(client))

TOKEN = os.getenv("TOKEN")

client.run(TOKEN)
