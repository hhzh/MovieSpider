# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
from MovieSpider.items import YinfansItem


class YinfansSpider(scrapy.Spider):
    name = "yinfans"
    allowed_domains = ["yinfans.com"]
    start_urls = ['http://www.yinfans.com/']

    def parse(self, response):
        li_items = response.xpath('//div[@class="container"]/div[@class="mainleft"]/ul[@id="post_container"]/li')
        for li_item in li_items:
            thumbnail_item = li_item.xpath('div[@class="thumbnail"]/a')
            origin_url = thumbnail_item.xpath("@href").extract_first('')
            title = thumbnail_item.xpath('@title').extract_first('')
            thumbnail = thumbnail_item.xpath('img/@src').extract_first('')

            info_item = li_item.xpath('div[@class="info"]')
            publish_date = info_item.xpath('span[contains(@class,"info_date")]/text()').extract_first('')
            read_count = info_item.xpath('span[contains(@class,"info_views")]/text()').extract_first('')
            comment_count = info_item.xpath('span[contains(@class,"info_comment")]/a/text()').extract_first('')
            category = info_item.xpath('span[contains(@class,"info_category")]/a/text()').extract_first('')
            yield Request(url=origin_url, meta={'origin_url': origin_url, 'title': title, 'thumbnail': thumbnail,
                                                'publish_date': publish_date, 'read_count': read_count,
                                                'comment_count': 'comment_count', 'category': category},
                          callback=self.parse_detail)
            # next_url = response.xpath('//div[@class="pagination"]/a[@class="next"]/@href').extract_first('')
            # if next_url:
            #     yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        item = YinfansItem()
        # article_container = response.xpath(
        #     '//div[@class="container"]/div[@id="content"]/div[contains(@class,"artcile_container")]')
        # post_content = article_container.xpath('div[@class="context"]/div[@id="post_content"]')
        # poster = post_content.xpath('p[0]/a/@href').extract_first('')
        post_content = response.xpath('//div[@id="post_content"]/p')
        poster = post_content.xpath('a/@href').extract_first('')
        for p_list in post_content:
            a_href = p_list.xpath('a/@href').extract_first('')
            all_text = p_list.xpath(
                'strong/text() | strong/a/Href | strong/text() | strong/a/b/text() | strong/a/text()').extract_first('')
            content_text=p_list.xpath('text()').extract()
