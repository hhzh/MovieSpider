# -*- coding: utf-8 -*-
import scrapy


class YinfansSpider(scrapy.Spider):
    name = "yinfans"
    allowed_domains = ["yinfans.com"]
    start_urls = ['http://yinfans.com/']

    def parse(self, response):
        pass