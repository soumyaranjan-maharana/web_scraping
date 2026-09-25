import scrapy
from ..items import QuotestoscrapeItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css(".quote"):
            items = QuotestoscrapeItem()

            title = quote.css(".text::text").get()
            author = quote.css(".author::text").get()
            tag = quote.css(".tags .tag::text").getall()

            items.title = title
            items.author = author
            items.tag = tag

            yield items

        nxt_page = response.css(".next a::attr(href)").get()
        if nxt_page:
            yield response.follow(nxt_page, self.parse)