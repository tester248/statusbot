from typing import Optional, List
import discord
from discord import app_commands
from discord.ext import commands
import datetime
import aiohttp
import json
import asyncio
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables and validate them
load_dotenv()

# Check for required environment variables
if not os.getenv('TOKEN'):
    raise ValueError(
        "No TOKEN found in environment variables.\n"
        "1. Copy .env.example to .env\n"
        "2. Add your bot token to the .env file"
    )

class MinecraftStatus(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        
    async def setup_hook(self):
        # Clear existing commands
        if self.application_id:
            self.tree.clear_commands(guild=None)
            await self.tree.sync()
        
        # Add cogs here later if needed
        print("Bot is setting up...")

class MinecraftServerModal(discord.ui.Modal, title="Minecraft Server Status"):
    servername = discord.ui.TextInput(
        label="Server Name",
        placeholder="Enter the name of the server...",
        required=True
    )
    
    serverip = discord.ui.TextInput(
        label="Server IP/Hostname",
        placeholder="Enter the IP or hostname (with port if needed)...",
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.mcsrvstat.us/2/{self.serverip.value}") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        embed = await create_server_status_embed(
                            self.servername.value,
                            self.serverip.value,
                            data
                        )
                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send("Failed to get server status. Please check the IP/hostname and try again.")
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}")

async def create_server_status_embed(server_name: str, server_ip: str, data: dict) -> discord.Embed:
    embed = discord.Embed(
        title=server_name,
        timestamp=datetime.datetime.utcnow()
    )
    
    embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{server_ip}")
    
    if data.get("online", False):
        embed.add_field(name="Status", value="**Online** :green_circle:", inline=False)
        
        # Player info
        players = data.get("players", {})
        if "list" in players:
            embed.add_field(name="Players", value="\n".join(players["list"]), inline=False)
        else:
            embed.add_field(
                name="Players",
                value=f"{players.get('online', 0)} / {players.get('max', 0)}",
                inline=False
            )
        
        # Version info
        version = []
        if "software" in data:
            version.append(data["software"])
        if "version" in data:
            version.append(data["version"])
        
        if version:
            embed.add_field(name="Version", value=" ".join(version), inline=False)
        
    else:
        embed.add_field(name="Status", value="**Offline** :red_circle:", inline=False)
    
    embed.set_footer(text="Minecraft Status Bot")
    return embed

class ServerStatusView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.green, custom_id="refresh_status")
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        if not message.embeds:
            await interaction.response.send_message("No server status to refresh!", ephemeral=True)
            return
            
        embed = message.embeds[0]
        server_name = embed.title
        server_ip = embed.thumbnail.url.split("/")[-1]
        
        await interaction.response.defer()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.mcsrvstat.us/2/{server_ip}") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        new_embed = await create_server_status_embed(server_name, server_ip, data)
                        await message.edit(embed=new_embed)
                        await interaction.followup.send("Server status refreshed!", ephemeral=True)
                    else:
                        await interaction.followup.send("Failed to refresh server status.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)

bot = MinecraftStatus()

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")
    try:
        bot.add_view(ServerStatusView())  # Add the persistent view
    except Exception as e:
        print(f"Error adding persistent view: {e}")

@bot.tree.command(name="status")
async def status(interaction: discord.Interaction):
    """Check the status of a Minecraft server"""
    modal = MinecraftServerModal()
    await interaction.response.send_modal(modal)

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    """Check if the bot is responsive"""
    await interaction.response.send_message("🏓 Pong!")

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))
#to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
#enjoy!
