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


# |------------------------------------------------|
# |---------------------CONFIG---------------------|
# |------------------------------------------------|
DEV_GUILD_ID = discord.Object(id=942140682083115008)
UPDATE_RATE_MINUTES = 30
UPDATE_MESSAGE = "Chapter **{chapter_number}** is now out for **{manga_name}**!"
DB_CONNECTION_ERROR_MESSAGE = "An error occurred when trying to reach the server"
BOT_IS_NOT_ACTIVATED_ERROR_MESSAGE = "Bot has not been set up for this server"
UPDATE_TIME = datetime.time(hour=23, minute=59)


class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user}!")

        try:
            synced = await client.tree.sync(guild=DEV_GUILD_ID)
            print(f"Synced {len(synced)} commands!")
        except Exception as e:
            print(f"Error syncing commands:\n\n{e}")

        if not update.is_running():
            update.start()
            print("Auto-update task started")


intents = discord.Intents.default()
client = Client(command_prefix="!", intents=intents)









# |------------------------------------------------|
# |--------------------COMMANDS--------------------|
# |------------------------------------------------|
# setup 
@client.tree.command(name="setup", description=
                     "(REQUIRED) Enables the bot for this server.")
async def setup(interaction: discord.Interaction):
    try:
        db.connect()
    except Exception as e:
        print(e)
        return

    try:
        db.register_guild(db.Guild(interaction.guild_id, interaction.guild.name, interaction.channel_id))
    except:
        db.disconnect()
        await interaction.response.send_message("Bot has already been set up for this server OR an error occurred when trying to reach the server. \nTry again in a few minutes if you haven't set up the bot for this server yet.", ephemeral=True)
        return

    db.disconnect()
    await interaction.response.send_message("Bot has now been set up for this server. Start tracking manga by running /track", ephemeral=True)
    print(f"set up bot for [{interaction.guild.name}]")





# set update channel
@client.tree.command(name="set_update_channel", description=
                     "Makes the bot send the updates in the channel this command is run in.")
async def set_update_channel(interaction: discord.Interaction):
    try:
        db.connect()
    except Exception as e:
        print(e)
        return

    try:
        if not db.is_guild_registered(interaction.guild_id):
            db.disconnect()
            await interaction.response.send_message(BOT_IS_NOT_ACTIVATED_ERROR_MESSAGE, ephemeral=True)
            return
    except:
        db.disconnect()
        await interaction.response.send_message(DB_CONNECTION_ERROR_MESSAGE, ephemeral=True)
        return

    try:
        db.set_channel(interaction.guild_id, interaction.channel_id)
    except:
        db.disconnect()
        await interaction.response.send_message(DB_CONNECTION_ERROR_MESSAGE, ephemeral=True)
        return

    db.disconnect()
    await interaction.response.send_message(f"Will now send updates in **{interaction.channel.name}**", ephemeral=True)





# track
@client.tree.command(name="track", description=
                     "Start tracking a manga (role_id is not implemented)")
async def track_manga(interaction: discord.Interaction, manga_updates_id: str, role_id: int = -1):
    try:
        db.connect()
    except Exception as e:
        print(e)
        return

    try:
        if not db.is_guild_registered(interaction.guild_id):
            await interaction.response.send_message(BOT_IS_NOT_ACTIVATED_ERROR_MESSAGE, ephemeral=True)
            return
    except Exception as e:
        db.disconnect()
        await interaction.response.send_message(DB_CONNECTION_ERROR_MESSAGE, ephemeral=True)
        print(e)
        return
    
    manga_name = api.get_manga_name(manga_updates_id)
    if manga_name == "":
        db.disconnect()
        await interaction.response.send_message(f"Couldn't find manga {manga_updates_id}", ephemeral=True)
        return

    try:
        db.track_manga(interaction.guild_id, db.Manga(manga_name, manga_updates_id, role_id, str(datetime.date.today())))
        await interaction.response.send_message(f"Started tracking **{manga_name}**")
    except Exception as e:
        await interaction.response.send_message(f"Failed to start tracking **{manga_name}**", ephemeral=True)
    
    db.disconnect()




# untrack
@client.tree.command(name="untrack", description=
                     "Stop tracking a manga")
async def untrack_manga(interaction: discord.Interaction, manga_id: str):
    try:
        db.connect()
    except Exception as e:
        print(e)
        return

    try:
        if not db.is_guild_registered(interaction.guild_id):
            db.disconnect()
            await interaction.response.send_message(BOT_IS_NOT_ACTIVATED_ERROR_MESSAGE, ephemeral=True)
            return
    except:
        db.disconnect()
        await interaction.response.send_message(DB_CONNECTION_ERROR_MESSAGE, ephemeral=True)
        return

    try:
        manga = db.get_manga_details(manga_id)
    except:
        db.disconnect()
        await interaction.response.send_message(DB_CONNECTION_ERROR_MESSAGE, ephemeral=True)
        return

    try:
        db.stop_tracking_manga(interaction.guild_id, manga_id)
        await interaction.response.send_message(f"Stopped tracking **{manga.name}**")
    except Exception as e:
        await interaction.response.send_message(f"Failed to stop tracking {manga_id}. Use /tracked_manga to make sure this server is tracking it before trying again.", ephemeral=True)
    
    db.disconnect()





# tracked manga
@client.tree.command(name="tracked_manga", description=
                     "Shows a list of all tracked manga")
async def tracked_manga(interaction: discord.Interaction):
    try:
        db.connect()
    except Exception as e:
        print(e)
        return

    try:
        if not db.is_guild_registered(interaction.guild_id):
            db.disconnect()
            await interaction.response.send_message(BOT_IS_NOT_ACTIVATED_ERROR_MESSAGE, ephemeral=True)
            return
    except:
        db.disconnect()
        await interaction.response.send_message(DB_CONNECTION_ERROR_MESSAGE, ephemeral=True)
        return
    
    try:
        manga = db.get_tracked_manga(interaction.guild_id)
        
        response = f"Tracked manga for **{interaction.guild.name}**"
        for m in manga:
            response += f"\n* **{m.name}**"

        await interaction.response.send_message(response)
    except Exception as e:
        await interaction.response.send_message(DB_CONNECTION_ERROR_MESSAGE, ephemeral=True)

    db.disconnect()




# set update schedule
@client.tree.command(name="force_command_sync", description=
                     "Force sync commands (DEV ONLY)",
                     guild=DEV_GUILD_ID)
async def force_command_sync(interaction: discord.Interaction):
    try:
        synced = await client.tree.sync()
        await interaction.response.send_message(f"Synced {len(synced)} commands!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Error syncing commands:\n\n{e}", ephemeral=True)









# |------------------------------------------------|
# |----------------------TASKS---------------------|
# |------------------------------------------------|
# check for updates 23:59 (11:59 PM) every day
@tasks.loop(minutes=5)
async def update():
    # for each manga
    # ... if updated
    # ... ... for every guild tracking this manga
    # ... ... ... send update
    try:
        db.connect()
    except Exception as e:
        print(e)
        return

    try:    
        manga = db.get_all_manga()
    except Exception as e:
        db.disconnect()
        return

    for manga in manga:
        # mangaupdates api call
        new_chapters = api.get_chapters(str(manga.id), manga.last_updated, str(datetime.date.today()))

        print(f"found {len(new_chapters)} new chapters for {manga.id} ({manga.name})")
        
        if len(new_chapters) == 0:
            continue
        
        try:
            channels = db.get_update_channel_ids_for_servers_tracking_manga(manga.id)
        except Exception as e:
            print(e)

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
            except:
                continue
        
        db.set_last_updated(manga.id)
    
    db.disconnect()


# |------------------------------------------------|
# |---------------------EVENTS---------------------|
# |------------------------------------------------|


# |------------------------------------------------|
# |----------------------MISC----------------------|
# |------------------------------------------------|


# |------------------------------------------------|
# |---------------------LAUNCH---------------------|
# |------------------------------------------------|
client.run(token)