# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    title = scrapy.Field()
    availability = scrapy.Field()
    eng_title = scrapy.Field()
    genre = scrapy.Field()
    age = scrapy.Field()
    translator = scrapy.Field()
    publisher = scrapy.Field()
    year = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field()


