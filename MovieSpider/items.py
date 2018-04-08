# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
import datetime
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def date_covert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_nums(value):
    nums = 0
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    return nums


def get_list(value):
    return [value]

class MoviespiderItem(scrapy.Item):
    pass


class YinfansItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    aka = scrapy.Field()
    origin_url = scrapy.Field()
    thumbnail = scrapy.Field()
    poster = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    actors = scrapy.Field()
    category = scrapy.Field()
    rating = scrapy.Field()
    officia_website = scrapy.Field()
    douban_url = scrapy.Field()
    intro = scrapy.Field()
    lang = scrapy.Field()
    countries = scrapy.Field()
    year = scrapy.Field()
    release_date = scrapy.Field()
    mins = scrapy.Field()
    IMDb = scrapy.Field()
    IMDb_rating = scrapy.Field()
    awards = scrapy.Field()
    printscreen = scrapy.Field(
        output_processor=Join(',')
    )
    publish_date = scrapy.Field()
    read_count = scrapy.Field()
    comment_count = scrapy.Field()
    website_url = scrapy.Field()
    website_name = scrapy.Field()
    sharpness = scrapy.Field()
    tags = scrapy.Field()
    download_name = scrapy.Field()
    download_url = scrapy.Field()
    pan_name = scrapy.Field()
    pan_url = scrapy.Field()
    pan_pwd = scrapy.Field()
    link_list = scrapy.Field()
