import logging

from scrapy.spiders import Spider

logger = logging.getLogger(__name__)


class NonsenseSpider(Spider):
    name = "nonsense"
    start_urls = [
        "https://www.ikea.com/at/de/cat/produkte-products/",
    ]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': "../crawlData/crawl.json"
    }

    def parse(self, response):
        products = response.css(".product-compact")
        for product in products:
            name = product.css(".product-compact__name::text").extract_first()
            description = product.css(".product-compact__type::text").extract_first().strip().strip(",")
            yield {
                'name': name,
                'description': description,
            }
        for url in response.css("a.range-catalog-list__link::attr(href)"):
            if url is not None:
                yield response.follow(url, callback=self.parse)
