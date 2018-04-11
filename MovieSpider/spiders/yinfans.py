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
                                                'comment_count': comment_count, 'category': category},
                          callback=self.parse_detail)
            next_url = response.xpath('//div[@class="pagination"]/a[@class="next"]/@href').extract_first('')
            if next_url:
                yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        item = YinfansItem()
        # article_container = response.xpath(
        #     '//div[@class="container"]/div[@id="content"]/div[contains(@class,"artcile_container")]')
        # post_content = article_container.xpath('div[@class="context"]/div[@id="post_content"]')
        # poster = post_content.xpath('p[0]/a/@href').extract_first('')
        post_content = response.xpath('//div[@id="post_content"]/p | //div[@id="post_content"]/div | //div[@id="post_content"]/div/p')
        poster = post_content.xpath('a[contains(@href,".jpg")]/@href').extract_first('')
        content_text = []
        sharpness_id = 0
        sharpness_name = ''
        link_list = []
        content_img = []
        for p_list in post_content:
            strong_text_ori = p_list.xpath(
                'strong[last()]/text() | text() |strong[last()]/strong/text()').extract()
            link_url = p_list.xpath('strong/a[contains(@href,"magnet")]/@href').extract_first('')
            link_name = p_list.xpath('strong/a/b/text() | strong/a[contains(@href,"magnet")]/text()').extract_first(
                '').strip()
            movie_size = '0GB'
            strong_text = [x for x in strong_text_ori if x.strip() != '']
            if len(strong_text):
                if len(strong_text) == 2 and strong_text == 'GB':
                    strong_text = strong_text[0] + strong_text[1]
                else:
                    strong_text = strong_text[-1].strip()
                if strong_text.startswith('4K MKV'):
                    sharpness_id = 1
                    sharpness_name = '4K MKV磁力链'
                elif strong_text.startswith('4K蓝光'):
                    sharpness_id = 2
                    sharpness_name = '4K蓝光原盘磁力链'
                elif strong_text.startswith('蓝光原盘'):
                    sharpness_id = 3
                    sharpness_name = '蓝光原盘磁力链'
                elif strong_text.startswith('3D蓝光'):
                    sharpness_id = 4
                    sharpness_name = '3D蓝光原盘'
                elif strong_text.startswith('高清MKV'):
                    sharpness_id = 5
                    sharpness_name = '高清MKV磁力链'
                elif strong_text.startswith('3D高清MKV'):
                    sharpness_id = 6
                    sharpness_name = '3D高清MKV磁力链'
                elif 'G' in strong_text or 'M' in strong_text:
                    movie_size = strong_text

            if link_url:
                # if movie_size == '0GB' or movie_size == 'GB':
                #     print('-------' + str(response.url) + str(strong_text) + '----' + str(strong_text_ori))
                link_list.append({'name': link_name, 'link': link_url, 'size': movie_size, 'sharpness_id': sharpness_id,
                                  'sharpness_name': sharpness_name})
            # movie_size=p_list.xpath('strong/text()')
            # all_text = p_list.xpath(
            #     'strong/text() | strong/a/@href | strong/text() | strong/a/b/text() | strong/a/text()').extract_first('')
            content_text_temp = p_list.xpath(
                'text() | span/text() | div/text() | span/span/text() | span/span/span/text() | div/div/div/p/text()').extract()
            if content_text_temp:
                content_text.extend(content_text_temp)
            content_img_temp = p_list.xpath('a/img/@src').extract()
            if content_img_temp:
                content_img.extend(content_img_temp)
        # tags = response.xpath('//div[@class="article_tags"]/div[@class="tagcloud"]/a/text()').extract()

        title = response.meta.get('title', '')
        thumbnail = response.meta.get('thumbnail', '')
        read_count = response.meta.get('read_count', '')
        comment_count = response.meta.get('comment_count', '')
        category = response.meta.get('category', '')
        publish_date = response.meta.get('publish_date', '')
        item['title'] = title
        item['origin_url'] = response.url
        item['thumbnail'] = thumbnail
        item['read_count'] = read_count
        item['comment_count'] = comment_count
        item['category'] = category
        item['link_list'] = link_list
        item['publish_date'] = publish_date
        item['website_url'] = 'http://www.yinfans.com'
        item['website_name'] = '音范丝'
        item['poster'] = poster
        item['printscreen'] = ','.join(content_img)

        if content_text:
            new_content = []
            for content_temp in content_text:
                content_temp = content_temp.strip().replace(' ', '')
                content_temp = content_temp.replace('　', '')
                content_temp = content_temp.replace('\xa0', '')
                content_temp = content_temp.replace('：', '')
                content_temp = content_temp.replace(':', '')
                if content_temp.startswith('◎') or content_temp.startswith('【'):
                    new_content.append(content_temp)
                elif len(new_content) > 0:
                    last_element = new_content.pop()
                    new_content.append(last_element + '/' + content_temp)
            # if response.url == 'http://www.yinfans.com/movie/12034':
            #     item['aka'] = str(new_content)
            for sub_content in new_content:
                # sub_content = sub_content.strip().replace(' ', '')
                # sub_content = sub_content.replace('　', '')
                if '◎译名' in sub_content:
                    item['aka'] = sub_content[3:]
                elif '◎片名' in sub_content:
                    item['name'] = sub_content[3:]
                elif '◎年代' in sub_content:
                    item['year'] = sub_content[3:]
                elif '◎国家' in sub_content:
                    item['countries'] = sub_content[3:]
                elif '◎类别' in sub_content:
                    item['tags'] = sub_content[3:]
                elif '◎语言' in sub_content:
                    item['lang'] = sub_content[3:]
                elif '◎上映日期' in sub_content:
                    item['release_date'] = sub_content[5:]
                elif '◎ＩＭＤＢ' in sub_content and '分' in sub_content:
                    item['IMDb_rating'] = sub_content[5:]
                elif '◎ＩＭＤＢhttp' in sub_content:
                    item['IMDb'] = sub_content[5:]
                elif '◎豆瓣评分' in sub_content:
                    item['rating'] = sub_content[5:]
                elif '◎豆瓣链接' in sub_content:
                    item['douban_url'] = sub_content[5:]
                elif '◎片长' in sub_content:
                    item['mins'] = sub_content[3:]
                elif '◎导演' in sub_content:
                    item['directors'] = sub_content[3:]
                elif '◎主演' in sub_content:
                    item['actors'] = sub_content[3:]
                elif '◎简介' in sub_content:
                    item['intro'] = sub_content[3:]
                elif '◎获奖情况' in sub_content:
                    item['awards'] = sub_content[5:]
                elif '【中文译名】' in sub_content:
                    item['aka'] = sub_content[6:]
                elif '【影片原名】' in sub_content:
                    item['name'] = sub_content[6:]
                elif '【出品年代】' in sub_content:
                    item['year'] = sub_content[6:]
                elif '【国家】' in sub_content:
                    item['countries'] = sub_content[4:]
                elif '【类别】' in sub_content:
                    item['tags'] = sub_content[4:]
                elif '【语言】' in sub_content:
                    item['lang'] = sub_content[4:]
                elif '【上映日期】' in sub_content:
                    item['release_date'] = sub_content[6:]
                elif '【IMDB评分】' in sub_content:
                    item['IMDb_rating'] = sub_content[8:]
                elif '【导演】' in sub_content:
                    item['directors'] = sub_content[4:]
                elif '【主演】' in sub_content:
                    item['actors'] = sub_content[4:]
                elif '【内容简介】' in sub_content:
                    item['intro'] = sub_content[6:]
        yield item
