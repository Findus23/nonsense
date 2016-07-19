#!/usr/bin/env python3
import json
import re

with open('download.json') as data_file:
    data = json.load(data_file)

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

data = {
    "nouns": list(nouns),
    "adj": list(adj),
    "digit": list(digit),
    "prefix": list(prefix),
    "suffix": list(suffix)
}
with open('data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
