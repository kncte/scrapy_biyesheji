# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiyeshejiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    country = scrapy.Field()
    address = scrapy.Field()
    type = scrapy.Field()
    duration = scrapy.Field()
    jianjie = scrapy.Field()


class MusicItem(scrapy.Item):
    name = scrapy.Field()
    music_id = scrapy.Field()
    singer = scrapy.Field()
    Album_Name = scrapy.Field()
    Album_pic = scrapy.Field()
    mp3_url = scrapy.Field()


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    urls = scrapy.Field()
    time = scrapy.Field()
    new_from = scrapy.Field()
