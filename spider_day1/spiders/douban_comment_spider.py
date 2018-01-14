# -*- coding: utf-8 -*-

import scrapy
import re
import time
from scrapy.http import Request
from spider_day1.spiders.sim_login import DoubanLogin
from spider_day1.items import CommentItem


class DoubanSpider(scrapy.Spider):
    cookie = {}
    maxPage = 499
    """docstring for DoubanSpider"""
    name = "doubanCommentSpider"
    allowed_domains = ["movie.douban.com", "accounts.douban.com"]
    start_urls = ['https://movie.douban.com/subject/26654146/comments?start=1&limit=20&sort=new_score&status=P']

    def __init__(self):
        self.login()

    def login(self):
        login = DoubanLogin()
        cookieTrupleList = login.login('18124503375', 'meier2008')
        cookie = {}
        for cookieTruple in cookieTrupleList:
            cookie[cookieTruple[0]] = cookieTruple[1]

        self.cookie = cookie
        print cookie

    def doRequests(self, start):
        commentTemplateUrl = "https://movie.douban.com/subject/26654146/comments?start={}&limit=20&sort=new_score&status=P"
        url = commentTemplateUrl.format(str(start))
        preUrl= commentTemplateUrl.format(str(start-1))
        # 模拟headers
        headers = {
            'referer': preUrl,
            'host': 'movie.douban.com'
        }
        time.sleep(3000)
        yield Request(url=url, cookies=self.cookie, callback=self.parse, headers=headers)

    def parse(self, response):
        items = []
        status = response.status
        url = response.url
        start = int(url[url.index('=') + 1:url.index('=') + 2])
        if status == 200:
            selector = scrapy.Selector(response)
            comments = selector.xpath('//div[@id="comments"]/div[@class="comment-item"]/div[@class="comment"]/p')
            for comment in comments:
                item = CommentItem()
                item['comment'] = comment.xpath('./text()').extract()[0]
                items.append(item)

            if start < self.maxPage:
                self.doRequests(start + 1)
        else:
            if start < self.maxPage:
                self.login()
                self.doRequests(start)
        return items
