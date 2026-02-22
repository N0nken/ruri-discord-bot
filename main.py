from dotenv import load_dotenv
import os
import datetime

import discord
from discord.ext import commands
from discord.ext import tasks

import db
import manga_updates_api as api


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
UPDATE_MESSAGE = "@{role} Chapter **{chapter_number}** is now out for **{manga_name}**!"
GENERIC_ERROR_MESSAGE = "An error occurred when trying to reach the server"

# |------------------------------------------------|
# |--------------------COMMANDS--------------------|
# |------------------------------------------------|
# setup 
@client.tree.command(name="setup", description=
                     "(REQUIRED) Enables the bot for this server.")
async def setup(interaction: discord.Interaction):
    if db.is_guild_registered(interaction.guild_id):
        await interaction.response.send_message("Bot has already been set up for this server", ephemeral=True)
        return
    
    try:
        db.register_guild(db.Guild(interaction.guild_id, interaction.guild.name, interaction.channel_id))
    except:
        await interaction.response.send_message(GENERIC_ERROR_MESSAGE, ephemeral=True)
        return

    await interaction.response.send_message("Bot has now been set up for this server. Start tracking manga by running /track")
    print(f"set up bot for [{interaction.guild.name}]")

# set update channel
@client.tree.command(name="set_update_channel", description=
                     "Makes the bot send the updates in the channel this command is run in.")
async def set_update_channel(interaction: discord.Interaction):
    if not db.is_guild_registered(interaction.guild_id):
        await interaction.response.send_message("Bot has not been set up for this server", ephemeral=True)
        return

    try:
        db.set_channel(interaction.guild_id, interaction.channel_id)
    except:
        await interaction.response.send_message(GENERIC_ERROR_MESSAGE, ephemeral=True)
        return

    await interaction.response.send_message(f"Will now send updates in **{interaction.channel.name}**")
    print(f"updated channel for {interaction.guild.name} to {interaction.channel.name}")

# track
@client.tree.command(name="track", description=
                     "Start tracking a manga (role_id is not implemented)")
async def track_manga(interaction: discord.Interaction, manga_updates_id: str, role_id: int = -1):
    if not db.is_guild_registered(interaction.guild_id):
        await interaction.response.send_message("Bot has not been set up for this server", ephemeral=True)
        return
    
    manga_name = api.get_manga_name(manga_updates_id)
    if manga_name == "":
        await interaction.response.send_message(f"Couldn't find manga {manga_updates_id}", ephemeral=True)
        return

    try:
        db.track_manga(interaction.guild_id, db.Manga(manga_name, manga_updates_id, role_id))
        await interaction.response.send_message(f"Started tracking **{manga_name}**")
    except Exception as e:
        await interaction.response.send_message(f"Failed to start tracking **{manga_name}**", ephemeral=True)

# untrack
@client.tree.command(name="untrack", description=
                     "Stop tracking a manga")
async def untrack_manga(interaction: discord.Interaction, manga_id: str):
    if not db.is_guild_registered(interaction.guild_id):
        await interaction.response.send_message("Bot has not been set up for this server", ephemeral=True)
        return

    try:
        manga = db.get_manga_details(manga_id)
    except:
        await interaction.response.send_message(GENERIC_ERROR_MESSAGE, ephemeral=True)
        return

    try:
        db.stop_tracking_manga(interaction.guild_id, manga_id)
        await interaction.response.send_message(f"Stopped tracking **{manga.name}**")
    except Exception as e:
        await interaction.response.send_message(f"Failed to stop tracking {manga_id}. Use /tracked_manga to make sure this server is tracking it before trying again.", ephemeral=True)

# tracked manga
@client.tree.command(name="tracked_manga", description=
                     "Shows a list of all tracked manga")
async def tracked_manga(interaction: discord.Interaction):
    if not db.is_guild_registered(interaction.guild_id):
        await interaction.response.send_message("Bot has not been set up for this server", ephemeral=True)
        return
    
    try:
        manga = db.get_tracked_manga(interaction.guild_id)
        
        response = f"Tracked manga for **{interaction.guild.name}**"
        for m in manga:
            response += f"\n* **{m.name}**"

        await interaction.response.send_message(response)
    except Exception as e:
        await interaction.response.send_message(GENERIC_ERROR_MESSAGE, ephemeral=True)


# |------------------------------------------------|
# |----------------------TASKS---------------------|
# |------------------------------------------------|
# check for updates 00:00 every day
@tasks.loop(time=datetime.time(hour=0, minute=0))
async def update():
    # for each manga
    # ... if updated
    # ... ... for every guild tracking this manga
    # ... ... ... send update

    try:
        manga = db.get_all_manga()
    except:
        return

    for manga in manga:
        # mangaupdates api call
        new_chapters = api.get_chapters(manga.id, str(yesterday()), str(yesterday()))
        
        if len(new_chapters) == 0:
            continue
        
        channels = db.get_update_channel_ids_for_servers_tracking_manga(manga.id)

        prepared_message = ""
        for chapter in new_chapters:
            prepared_message += UPDATE_MESSAGE.format(
                role=manga.role_id,
                manga_name=chapter.title,
                chapter_number=chapter.number)
            prepared_message += "\n"

        for channel_id in channels:
            channel = client.get_channel(channel_id)

            try:
                await channel.send(prepared_message)
            except Exception as e:
                print(e)


# |------------------------------------------------|
# |---------------------EVENTS---------------------|
# |------------------------------------------------|


# |------------------------------------------------|
# |----------------------MISC----------------------|
# |------------------------------------------------|
def yesterday() -> datetime.date:
    return datetime.date.fromtimestamp(datetime.datetime.timestamp(datetime.datetime.today()) - 3600 * 24)

# |------------------------------------------------|
# |---------------------LAUNCH---------------------|
# |------------------------------------------------|
client.run(token)