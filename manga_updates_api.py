import requests
import xml.etree.ElementTree as ET
import datetime


MANGA_UPDATES_SEARCH_RELEASES_URL = "https://api.mangaupdates.com/v1/releases/search"


class Chapter:
    def __init__(self, title: str, number: str):
        self.title = title
        self.number = number


def get_chapters(manga_id: str, date_start: str = "0001-01-01", date_end: str = "9999-12-31") -> list[Chapter]:
    params = {
        "search": str(manga_id),
        "search_type": "series",
        "start_date": date_start,
        "end_date": date_end
    }

    r = requests.post(
        url=MANGA_UPDATES_SEARCH_RELEASES_URL,
        json=params
    )

    try:
        json = r.json()
        if json["total_hits"] == 0:
            raise Exception("No Results")
        
        chapters = []
        for result in json["results"]:
            record = result["record"]
            chapters.append(Chapter(record["title"], record["chapter"]))
        
        return chapters
    except:
        return []


def get_manga_name(manga_id: str) -> str:
    params = {
        "search": str(manga_id),
        "search_type": "series",
        "perpage": 1
    }

    r = requests.post(
        url=MANGA_UPDATES_SEARCH_RELEASES_URL,
        json=params
    )

    try:
        json = r.json()
        if json["total_hits"] == 0:
            raise Exception("No Results")
        
        title = json["results"][0]["record"]["title"]

        return title
    except:
        return ""


if __name__ == "__main__":
    chapters = get_chapters("3236302268", "2026-02-23", str(datetime.date.today()))
    for chapter in chapters:
        print(chapter.title, chapter.number)