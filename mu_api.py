import requests
import xml.etree.ElementTree as ET


MANGA_UPDATES_BASE_URL = "https://api.mangaupdates.com/v1/series/{id}/rss"


def get_latest_chapter(manga_id: int, manga_latest_chapter: float):
    # get rss feed
    try:
        r = requests.get(f"{MANGA_UPDATES_BASE_URL.format(id=manga_id)}")
    except:
        return -1
    
    latest_chapter = -1

    # parse rss feed
    chapters = _parse_rss(r.text)

    # find the latest chapter
    for chapter in chapters:
        if float(chapter) > manga_latest_chapter and float(chapter) > latest_chapter:
            latest_chapter = float(chapter)
    
    return latest_chapter


def _parse_rss(rss_string: str):
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


def _extract_chapter(title: str) -> float:
    # chapters are written as "bla bla bla bla bla bla c.X/X.X/X.X-Y.Y"
    # so split at spaces to get the chapter as its own string
    # then assume it has a range of chapters and split at "-" 
    split = title.split(" ")
    chapter_string = split[-1] # chapter always at the end
    chapter_string = chapter_string[2:] # remove "c."
    split = chapter_string.split("-")

    # however we do assume it doesn't have a range when setting the
    # initial value for the newest_chapter
    # and then change it if it did have a range
    newest_chapter = float(split[0])
    if len(split) > 1: # release included a range of chapters
        newest_chapter = float(split[1]) # so newest chapter is the upper bound of the range

    return newest_chapter