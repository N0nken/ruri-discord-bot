import json
import os


class Manga:
    def __init__(self, name: str, id: str, role_id: int = -1, latest_chapter: int = -1):
        self.name = name
        self.id = id
        self.role_id = role_id
        self.latest_chapter = latest_chapter

    def dict(self) -> dict:
        return {
            "name" : self.name,
            "id" : self.id,
            "role_id" : self.role_id,
            "latest_chapter" : self.latest_chapter
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
    with open("configs/overview.json", "r") as overview:
        overview_data = json.load(overview)
        return overview_data
    return None


def _get_guild_file_path(guild_id: str) -> str:
    overview_data = _get_overview()

    base_path = overview_data["base_path"]

    # raise error if guild isn't registered
    if not guild_id in overview_data["file_names"].keys():
        raise ValueError("Guild ID not recognized")

    # build filepath
    file_name = overview_data["file_names"][guild_id]
    full_path = "configs/" + base_path + file_name

    return full_path


def _write_guild(guild: Guild):
    content = guild.dict()
    content.pop("id")
    with open(_get_guild_file_path(guild.id), "w") as guild_file:
        json.dump(content, guild_file)


def get_registered_guilds() -> list[str]:
    overview = _get_overview()
    return overview["file_names"].keys()


def is_guild_registered(guild_id: str) -> bool:
    return guild_id in get_registered_guilds()


def get_guild_config(guild_id: str) -> Guild:
    full_path = _get_guild_file_path(guild_id)

    # raise error if the guilds file for some reason isn't found
    if not os.path.exists(full_path):
        raise FileExistsError("File not found")

    with open(full_path, "r") as guild_file:
        guild_data = json.load(guild_file)
        guild_name = guild_data["name"]
        channel_id = guild_data["channel"]

        manga = []
        for m in guild_data["manga"]:
            manga.append(Manga(m["name"], m["id"], m["role_id"], m["latest_chapter"]))

        return Guild(guild_id, guild_name, channel_id, manga)


def get_tracked_manga(guild_id: str) -> list[Manga]:
    guild_config = get_guild_config(guild_id)
    return guild_config.manga


def register_guild(guild: Guild):
    # get guild overview
    overview_data = _get_overview()
    
    # raise error if guild already exists
    if guild.id in overview_data["file_names"].keys():
        raise ValueError("Guild already registered")

    # add new config file path to overview
    overview_data["file_names"][guild.id] = guild.id + ".json"
    with open("configs/overview.json", "w") as overview:
        json.dump(overview_data, overview)

    # write content to guild file
    _write_guild(guild)


def set_channel(guild_id: str, channel_id: str):
    guild = get_guild_config(guild_id)
    guild.channel = channel_id
    _write_guild(guild)


def register_manga(guild_id: str, manga: Manga):
    guild = get_guild_config(guild_id)

    # raise error if manga already registered
    if guild.is_manga_registered(manga.name):
        raise ValueError("Manga already registered")
    
    guild.manga.append(manga)

    # update guild file
    _write_guild(guild)


def remove_manga(guild_id: str, name: str):
    guild = get_guild_config(guild_id)

    # raise error if manga is not registered. can't remove manga that doesn't exist dummy (,,>_<,,)
    if not guild.is_manga_registered(name):
        raise ValueError("Manga not registered")
    
    # remove manga
    i = 0
    for manga in guild.manga:
        if manga.name == name:
            break
        i += 1
    guild.manga.pop(i)

    # update guild file
    _write_guild(guild)


def set_latest_chapter(guild_id: str, name: str, chapter: int):
    guild_config = get_guild_config(guild_id)

    for manga in guild_config.manga:
        if manga.name != name:
            continue
        manga.latest_chapter = chapter
    
    _write_guild(guild_config)


if __name__ == "__main__":
    get_guild_config("0")
    register_guild(Guild("1234567890", "test test", "0987654321", [
            Manga("Manga 1", "Mangadex_Link_1", 1),
            Manga("Manga 2", "Mangadex_Link_2", 2),
            Manga("Manga 3", "Mangadex_Link_3", 3)]))
    remove_manga("1234567890", "Manga 3")
    register_manga("1234567890", Manga("Manga 4", "Mangadex_Link_4", 4))
    for manga in get_tracked_manga("1234567890"):
        print(manga.dict())