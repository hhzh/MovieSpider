# -*- coding: utf-8 -*-

import pymysql
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline


class MoviespiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='SCMD_2017_scmd', db='spider',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, '')
        movie_sql = "insert into movie (name,title,aka,origin_url,thumbnail,poster,directors,writers,actors,category," \
                    "rating,officia_website,douban_url,intro,lang,countries,year,release_date,mins,IMDb,IMDb_rating," \
                    "awards,printscreen,publish_date,read_count,comment_count,website_url,website_name,sharpness," \
                    "tags,download_name,download_url,pan_name,pan_url,pan_pwd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        link_sql = "insert into movie_link (moive_id,name,link,size,sharpness_id,sharpness_name,website_name) VALUES " \
                   "(%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(movie_sql, (
            item['name'], item['title'], item['aka'], item['origin_url'], item['thumbnail'], item['poster'],
            item['directors'], item['writers'], item['actors'], item['category'], item['rating'],
            item['officia_website'], item['douban_url'], item['intro'], item['lang'], item['countries'], item['year'],
            item['release_date'], item['mins'], item['IMDb'], item['IMDb_rating'], item['awards'], item['printscreen'],
            item['publish_date'], item['read_count'], item['comment_count'], item['website_url'], item['website_name'],
            item['sharpness'], item['tags'], item['download_name'], item['download_url'], item['pan_name'],
            item['pan_url'], item['pan_pwd']))
        movie_id = self.cursor.lastrowid
        link_list = item['link_list']
        if len(link_list):
            for link_item in link_list:
                self.cursor.execute(link_sql, (
                    movie_id, link_item['name'], link_item['link'], link_item['size'], link_item['sharpness_id'],
                    link_item['sharpness_name'], item['website_name']))
        self.conn.commit()
        return item

    def spider_closed(self, spider):
        self.conn.close()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        for field in item.fields:
            item.setdefault(field, '')
        movie_sql = "insert into movie (name,title,aka,origin_url,poster,directors,writers,actors,category,rating," \
                    "officia_website,douban_url,intro,lang,countries,year,mins,IMDb,IMDb_rating,awards,printscreen," \
                    "publish_date,read_count,comment_count,website_url,website_name,sharpness,tags,download_name," \
                    "download_url,pan_name,pan_url,pan_pwd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        link_sql = "insert into movie_link (moive_id,name,link,sharpness_id,sharpness_name,website_name) VALUES " \
                   "(%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(movie_sql, (
            item['name'], item['title'], item['aka'], item['origin_url'], item['thumbnail'], item['directors'],
            item['writers'], item['actors'], item['movie_type'], item['rating'], item['officia_website'],
            item['douban_url'], item['intro'], item['lang'], item['countries'], item['year'], item['mins'],
            item['IMDb'], item['IMDb_rating'], item['awards'], item['printscreen'], item['publish_date'],
            item['read_count'], item['comment_count'], item['website_url'], item['website_name'], item['sharpness'],
            item['tags'], item['download_name'], item['download_url'], item['pan_name'], item['pan_url'],
            item['pan_pwd']))
        # self.cursor.execute(link_sql, (
        #     item['moive_id'], item['name'], item['link'], item['sharpness_id'], item['sharpness_name'],
        #     item['website_name']))


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        pass
