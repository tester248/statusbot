import discord
import datetime
import time
import requests
import json
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
import asyncio # To get the exception
#^ basic imports for other features of discord.py and python ^
client = discord.Client()

client = commands.Bot(command_prefix = '.',case_insensitive=True) #put your own prefix here

@client.event
async def on_ready():
    print("bot online") #will print "bot online" in the console when the bot is online

@client.command(pass_context=True)
async def autostatus(ctx):
  try:
    await ctx.send("Server Name:")
    def name(name):
      return name.author == ctx.author and name.channel == ctx.channel
    name = await client.wait_for("message", check=name,timeout=30)

    await ctx.send("Specify IP/hostname: (add :PORT if applies)")
    def ip(ip):
      return ip.author == ctx.author and ip.channel == ctx.channel
    ip = await client.wait_for("message", check=ip,timeout=30)
  
    embed=discord.Embed(title=name.content,timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url="https://api.mcsrvstat.us/icon/"+ip.content+"")
    status = requests.get("https://api.mcsrvstat.us/simple/"+ip.content+"")
    response = requests.get("https://api.mcsrvstat.us/2/"+ip.content+"")
    if status.status_code == 200:
      embed.add_field(name="Status", value="**Online** :green_circle:", inline=False)
      data = json.loads(response.content)
      try:
        embed.add_field(name="Players", value=data["players"]["list"], inline=False)
        embed.add_field(name="Version", value=data["version"], inline=False)
      except KeyError:
        embed.add_field(name="Players", value=f'{data["players"]["online"]} / {data["players"]["max"]}', inline=False)
        embed.add_field(name="Version", value=data["version"], inline=False)
      except KeyError:
        embed.add_field(name="ERROR", value="Can't retrieve data... Is the server online? :red_circle:", inline=False)
    elif status.status_code != 200:
        embed.add_field(name="Status", value="**Offline** :red_circle:", inline=False)
    embed.set_footer(text="Statusbot made by tester248#9889")
    message = await ctx.send(embed=embed)
    while True:
      await asyncio.sleep(300)
      embed.clear_fields()
      status = requests.get("https://api.mcsrvstat.us/simple/"+ip.content+"")
      response = requests.get("https://api.mcsrvstat.us/2/"+ip.content+"")
      data = json.loads(response.content)
      embed=discord.Embed(title="Refreshing...")
      embed.set_thumbnail(url="https://media.discordapp.net/attachments/880098937959243786/902931427904081950/ezgif.com-gif-maker.gif?width=58&height=58")
      embed.set_footer(text="Statusbot made by tester248#9889")
      await message.edit(embed=embed)
      embed.clear_fields()
      await asyncio.sleep(10)


      embed=discord.Embed(title=name.content,timestamp=datetime.datetime.utcnow())
      embed.set_thumbnail(url="https://api.mcsrvstat.us/icon/"+ip.content+"")
      status = requests.get("https://api.mcsrvstat.us/simple/"+ip.content+"")
      response = requests.get("https://api.mcsrvstat.us/2/"+ip.content+"")
      if status.status_code == 200:
        embed.add_field(name="Status", value="**Online** :green_circle:", inline=False)
        data = json.loads(response.content)
        try:
          embed.add_field(name="Players", value=data["players"]["list"], inline=False)
          embed.add_field(name="Version", value=data["version"], inline=False)
        except KeyError:
          embed.add_field(name="Players", value=f'{data["players"]["online"]} / {data["players"]["max"]}', inline=False)
          embed.add_field(name="Version", value=data["version"], inline=False)
        except KeyError:
          embed.add_field(name="ERROR", value="Can't retrieve data... Is the server online? :red_circle:", inline=False)
      elif status.status_code != 200:
        embed.add_field(name="Status", value="**Offline** :red_circle:", inline=False)
      embed.set_footer(text="Statusbot made by tester248#9889")
      await message.edit(embed=embed)

      
      
      
      
  except asyncio.TimeoutError:
      await ctx.send("Sorry, you didn't reply in time!")
    
  
@client.command()
async def status(ctx):
    embed1=discord.Embed(title="TSQ Survival")
    embed1.set_thumbnail(url="https://api.mcsrvstat.us/icon/survival.testersquad.tk")
    status1 = requests.get("https://api.mcsrvstat.us/simple/survival.testersquad.tk")
    response1 = requests.get('https://api.mcsrvstat.us/2/survival.testersquad.tk')
    if status1.status_code == 200:
        embed1.add_field(name="Status", value="**Online** :green_circle:", inline=False)
        data1 = json.loads(response1.content)
        try:
            embed1.add_field(name="Players", value=data1["players"]["list"], inline=False)
        except KeyError:
            try:
                embed1.add_field(name="Players", value=f'{data1["players"]["online"]} / {data1["players"]["max"]}', inline=False)
                embed1.add_field(name="Version", value=f'{data1["software"]} {data1["version"]}', inline=False)
            except KeyError:
                try:
                    embed1.add_field(name="Version", value="Vanilla " f'{data1["version"]}', inline=False)
                except KeyError:
                    pass
    elif status1.status_code != 200:
        embed1.add_field(name="Status", value="**Offline** :red_circle:", inline=False)
    embed1.set_footer(text="Statusbot made by tester248#9889")
    await ctx.send(embed=embed1)

    embed3=discord.Embed(title="2b2t")
    embed3.set_thumbnail(url="https://api.mcsrvstat.us/icon/2b2t.org")
    status3 = requests.get("https://api.mcsrvstat.us/simple/2b2t.org")
    response3 = requests.get('https://api.mcsrvstat.us/2/2b2t.org')

    if status3.status_code == 200:
      embed3.add_field(name="Status", value="**Online** :green_circle:", inline=False)
      data3 = json.loads(response3.content)
      try:
        embed3.add_field(name="Players", value=data3["players"]["list"], inline=False)
        embed3.add_field(name="Version", value=f'{data3["software"]} {data3["version"]}', inline=False)
      except KeyError:
        embed3.add_field(name="Players", value=f'{data3["players"]["online"]} / {data3["players"]["max"]}', inline=False)
        embed3.add_field(name="Version", value=f'{data3["software"]} {data3["version"]}', inline=False)
    elif status3.status_code != 200:
      embed3.add_field(name="Status", value="**Offline** :red_circle:", inline=False)
    
    embed3.set_footer(text="Statusbot made by tester248#9889")
    await ctx.send(embed=embed3)

  
    # await ctx.send("http://mcapi.us/server/image?ip=anarchy.testersquad.ml&theme=dark&title=TSQ%20Anarchy&port=25565") 
    # await ctx.send("http://mcapi.us/server/image?ip=moddedsmp.testersquad.ml&theme=dark&title=TSQ%20ModdedSMP&port=25565")  
    # await ctx.send("http://mcapi.us/server/image?ip=mods2.testersquad.ml&theme=dark&title=TSQ%20Origins%20SMP&port=25565")  
    # await ctx.send("http://mcapi.us/server/image?ip=s2.cyberland.ml&theme=dark&title=Cyberland%20Season%202&port=25565")
  

@client.command()
async def statusof(ctx):
    await ctx.send("Server Name:")
    def name(name):
      return name.author == ctx.author and name.channel == ctx.channel
    name = await client.wait_for("message", check=name,timeout=30)

    await ctx.send("Specify IP/hostname: (add :PORT if applies)")
    def ip(ip):
      return ip.author == ctx.author and ip.channel == ctx.channel
    ip = await client.wait_for("message", check=ip,timeout=30)

    embed=discord.Embed(title=name.content)
    embed.set_thumbnail(url="https://api.mcsrvstat.us/icon/"+ip.content+"")
    status = requests.get("https://api.mcsrvstat.us/simple/"+ip.content+"")
    response = requests.get("https://api.mcsrvstat.us/2/"+ip.content+"")
    if status.status_code == 200:
      embed.add_field(name="Status", value="**Online** :green_circle:", inline=False)
      data = json.loads(response.content)
      try:
        embed.add_field(name="Players", value=data["players"]["list"], inline=False)
        embed.add_field(name="Version", value=data["version"], inline=False)
      except KeyError:
        embed.add_field(name="Players", value=f'{data["players"]["online"]} / {data["players"]["max"]}', inline=False)
        embed.add_field(name="Version", value=data["version"], inline=False)
      except KeyError:
        embed.add_field(name="ERROR", value="Can't retrieve data... Is the server online? :red_circle:", inline=False)
    elif status.status_code != 200:
        embed.add_field(name="Status", value="**Offline** :red_circle:", inline=False)
    embed.set_footer(text="Statusbot made by tester248#9889")
    await ctx.send(embed=embed)


    
@client.command()
async def ping(ctx):
    await ctx.send("pong!") #simple command so that when you type "!ping" the bot will respond with "pong!"
    
@client.command()
async def kick(ctx, member : discord.Member, arg):
    try:
        await member.kick(reason=None)
        await ctx.send("kicked "+member.mention) #simple kick command to demonstrate how to get and use member mentions
    except:
        await ctx.send("bot does not have the kick members permission!")


client.run("ODgwMDk4MjgwMzM0MzA3Mzc5.GTIsqB.9G5icVhVMYlTGuhai0h_seXp1s9IrQPkC9yNwM") #get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value. 
#to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
#enjoy!