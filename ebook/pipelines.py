# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.http import Request
import MySQLdb
import requests
import os
import pdb

class EbookPipeline(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "qinhaoyan945520.", "ebook", charset='utf8')

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        if(cursor.execute('select * from ebookapp_book where title="'+item['title']+'"')==0):
            book = requests.get(item['url'],timeout=1800)
            if(book.status_code == 200):
                bookf = open(os.path.dirname(os.path.realpath(__file__))+'/book/'+item['title']+'.txt','wb')
                bookf.write(book.content)
                bookf.close()
                img = requests.get(item['img'])
                if(img.status_code == 200):
                    imgf = open(os.path.dirname(os.path.realpath(__file__))+'/img/'+item['title']+'.jpg','ab')
                    imgf.write(img.content)
                    imgf.close()
                
                cursor.execute('insert into ebookapp_book (title,btype,author,brief) values ("'+item['title']+'","'+item['btype']+'","'+item['author']+'","'+item['brief']+'")')
                self.db.commit()
        return item
    def close_spider(self,spider):
        self.db.close()


