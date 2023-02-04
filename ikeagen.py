#!/usr/bin/python3

import os
import pickle
import random
import resource
from pathlib import Path

import utils


def gen():
    table = {}
    crawldata = utils.crawl_data()
    names = {result["name"] for result in crawldata}
    count = 0
    for name in names:
        if name is not None:
            name = "  " + name + "  "
            zeichen = list(name)
            zeichenl = len(zeichen)
            a = 0
            while a < zeichenl - 2:
                if (zeichen[a], zeichen[a + 1]) not in table:
                    table[(zeichen[a], zeichen[a + 1])] = {}

                if zeichen[a + 2] in table[(zeichen[a], zeichen[a + 1])]:
                    table[(zeichen[a], zeichen[a + 1])][zeichen[a + 2]] += 1
                else:
                    table[(zeichen[a], zeichen[a + 1])][zeichen[a + 2]] = 1
                count += 1
                a += 1
    return table, count


def letter(a, b):
    mylist = []
    for c in table[(a, b)]:
        mylist.extend([c] * table[(a, b)][c])
    return random.choice(mylist)


use_saving = False  # Loading uses twice the memory and is therefore disabled
save_file=Path('runtime/ikeaname.pickle')

if save_file.exists() and use_saving:
    with save_file.open("rb") as handle:
        b = pickle.load(handle)
else:
    table, count = gen()
    if use_saving:
        with save_file.open("wb") as handle:
            pickle.dump((table, count), handle, protocol=pickle.HIGHEST_PROTOCOL)


def generate():
    a = b = " "
    wort = []
    while True:
        new = letter(a, b)
        wort.append(new)
        a = b
        b = new
        if a == " " and b == " ":
            if len(wort) > 5:
                return "".join(wort).strip()
            else:
                wort = []
                a = b = " "


if __name__ == "__main__":
    for _ in range(100):
        print(generate())
    print("used {mb}MB".format(mb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
