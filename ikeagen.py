#!/usr/bin/python3

import numpy as np
import os
import random
from PIL import Image

import utils


def gen():
    n = 221
    table = np.empty(shape=(n, n, n), dtype=np.int)
    crawldata = utils.crawl_data()
    names = {result["name"] for result in crawldata}
    count = 0
    for name in names:
        if name is not None and "„" not in name:
            name = "  " + name + "  "
            zeichen = list(name)
            zeichenl = len(zeichen)
            zeichenl -= 2
            a = 0
            while a < zeichenl:
                table[ord(zeichen[a])][ord(zeichen[a + 1])][ord(zeichen[a + 2])] += 1
                count += 1
                a += 1
    return table, count


def letter(a, b):
    mylist = []
    for c in range(221):
        for x in range(table[a][b][c]):
            mylist.append(c)

    return random.choice(mylist)


def image(table):
    img = Image.new('RGB', (221, 221))
    maximum = max(max(table))
    print(maximum)
    row = 0
    col = 0
    for coln in range(221):
        for rown in range(221):
            color = 255 - int(table[coln][rown] / maximum * 255)
            img.putpixel((coln, rown), (color, color, color))

    img = img.resize((2210, 2210), )
    img.save('image.png')


if os.path.isfile('ikeaname.npy') and False:  # Loading uses twice the memory and is therefore disabled
    table, count = np.load('ikeaname.npy')
else:
    table, count = gen()
    np.save('ikeaname.npy', (table, count), )


def generate():
    a = b = 32
    wort = []
    while True:
        new = letter(a, b)
        wort.append(chr(new))
        a = b
        b = new
        if a == 32 and b == 32:
            if len(wort) > 5:
                return "".join(wort).strip()
            else:
                wort = []
                a = b = 32


if __name__ == "__main__":
    for _ in range(100):
        print(generate())
