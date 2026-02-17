import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import configs

load_dotenv()
token = os.getenv("DISCORD_TOKEN")


class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

        try:
            guild = discord.Object(id=1473070081700528170)
            synced = await self.tree.sync(guild=guild)
            print(f"synced {len(synced)} commands to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing commands: {e}")



intents = discord.Intents.default()
client = Client(command_prefix="!", intents=intents)

guild_id = discord.Object(id=1473070081700528170)


@client.tree.command(name="hello", description="say hello", guild=guild_id)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")



print(token)
client.run(token)