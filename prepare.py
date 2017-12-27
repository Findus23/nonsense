#!/usr/bin/env python3
import json

import re
import yaml

with open('crawl.json', "r") as inputfile:
    crawldata = json.load(inputfile)

descriptions = {result["description"] for result in crawldata}
print(len(descriptions))

nouns = set()
adj = set()
digit = set()
prefix = set()
suffix = set()
for d in descriptions:
    if d is not None:
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
with open('words.yaml', 'w') as outfile:
    yaml.dump(words, outfile, default_flow_style=False)
