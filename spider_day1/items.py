# -*- coding: utf-8 -*-

# 定义要爬取的数据的Model

from scrapy.item import Item,Field


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # 电影名字
    name=Field()
    #电影导演
    director=Field()
    #电影编剧
    editor=Field()
    #主演
    actors=Field()
    #电影类型
    category=Field()
    #制片国家/地区
    region=Field()
    #语言
    language=Field()
    #上映日期
    releaseDay=Field()
    #片长
    timeByMinute=Field()
    #别名
    alias=Field()
    #剧情简介
    synopsis=Field()
    #豆瓣评分
    doubanRating=Field()
    #豆瓣评星
    doubanStars=Field()
    #参评人数
    ratingPepoles=Field()
    #5星占比
    fiveStarPercent=Field()
    #4星占比
    fourStarPercent=Field()
    #3星占比
    threeStarPercent=Field()
    #2星占比
    twoStarPercent=Field()
    #1星占比
    oneStarPercent=Field()





