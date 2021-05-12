import json
from time import sleep

import requests

categories_url = "https://shop.api.ingka.ikea.com/range/v2/at/de/category-browse"
products_url = "https://shop.api.ingka.ikea.com/range/v1/at/de/category-details?category="


class OutputWriter:
    def __init__(self):
        self.file = open("crawlData/crawl.jsonl", "w")

    def log(self, name: str, description: str):
        print(name, description)
        text = json.dumps({"name": name, "description": description}, ensure_ascii=False)
        self.file.write(text + "\n")

    def close(self):
        self.file.close()


output = OutputWriter()

s = requests.Session()
s.headers.update({"User-Agent": "IKEA App/2.26.0-4156 (iOS) NonsenseBot"})
r = s.get(categories_url)
r.raise_for_status()

categories = set()
data = r.json()["categories"]

for category in data:
    categories.add(category["categoryId"])
    for subcategory in category["subcategories"]:
        categories.add(subcategory["categoryId"])
print(categories)

for category in categories:
    print(category)
    sleep(1)  # make requests slowly
    r = s.get(products_url + category)
    r.raise_for_status()
    products = r.json()["products"]
    for product in products:
        output.log(
            name=product["title"],
            description=product["description"]
        )

output.close()
