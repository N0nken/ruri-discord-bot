import mysql.connector
import os
import atexit
import datetime
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("SQL_USER")
password = os.getenv("SQL_PASS")

database = mysql.connector.connect(
    host="localhost",
    user=user,
    passwd=password
)

def _exit_handler():
    database.close()

atexit.register(_exit_handler)


class Manga:
    def __init__(self, name: str, id: int, role_id: int = -1, latest_chapter: int = -1, last_updated: str = ""):
        self.name = name
        self.id = id
        self.role_id = role_id
        self.latest_chapter = latest_chapter
        self.last_updated = last_updated


class Guild:
    def __init__(self, guild_id: int, name: str, channel_id: int = "", manga: list[Manga] = []):
        self.id = guild_id
        self.name = name
        self.channel = channel_id
        self.manga = manga


def is_guild_registered(guild_id: int) -> bool:
    cursor = database.cursor()

    cursor.execute("SELECT count(discord_guild_id) FROM guilds WHERE discord_guild_id=%s", (guild_id))
    result = cursor.fetchone()
    count = result[0]

    cursor.close()

    return 0 < count


def register_guild(guild: Guild):
    query = "INSERT INTO guilds (discord_guild_id, name, updates_channel_id) VALUES (%s, %s, %s)"

    cursor = database.cursor()
    cursor.execute(query, (guild.id, guild.name, guild.channel))
    cursor.close()


def get_tracked_manga(guild_id: int) -> list[Manga]:
    query = "SELECT * FROM manga WHERE manga_updates_id IN (SELECT manga_updates_id FROM tracked_manga WHERE discord_guild_id=%s);"
    
    cursor = database.cursor()
    cursor.execute(query, (guild_id))
    result = cursor.fetchall()

    cursor.close()
    
    manga = []
    for row in result:
        manga.append(Manga(row[1], row[0], latest_chapter=row[2], last_updated=str([3])))
    
    return manga


def set_channel(guild_id: int, channel_id: int):
    query = "UPDATE guilds SET updates_channel_id=%s WHERE discord_guild_id=%s;"

    cursor = database.cursor()
    cursor.execute(query, (channel_id, guild_id))
    cursor.close()


def track_manga(guild_id: int, manga: Manga):
    insert_manga_query = "INSERT INTO manga (manga_updates_id, name, latest_chapter) VALUES (%s, %s, %s)"
    update_guild_tracking_query = "INSERT INTO tracked_manga (discord_guild_id, manga_updates_id) VALEUS (%s, %s)"

    cursor = database.cursor()

    # manga may already exist in db
    try:
        cursor.execute(insert_manga_query, (manga.id, manga.name, manga.latest_chapter))
    except:
        pass

    cursor.execute(update_guild_tracking_query, (guild_id, manga.id))
    cursor.close()


def stop_tracking_manga(guild_id: int, manga_id: int):
    query = "DELETE FROM tracked_manga WHERE discord_guild_id=%s AND manga_updates_id=%s"

    cursor = database.cursor()
    cursor.execute(query, (guild_id, manga_id))
    cursor.close()


def set_latest_chapter(manga_id: int, chapter: float):
    query = "UPDATE manga SET latest_chapter=%s, last_updated=%s WHERE manga_updates_id=%s"

    cursor = database.cursor()
    cursor.execute(query, (chapter, datetime.datetime.now(), manga_id))
    cursor.close()


def get_all_manga() -> list[Manga]:
    query = "SELECT * FROM manga"

    cursor = database.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    manga = []
    for row in result:
        manga.append(Manga(row[1], row[0], latest_chapter=row[2], last_updated=row[3]))
    
    return manga


def get_update_channel_ids_for_servers_tracking_manga(manga_id: int) -> list[int]:
    query = "SELECT updates_channel_id FROM guilds WHERE discord_guild_id IN (SELECT discord_guild_id FROM tracked_manga WHERE manga_updates_id=%s)"

    cursor = database.cursor()
    cursor.execute(query, (manga_id))
    result = cursor.fetchall()
    cursor.close()

    channel_ids = []
    for row in result:
        channel_ids.append(row[0])
    
    return channel_ids


if __name__ == "__main__":
    #get_guild_config("0")
    register_guild(Guild("1234567890", "test test", "0987654321", [
            Manga("Manga 1", "Mangadex_Link_1", 1, "2001-01-01"),
            Manga("Manga 2", "Mangadex_Link_2", 2, "2002-02-02"),
            Manga("Manga 3", "Mangadex_Link_3", 3, "2003-03-03")]))
    #remove_manga("1234567890", "Manga 3")
    #register_manga("1234567890", Manga("Manga 4", "Mangadex_Link_4", 4, "2004-04-04"))
    for manga in get_tracked_manga("1234567890"):
        print(manga.dict())