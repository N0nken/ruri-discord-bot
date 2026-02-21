import requests
import xml.etree.ElementTree as ET


MANGA_UPDATES_URL = "https://api.mangaupdates.com/v1/series/{id}/rss"


def get_latest_chapter(manga_id: int) -> str:
    # get rss feed
    try:
        r = requests.get(f"{MANGA_UPDATES_URL.format(id=manga_id)}")
    except:
        return ""

    # parse rss feed
    newest_chapter = _parse_rss_for_chapter(r.text)
    
    return newest_chapter


def _parse_rss_for_chapter(rss_string: str) -> str:
    # create element tree object
    root = ET.fromstring(rss_string)

    # create empty list for news items
    chapters = root.findall("./channel/item")

    if len(chapters) == 0:
        return -1
    
    latest_chapter_elem = chapters[0]
    chapter_title_elem = latest_chapter_elem.find("./title")
    
    if chapter_title_elem == None:
        return -1
    
    # return news items list
    return _extract_chapter(chapter_title_elem.text)


def _extract_chapter(title: str) -> str:
    # chapters are written as "bla bla bla bla bla bla c.X/X.X/X.X-Y.Y"
    # so split at spaces to get the chapter as its own string
    split = title.split(" ")
    chapter_string = split[-1] # chapter always at the end
    chapter_string = chapter_string[2:] # remove "c."

    return chapter_string


def get_manga_name(manga_id: int) -> str:
    # get rss feed
    try:
        r = requests.get(f"{MANGA_UPDATES_URL.format(id=manga_id)}")
    except:
        return -1
    
    return _parse_rss_for_title(r.text)
    

def _parse_rss_for_title(rss_string: str) -> str:
    # create element tree object
    root = ET.fromstring(rss_string)

    # create empty list for news items
    chapters = root.findall("./channel/item")

    if len(chapters) == 0:
        return ""
    
    latest_chapter_elem = chapters[0]
    chapter_title_elem = latest_chapter_elem.find("./title")

    if chapter_title_elem == None:
        return ""

    return _extract_title(chapter_title_elem.text)


def _extract_title(title: str) -> str:
    chapter_start = 0
    # loop through the title backwards to find the first " ".
    # thats where the title ends and the chapter starts
    for i in range(len(title) - 1, -1, -1):
        if title[i] == " ":
            chapter_start = i
            break
    
    return title[:chapter_start]
