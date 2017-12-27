import logging

from scrapy.spiders import Spider

logger = logging.getLogger(__name__)


class NonsenseSpider(Spider):
    name = "nonsense"
    start_urls = [
        "http://www.ikea.com/at/de/catalog/allproducts/",
        "http://www.ikea.com/at/de/catalog/allproducts/department/",
        "http://www.ikea.com/at/de/catalog/allproducts/alphabetical/"
    ]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': "../crawl.json"
    }

    def parse(self, response):
        for url in response.css(".productCategoryContainerWrapper a::attr(href)"):
            if url is not None:
                yield response.follow(url, callback=self.parse_product_list)
        pass

    def parse_product_list(self, response):
        products = response.css(".productDetails")
        for product in products:
            yield {
                'name': product.css(".productTitle::text").extract_first(),
                'description': product.css(".productDesp::text").extract_first(),
            }
