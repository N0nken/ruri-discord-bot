import requests
import xml.etree.ElementTree as ET


MANGA_UPDATES_BASE_URL = "https://api.mangaupdates.com/v1/series/{id}/rss"


def get_latest_chapter(manga_id: int, manga_latest_chapter: float):
    try:
        r = requests.get(f"{MANGA_UPDATES_BASE_URL.format(id=manga_id)}")
    except:
        return -1
    
    latest_chapter = -1

    chapters = _parse_rss(r.text)

    for chapter in chapters:
        if float(chapter) > manga_latest_chapter and float(chapter) > latest_chapter:
            latest_chapter = float(chapter)
    
    return latest_chapter


def _parse_rss(rss_string: str):
    # create element tree object
    root = ET.fromstring(rss_string)

    # create empty list for news items
    chapters = []
    for item in root.findall('./channel/item'):
        for child in item:
            if child.tag == 'title':
                chapters.append(_extract_chapter(child.text))
    
    # return news items list
    return chapters


def _extract_chapter(title: str) -> float:
    inverted_string = ""
    for i in range(len(title) - 1, -1, -1):
        if title[i] == "c":
            break
        
        inverted_string += title[i]
    
    chapter_string = ""
    for i in range(len(inverted_string) - 1, -1, -1):
        chapter_string += inverted_string[i]

    return chapter_string[1:]