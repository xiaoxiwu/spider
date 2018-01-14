# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs


class DoubanSpiderPipeline(object):
    # 初始化时指定要操作的文件
    def __init__(self):
        self.movieFile = codecs.open('movie.json', 'w', encoding='utf-8')
        self.commentFile = codecs.open('comments.json', 'w', encoding='utf-8')

    def open_spider(self, spider): #当spider被开启时，这个方法被调用。
        print spider.name

    # 每个item pipeline组件都需要调用该方法，这个方法必须返回一个 Item (或任何继承类)对象，或是抛出 DropItem异常，被丢弃的item将不会被之后的pipeline组件所处理。

    def process_item(self, item, spider):
        # 参 数:
        # item: 由 parse 方法返回的 Item 对象(Item对象)
        # spider: 抓取到这个 Item 对象对应的爬虫对象(Spider对象)
        if spider.name == 'doubanSpider':
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.movieFile.write(line)
        elif spider.name == 'doubanCommentSpider':
            self.commentFile.write(item['comment'])

        return item

    # 处理结束后关闭 文件 IO 流
    def close_spider(self, spider):
        self.movieFile.close()
        self.commentFile.close()
