#!/usr/bin/env python3
import json
import re

import requests
from bs4 import BeautifulSoup

descriptions = []
names = []
for i in range(0, 25):
    r = requests.get("http://www.ikea.com/at/de/catalog/productsaz/{letter}/".format(letter=i))
    soup = BeautifulSoup(r.text, 'html.parser')
    for span in soup.find_all('span', "productsAzLink"):
        product = span.a.string
        m = re.match("((?:[^a-z\s]|Ä|Å|Ö){2,})? ?(.*)?", product)
        print(product)
        names.append(m.group(1))
        descriptions.append(m.group(2))
data = {
    "descriptions": list(set(descriptions)),
    "names": list(set(names))
}

nouns = set()
adj = set()
digit = set()
prefix = set()
suffix = set()
for d in (data["descriptions"]):
    nouns.update(re.findall("([A-ZÖÄÜ][^A-Z\s\dÖÄÜ\-/,+()\"]+)", d))
    adj.update(re.findall(" ([^A-ZÖÄÜ\d]{3,}[^A-ZÖÄÜ\s\d])", d))
    digit.update(re.findall(" ([\d]+[\w.-]{3,}[\w./]+)", d))
    prefix.update(re.findall("([\w.-]+-)", d))
    suffix.update(re.findall("(-[\w.-]+)", d))

words = {
    "nouns": list(nouns),
    "adj": list(adj),
    "digit": list(digit),
    "prefix": list(prefix),
    "suffix": list(suffix)
}
with open('words.json', 'w') as outfile:
    json.dump(words, outfile, indent=4)
