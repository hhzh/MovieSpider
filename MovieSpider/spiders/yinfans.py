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
            title = thumbnail_item.xpath('@title').extract_first('').strip()
            thumbnail = thumbnail_item.xpath('img/@src').extract_first('')

            info_item = li_item.xpath('div[@class="info"]')
            publish_date = info_item.xpath('span[contains(@class,"info_date")]/text()').extract_first('')
            read_count = info_item.xpath('span[contains(@class,"info_views")]/text()').extract_first('')
            comment_count = info_item.xpath('span[contains(@class,"info_comment")]/a/text()').extract_first('')
            category = info_item.xpath('span[contains(@class,"info_category")]/a/text()').extract_first('')
            yield Request(url=origin_url, meta={'title': title, 'thumbnail': thumbnail,
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
        content_text = []
        for p_list in post_content:
            link_type = p_list.xpath('strong/text()').extract_first('')
            link_url = p_list.xpath('strong/a/@href').extract_first('')
            link_name = p_list.xpath('strong/a/b/text()').extract_first('')
            # all_text = p_list.xpath(
            #     'strong/text() | strong/a/@href | strong/text() | strong/a/b/text() | strong/a/text()').extract_first('')
            content_text_temp = p_list.xpath('text()').extract()
            if content_text_temp:
                content_text.append(content_text_temp)
            content_img = p_list.xpath('a/img/@src').extract()
        # tags = response.xpath('//div[@class="article_tags"]/div[@class="tagcloud"]/a/text()').extract()

        title = response.meta.get('title', '')
        thumbnail = response.meta.get('thumbnail', '')
        read_count = response.meta.get('read_count', '')
        comment_count = response.meta.get('comment_count', '')
        category = response.meta.get('category', '')
        item['title'] = title
        item['origin_url'] = response.url
        if content_text:
            for sub_content in content_text:
                sub_content = sub_content.strip().replace(' ', '')
                sub_content = sub_content.replace('　', '')
                if '◎译名' in sub_content:
                    item['aka'] = sub_content
                elif '◎片名' in sub_content:
                    item['name'] = sub_content
                elif '◎年代' in sub_content:
                    item['year'] = sub_content
                elif '◎国家' in sub_content:
                    item['countries'] = sub_content
                elif '◎类别' in sub_content:
                    item['tags'] = sub_content
                elif '◎语言' in sub_content:
                    item['lang'] = sub_content
                elif '◎上映日期' in sub_content:
                    item['release_data'] = sub_content
                elif '◎ＩＭＤＢ' in sub_content and '分' in sub_content:
                    item['IMDb_rating'] = sub_content
                elif '◎ＩＭＤＢhttp' in sub_content:
                    item['IMDb'] = sub_content
                elif '◎豆瓣评分' in sub_content:
                    item['rating'] = sub_content
                elif '◎豆瓣链接' in sub_content:
                    item['douban_url']=sub_content
                elif '◎片长' in sub_content:
                    item['mins']=sub_content
                elif '◎导演' in sub_content:
                    item['directors']=sub_content
                elif '◎主演' in sub_content:
                    item['actors']=sub_content
