#!/usr/bin/python3
import json

import os.path
import random
from PIL import Image


def gen():
    table = [[0 for i in range(221)] for j in range(221)]
    # contents = open("ikeaname.txt").read().splitlines()
    with open('download.json') as inputfile:
        contents = json.load(inputfile)["names"]
    count = 0
    for name in contents:
        if name:
            name = " " + name + " "
            zeichen = list(name)
            zeichenl = len(zeichen)
            zeichenl += -1
            a = 0
            while a < zeichenl:
                table[ord(zeichen[a])][ord(zeichen[a + 1])] += 1
                count += 1
                a += 1
    return table, count


def save(data):
    with open('ikeaname.json', 'w') as outfile:
        json.dump(data, outfile)


def load():
    with open('ikeaname.json') as inputfile:
        table = json.load(inputfile)
    return table


def letter(a):
    mylist = []
    for b in range(221):
        for x in range(table[a][b]):
            mylist.append(b)

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


if not os.path.isfile('ikeaname.json'):
    table, count = load()
    image(table)

else:
    table, count = gen()
    save((table, count))


def generate():
    a = 32
    wort = []
    while True:
        a = letter(a)
        wort.append(chr(a))
        if a == 32:
            if len(wort) > 5:
                return "".join(wort)


if __name__ == "__main__":
    for _ in range(100):
        print(generate())
