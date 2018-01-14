# -*- coding: utf-8 -*-

import scrapy


class DoubanSpider(scrapy.Spider):
    """docstring for DoubanSpider"""
    name = "doubanSpiderDay"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/subject/26654146/"]

    def parse(self, respose):
        print respose.body
