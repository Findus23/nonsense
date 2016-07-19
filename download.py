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
with open('download.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
