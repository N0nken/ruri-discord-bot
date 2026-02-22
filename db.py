import mysql.connector
import os
import atexit
import datetime
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("SQL_USER")
password = os.getenv("SQL_PASS")
host = os.getenv("SQL_HOST")

database = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database="ruri_discord_bot",
    autocommit=True
)

def _exit_handler():
    database.disconnect()

atexit.register(_exit_handler)


class Manga:
    def __init__(self, name: str, id: int, role_id: int = -1, last_updated="0000-00-00"):
        self.name = name
        self.id = id
        self.role_id = role_id
        self.last_updated = last_updated


class Guild:
    def __init__(self, guild_id: int, name: str, channel_id: int = "", manga: list[Manga] = []):
        self.id = guild_id
        self.name = name
        self.channel = channel_id
        self.manga = manga


def is_guild_registered(guild_id: int) -> bool:
    cursor = database.cursor()

    cursor.execute("SELECT count(discord_guild_id) FROM guilds WHERE discord_guild_id=%s", [guild_id])
    result = cursor.fetchone()
    count = result[0]

    cursor.close()

    return 0 < count


def register_guild(guild: Guild):
    query = "INSERT INTO guilds (discord_guild_id, name, updates_channel_id) VALUES (%s, %s, %s)"

    cursor = database.cursor()
    cursor.execute(query, [guild.id, guild.name, guild.channel])
    cursor.close()


def get_tracked_manga(guild_id: int) -> list[Manga]:
    query = "SELECT * FROM manga WHERE manga_updates_id IN (SELECT manga_updates_id FROM tracked_manga WHERE discord_guild_id=%s);"
    
    cursor = database.cursor()
    cursor.execute(query, [guild_id])
    result = cursor.fetchall()

    cursor.close()
    
    manga = []
    for row in result:
        manga.append(Manga(row[1], row[0], row[2]))
    
    return manga


def set_channel(guild_id: int, channel_id: int):
    query = "UPDATE guilds SET updates_channel_id=%s WHERE discord_guild_id=%s;"

    cursor = database.cursor()
    cursor.execute(query, [channel_id, guild_id])
    cursor.close()


def track_manga(guild_id: int, manga: Manga):
    insert_manga_query = "INSERT INTO manga (manga_updates_id, name, last_updated) VALUES (%s, %s, %s)"
    update_guild_tracking_query = "INSERT INTO tracked_manga (discord_guild_id, manga_updates_id) VALUES (%s, %s)"

    cursor = database.cursor()

    # manga may already exist in db
    try:
        cursor.execute(insert_manga_query, [manga.id, manga.name, manga.last_updated])
    except:
        pass

    cursor.execute(update_guild_tracking_query, [guild_id, manga.id])
    cursor.close()


def stop_tracking_manga(guild_id: int, manga_id: int):
    forget_tracking_query = "DELETE FROM tracked_manga WHERE discord_guild_id=%s AND manga_updates_id=%s"
    manga_track_count_query = "SELECT count(*) FROM tracked_manga WHERE manga_updates_id=%s"
    forget_manga_query = "DELETE FROM manga WHERE manga_updates_id=%s"

    cursor = database.cursor()
    cursor.execute(forget_tracking_query, [guild_id, manga_id])
    
    cursor.execute(manga_track_count_query, [manga_id])
    if cursor.fetchone()[0] == 0:
        cursor.execute(forget_manga_query, [manga_id])

    cursor.close()


def get_all_manga() -> list[Manga]:
    query = "SELECT * FROM manga"

    cursor = database.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    manga = []
    for row in result:
        manga.append(Manga(row[1], row[0], row[2]))
    
    return manga


def get_update_channel_ids_for_servers_tracking_manga(manga_id: int) -> list[int]:
    query = "SELECT updates_channel_id FROM guilds WHERE discord_guild_id IN (SELECT discord_guild_id FROM tracked_manga WHERE manga_updates_id=%s)"

    cursor = database.cursor()
    cursor.execute(query, [manga_id])
    result = cursor.fetchall()
    cursor.close()

    channel_ids = []
    for row in result:
        channel_ids.append(row[0])
    
    return channel_ids


def get_manga_details(manga_id: int) -> Manga:
    query = "SELECT * FROM manga WHERE manga_updates_id=%s"

    cursor = database.cursor()
    cursor.execute(query, [manga_id])
    result = cursor.fetchone()
    cursor.close()

    return Manga(result[1], result[0], result[2])


def set_last_updated(manga_id: int):
    query = "UPDATE manga SET last_updated=%s WHERE manga_updates_id=%s"

    cursor = database.cursor()
    cursor.execute(query, [str(datetime.date.today()), manga_id])
    cursor.close()
