#!/usr/bin/env python3

import re
from typing import Set

import tomli_w

import utils

crawldata = utils.crawl_data()

descriptions = {result["description"] for result in crawldata}
print(len(descriptions))

filter_regex = re.compile(r"(\d+[x-]\d+|\d+-|-\d+)", flags=re.IGNORECASE)


def postprocess(wordset: Set[str]):
    new_words = set()
    for word in wordset:
        word = word.strip()
        for replacephrase in ["+", "für ", "®"]:
            word = word.replace(replacephrase, "").strip()
        if filter_regex.match(word):
            continue
        if word in ["", "+"]:
            continue
        if "/" in word:
            new_words.update(postprocess(set(word.split("/"))))
        elif "," in word:
            new_words.update(postprocess(set(word.split(","))))
        else:
            new_words.add(word)
    return new_words


nouns = set()
adj = set()
digit = set()
prefix = set()
suffix = set()
for d in descriptions:
    if d is not None:
        nouns.update(re.findall(r"([A-ZÖÄÜ][^A-Z\s\dÖÄÜ\-/,+()\"]+)", d))
        adj.update(re.findall(r" ([^A-ZÖÄÜ\d]{3,}[^A-ZÖÄÜ\s\d])", d))
        digit.update(re.findall(r" ([\d]+[\w.-]{3,}[\w./]+)", d))
        prefix.update(re.findall(r"([\w.-]+-)", d))
        suffix.update(re.findall(r"(-[\w.-]+)", d))

words = {
    "nouns": sorted(postprocess(nouns)),
    "adj": sorted(postprocess(adj)),
    "digit": sorted(postprocess(digit)),
    "prefix": sorted(postprocess(prefix)),
    "suffix": sorted(postprocess(suffix))
}
with open('words.toml', 'wb') as outfile:
    tomli_w.dump(words, outfile)
