import glob
import json


def crawl_data():
    all_data = []
    for file in glob.glob("crawlData/*.json"):
        with open(file, "r") as inputfile:
            all_data.extend(json.load(inputfile))
    return all_data


if __name__ == "__main__":
    print(crawl_data().__len__())
