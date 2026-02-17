import requests
import xml.etree.ElementTree as ET
import re

#frieren id 66296374554
#ruri id 60867454335

base_url = "https://api.mangaupdates.com/v1/series/60867454335/rss"

params = {
    "search": "sousou no frieren",
    "stype": "title",
}

r = requests.get(
    f"{base_url}"
)

def parse_rss(rss_string: str):

    # create element tree object
    root = ET.fromstring(rss_string)

    # create empty list for news items
    chapters = []
    for item in root.findall('./channel/item'):
        for child in item:
            if child.tag == 'title':
                chapters.append(extract_chapter(child.text))
    
    # return news items list
    return chapters


def extract_chapter(title: str) -> float:
    inverted_string = ""
    for i in range(len(title) - 1, -1, -1):
        if title[i] == "c":
            break
        
        inverted_string += title[i]
    
    chapter_string = ""
    for i in range(len(inverted_string) - 1, -1, -1):
        chapter_string += inverted_string[i]

    return chapter_string[1:]


print(r.text)
print(parse_rss(r.text))

