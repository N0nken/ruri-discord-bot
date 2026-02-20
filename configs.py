import json
import os


class Manga:
    def __init__(self, name: str, id: str, role_id: int = -1, latest_chapter: int = -1, last_updated: str = ""):
        self.name = name
        self.id = id
        self.role_id = role_id
        self.latest_chapter = latest_chapter
        self.last_updated = last_updated


    def dict(self) -> dict:
        return {
            "name" : self.name,
            "id" : self.id,
            "role_id" : self.role_id,
            "latest_chapter" : self.latest_chapter,
            "last_updated" : self.last_updated
        }


class Guild:
    def __init__(self, guild_id: str, name: str, channel_id: str = "", manga: list[Manga] = []):
        self.id = guild_id
        self.name = name
        self.channel = channel_id
        self.manga = manga
    

    def dict(self) -> dict:
        result = {
            "id" : self.id,
            "name" : self.name,
            "channel" : self.channel,
            "manga" : []
        }

        for manga in self.manga:
            result["manga"].append(manga.dict())

        return result


    def is_manga_registered(self, name: str):
        for manga in self.manga:
            if manga.name == name:
                return True
        return False


def _get_overview() -> dict:
    pass


def _get_guild_file_path(guild_id: str) -> str:
    pass


def _write_guild(guild: Guild):
    pass


def get_registered_guilds() -> list[str]:
    pass


def is_guild_registered(guild_id: str) -> bool:
    pass


def get_guild_config(guild_id: str) -> Guild:
    pass


def get_tracked_manga(guild_id: str) -> list[Manga]:
    pass

def register_guild(guild: Guild):
    pass


def set_channel(guild_id: str, channel_id: str):
    pass


def register_manga(guild_id: str, manga: Manga):
    pass


def remove_manga(guild_id: str, name: str):
    pass


def set_latest_chapter(guild_id: str, name: str, chapter: int):
    pass


def set_last_updated(guild_id: str, name: str, date: str):
    pass


if __name__ == "__main__":
    get_guild_config("0")
    register_guild(Guild("1234567890", "test test", "0987654321", [
            Manga("Manga 1", "Mangadex_Link_1", 1, "2001-01-01"),
            Manga("Manga 2", "Mangadex_Link_2", 2, "2002-02-02"),
            Manga("Manga 3", "Mangadex_Link_3", 3, "2003-03-03")]))
    remove_manga("1234567890", "Manga 3")
    register_manga("1234567890", Manga("Manga 4", "Mangadex_Link_4", 4, "2004-04-04"))
    for manga in get_tracked_manga("1234567890"):
        print(manga.dict())