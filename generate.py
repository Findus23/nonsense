#!/usr/bin/env python3
import random

import tomli

with open('words.toml',"rb") as data_file:
    data = tomli.load(data_file)


def get_noun():
    noun = random.choice(data["nouns"])
    if random.random() <= 0.1:
        noun += random.choice(data["suffix"])
    if random.random() <= 0.1:
        noun = random.choice(data["prefix"]) + noun
    return noun


def get_description():
    description = get_noun()
    mit = False
    num_extras = round(abs(random.normalvariate(2.0, 2.0)))
    for i in range(0, num_extras):
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
        description += " " + extra
    return description


if __name__ == "__main__":
    for _ in range(10):
        print(get_description())
