import json
from pathlib import Path

datadir = Path("crawlData")


def crawl_data():
    all_data = []
    for file in datadir.glob("*.json"):
        with file.open() as inputfile:
            all_data.extend(json.load(inputfile))
    for file in datadir.glob("*.jsonl"):
        with file.open() as inputfile:
            for line in inputfile:
                if not line or line == "\n":
                    continue
                all_data.append(json.loads(line))

    return all_data


if __name__ == "__main__":
    print(crawl_data().__len__())
