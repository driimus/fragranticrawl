# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Fragrance(scrapy.Item):
    name = scrapy.Field()
    releaseYear = scrapy.Field()
    brand = scrapy.Field()
    perfumers = scrapy.Field()
    gender = scrapy.Field()
    # should be an alt to top/mid/base
    notes = scrapy.Field()
    thumbnail = scrapy.Field()
