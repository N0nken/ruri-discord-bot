import requests
import xml.etree.ElementTree as ET
import re

#frieren id 66296374554
#ruri id 60867454335
#fuufu ijou koibito miman id 27408632789

# {"name": "Manga Updates", "channel": "1473333823403200684", 
# "manga": [
# {"name": "Ruri Dragon", "id": 60867454335, "role_id": -1, "latest_chapter": 44.0}, 
# {"name": "Sousou No Frieren", "id": 66296374554, "role_id": -1, "latest_chapter": 147.0}, 
# {"name": "Inkya Gal Demo Ikigaritai!", "id": 55992461077, "role_id": -1, "latest_chapter": 18}, 
# {"name": "#Gyaru to Gyaru no Yuri", "id": 1928488413, "role_id": -1, "latest_chapter": -1}, 
# {"name": "Fuufu Ijou, Koibito Miman", "id": 27408632789, "role_id": -1, "latest_chapter": 79}]}


base_url = "https://api.mangaupdates.com/v1/series/27408632789/rss"
#base_url = "https://api.mangaupdates.com/v1/releases/search"

params = {
    "start_date" : "2026-02-18"
}

r = requests.get(
    f"{base_url}",
    json=params
)

def parse_rss(rss_string: str):
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
    return extract_chapter(chapter_title_elem.text)


def extract_chapter(title: str) -> float:
    split = title.split(" ")
    chapter_string = split[-1] # chapter always at the end
    chapter_string = chapter_string[2:] # remove "c."

    split = chapter_string.split("-") # in case of multiple chapters in the same release
    newest_chapter = float(split[0]) # get first chapter as newest chapter
    
    if len(split) > 1: # release included a range of chapters
        newest_chapter = float(split[1]) # so newest chapter is the upper bound of the range

    return newest_chapter


print(r.text)
print("---------------------")
print(parse_rss(r.text))

