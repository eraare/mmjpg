# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MmjpgItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    image_path = scrapy.Field()
    image_title = scrapy.Field()
    image_referer = scrapy.Field()
    # 使用ImagesPipeline所需
    image_urls = scrapy.Field()
    images = scrapy.Field()
