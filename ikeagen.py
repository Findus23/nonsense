#!/usr/bin/python3
import json

import pickle

import os
import random
from PIL import Image


def gen():
    table = [[[0 for i in range(221)] for j in range(221)] for k in range(221)]
    # contents = open("ikeaname.txt").read().splitlines()
    with open('download.json') as inputfile:
        contents = json.load(inputfile)["names"]
    count = 0
    for name in contents:
        if name:
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


def save(data):
    with open('ikeaname.pickle', 'wb') as outfile:
        pickle.dump(data, outfile,pickle.HIGHEST_PROTOCOL)


def load():
    with open('ikeaname.pickle',"rb") as inputfile:
        table = pickle.load(inputfile)
    return table


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


if os.path.isfile('ikeaname.pickle'):
    table, count = load()
    # image(table)

else:
    table, count = gen()
    save((table, count))


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
