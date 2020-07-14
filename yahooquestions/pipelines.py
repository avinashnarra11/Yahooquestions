# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class YahooquestionsPipeline:

    def __init__(self):
        self.conn = sqlite3.connect('yahoo_new.db')
        self.curr = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS questions_tb""")
        self.curr.execute("""create table questions_tb(
                        qid text PRIMARY KEY ,
                        title text,
                        detail text,
                        answerscount text,
                        thumbUpsCount text,
                        CreatedTime text,
                        categoryname text,
                        main_category text
                        ) """)

    def process_item(self, item, spider):
        self.store_db(item)
        return item


    def store_db(self, item):
        qid = item['qid']
        title = item['title']
        detail = item['detail']
        answerscount = item['answerscount']
        thumbUpsCount = item['thumbUpsCount']
        CreatedTime = item['CreatedTime']
        categoryname = item['categoryname']
        main_category = item['main_category']

        self.curr.execute("insert or ignore into questions_tb values (?,?,?,?,?,?,?,?)",
        (
            qid,title,detail,answerscount,thumbUpsCount,CreatedTime,categoryname,main_category
        ))
        self.conn.commit()
