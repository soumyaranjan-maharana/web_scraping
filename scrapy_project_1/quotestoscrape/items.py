# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class QuotestoscrapeItem:
    # define the fields for your item here like:
    title: str | None = None
    author: str | None = None
    tag: str | None = None
