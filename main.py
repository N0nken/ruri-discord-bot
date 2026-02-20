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
            synced = await self.tree.sync()
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

DEV_GUILD_ID = discord.Object(id=1473070081700528170)
UPDATE_RATE_MINUTES = 30
UPDATE_MESSAGE = "@{role} New chapter (ch. {chapter_number}) is now out for {manga_name}! \nLatest chapter is ch. {latest_chapter}"
GENERIC_ERROR_MESSAGE = "An error occurred when trying to reach the server"

# |------------------------------------------------|
# |--------------------COMMANDS--------------------|
# |------------------------------------------------|
# setup 
@client.tree.command(name="setup", description=
                     "(REQUIRED) Enables the bot for this server.")
async def setup(interaction: discord.Interaction):
    if configs.is_guild_registered(interaction.guild_id):
        await interaction.response.send_message("Bot has already been set up for this server", ephemeral=True)
        return
    
    configs.register_guild(configs.Guild(interaction.guild_id, interaction.guild.name, interaction.channel_id))
    await interaction.response.send_message("Bot has now been set up for this server. Start tracking manga by running /track")
    print(f"set up bot for [{interaction.guild.name}]")

# set update channel
@client.tree.command(name="set_update_channel", description=
                     "Makes the bot send the updates in the channel this command is run in.")
async def set_update_channel(interaction: discord.Interaction):
    if not configs.is_guild_registered(interaction.guild_id):
        await interaction.response.send_message("Bot has not been set up for this server", ephemeral=True)
        return

    try:
        configs.set_channel(interaction.guild_id, interaction.channel_id)
    except:
        await interaction.response.send_message(GENERIC_ERROR_MESSAGE, ephemeral=True)

    await interaction.response.send_message(f"Will now send updates in **{interaction.channel.name}**")
    print(f"updated channel for {interaction.guild.name} to {interaction.channel.name}")

# track
@client.tree.command(name="track", description=
                     "Start tracking a manga (role_id is not implemented)")
async def track_manga(interaction: discord.Interaction, manga_updates_id: int, role_id: int = -1):
    if not configs.is_guild_registered(interaction.guild_id):
        await interaction.response.send_message("Bot has not been set up for this server", ephemeral=True)
        return
    
    manga_name = api.get_manga_name(manga_updates_id)
    if manga_name == "":
        await interaction.response.send_message(f"Couldn't find manga {manga_updates_id}", ephemeral=True)

    latest_chapter = api.get_latest_chapter(manga_updates_id, -1)

    try:
        configs.track_manga(interaction.guild_id, configs.Manga(manga_name, manga_updates_id, role_id, latest_chapter, str(datetime.date.today())))
        await interaction.response.send_message(f"Started tracking **{manga_name}**")
    except Exception as e:
        await interaction.response.send_message(f"Failed to start tracking **{manga_name}**", ephemeral=True)

# untrack
@client.tree.command(name="untrack", description=
                     "Stop tracking a manga")
async def untrack_manga(interaction: discord.Interaction, manga_id: int):
    if not configs.is_guild_registered(interaction.guild_id):
        await interaction.response.send_message("Bot has not been set up for this server", ephemeral=True)
        return

    try:
        manga = configs.get_manga_details(manga_id)
    except:
        await interaction.response.send_message(GENERIC_ERROR_MESSAGE, ephemeral=True)

    try:
        configs.stop_tracking_manga(interaction.guild_id, manga_id)
        await interaction.response.send_message(f"Stopped tracking **{manga.name}**")
    except Exception as e:
        await interaction.response.send_message(f"Failed to stop tracking {manga_id}. Use /tracked_manga to make sure this server is tracking it before trying again.", ephemeral=True)

# tracked manga
@client.tree.command(name="tracked_manga", description=
                     "Shows a list of all tracked manga")
async def tracked_manga(interaction: discord.Interaction):
    if not configs.is_guild_registered(interaction.guild_id):
        await interaction.response.send_message("Bot has not been set up for this server", ephemeral=True)
        return
    
    try:
        manga = configs.get_tracked_manga(interaction.guild_id)
        
        response = f"Tracked manga for **{interaction.guild.name}**"
        for m in manga:
            response += f"\n* **{m.name}**"

        await interaction.response.send_message(response)
    except Exception as e:
        await interaction.response.send_message(GENERIC_ERROR_MESSAGE, ephemeral=True)


# |------------------------------------------------|
# |----------------------TASKS---------------------|
# |------------------------------------------------|
# check for updates continuously
@tasks.loop(minutes=UPDATE_RATE_MINUTES)
async def update():
    # for each manga
    # ... if updated
    # ... ... for every guild tracking this manga
    # ... ... ... send uptead

    manga = configs.get_all_manga()

    for manga in manga:
        # mangaupdates api call
        latest_chapter = api.get_latest_chapter(manga.id, manga.latest_chapter)
        
        if latest_chapter == -1:
            continue

        configs.set_latest_chapter(manga.id, latest_chapter)
        channels = configs.get_update_channel_ids_for_servers_tracking_manga(manga.id)

        for channel_id in channels:
            channel = client.get_channel(channel_id)

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