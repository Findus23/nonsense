#!/usr/bin/env python3
import json
import random


def get_noun():
    noun = random.choice(data["nouns"])
    if random.random() <= 0.1:
        noun += random.choice(data["suffix"])
    if random.random() <= 0.1:
        noun = random.choice(data["prefix"]) + noun
    return noun


with open('data.json') as data_file:
    data = json.load(data_file)

noun = get_noun()
mit = False
numExtras = round(abs(random.normalvariate(2.0, 2.0)))
for i in range(0, numExtras):
    rand = random.random()
    if rand <= 0.35:
        if mit:
            extra = "und " + get_noun()
        else:
            extra = "mit " + get_noun()
        mit = True
    elif 0.35 <= rand <= 0.50:
        extra = "für " + get_noun()
    elif rand >= 0.90:
        extra = random.choice(data["digit"])
        mit = False

    else:
        extra = random.choice(data["adj"])
        mit = False
    noun += " " + extra

print(noun)