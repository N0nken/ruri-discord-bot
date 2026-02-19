from dotenv import load_dotenv
import os
import datetime

import discord
from discord.ext import commands
from discord.ext import tasks

import configs
import mu_api as api


load_dotenv()
token = os.getenv("DISCORD_TOKEN")


class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user}!")

        try:
            guild = discord.Object(id=1473070081700528170)
            synced = await self.tree.sync(guild=guild)
            print(f"synced {len(synced)} commands to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing commands: {e}")

        if not update.is_running():
            update.start()
            print("Auto-update task started")


# |------------------------------------------------|
# |---------------------CONFIG---------------------|
# |------------------------------------------------|
intents = discord.Intents.default()
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1473070081700528170)
UPDATE_RATE_MINUTES = 1
UPDATE_MESSAGE = "@{role} New chapter (ch. {chapter_number}) is now out for {manga_name}! \nLatest chapter is ch. {latest_chapter}"


# |------------------------------------------------|
# |--------------------COMMANDS--------------------|
# |------------------------------------------------|
@client.tree.command(name="set_update_channel", description=
                     "Makes the bot send the updates in the channel this command is run in.", 
                     guild=GUILD_ID)
async def set_update_channel(interaction: discord.Interaction):
    if not configs.is_guild_registered(str(interaction.guild_id)):
        configs.register_guild(configs.Guild(str(interaction.guild_id), interaction.guild.name))

    configs.set_channel(str(interaction.guild_id), str(interaction.channel_id))
    await interaction.response.send_message(f"Will now send updates in **{interaction.channel.name}**")
    print(f"updated channel for {interaction.guild.name} to {interaction.channel.name}")


@client.tree.command(name="track", description=
                     "Start tracking a manga (role_id is not implemented)", 
                     guild=GUILD_ID)
async def track_manga(interaction: discord.Interaction, manga_name: str, manga_updates_id: int, role_id: int = -1, latest_chapter: int = -1):
    if not configs.is_guild_registered(str(interaction.guild_id)):
        configs.register_guild(configs.Guild(str(interaction.guild_id), interaction.guild.name))
    
    try:
        configs.register_manga(str(interaction.guild_id), configs.Manga(manga_name, manga_updates_id, role_id, latest_chapter, str(datetime.date.today())))
        await interaction.response.send_message(f"Started tracking **{manga_name}**")
    except Exception as e:
        await interaction.response.send_message(e)


@client.tree.command(name="untrack", description="Stop tracking a manga", 
                     guild=GUILD_ID)
async def untrack_manga(interaction: discord.Interaction, manga_name: str):
    if not configs.is_guild_registered(str(interaction.guild_id)):
        configs.register_guild(configs.Guild(str(interaction.guild_id), interaction.guild.name))
    
    try:
        configs.remove_manga(str(interaction.guild_id), manga_name)
        await interaction.response.send_message(f"Stopped tracking **{manga_name}**")
    except Exception as e:
        await interaction.response.send_message(e)


@client.tree.command(name="tracked_manga", description=
                     "Shows a list of all tracked manga", 
                     guild=GUILD_ID)
async def tracked_manga(interaction: discord.Interaction):
    if not configs.is_guild_registered(str(interaction.guild_id)):
        await interaction.response.send_message("No manga is being tracked in this server")
        return
    
    try:
        manga = configs.get_tracked_manga(str(interaction.guild_id))
        
        response = f"Tracked manga for **{interaction.guild.name}**"
        for m in manga:
            response += f"\n* **{m.name}**"

        await interaction.response.send_message(response)
    except Exception as e:
        await interaction.response.send_message(e)


# |------------------------------------------------|
# |----------------------TASKS---------------------|
# |------------------------------------------------|
@tasks.loop(minutes=UPDATE_RATE_MINUTES)
async def update():
    # go through each guild
    # ...go through each manga
    # ... ...mangaupdates api check if new chapter released
    # ... ...if new chapter
    # ... ... ...send update
    # ... ...else
    # ... ... ...nothing

    guild_ids = configs.get_registered_guilds()

    for guild_id in guild_ids:
        if guild_id == "0": # skip template
            continue

        channel = client.get_channel(int(configs.get_guild_config(guild_id).channel))

        for manga in configs.get_tracked_manga(guild_id):
            # mangaupdates api call
            latest_chapter = api.get_latest_chapter(manga.id, manga.latest_chapter)
            
            if latest_chapter == -1:
                continue
            
            configs.set_latest_chapter(guild_id, manga.name, latest_chapter)
            await channel.send(
                UPDATE_MESSAGE.format(role=manga.name, 
                                      chapter_number=str(latest_chapter if latest_chapter != int(latest_chapter) else int(latest_chapter)), 
                                      manga_name=manga.name,
                                      latest_chapter=manga.latest_chapter))


# |------------------------------------------------|
# |---------------------EVENTS---------------------|
# |------------------------------------------------|


# |------------------------------------------------|
# |---------------------LAUNCH---------------------|
# |------------------------------------------------|
client.run(token)