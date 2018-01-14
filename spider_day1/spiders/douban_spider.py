# -*- coding: utf-8 -*-

import scrapy
import re
from spider_day1.items import MovieItem


class DoubanSpider(scrapy.Spider):
    """docstring for DoubanSpider"""
    name = "doubanSpider"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/subject/26654146/"]
    starsWightDic = {u"5星": "fiveStarPercent", u"4星": "fourStarPercent", u"3星": "threeStarPercent", u"2星": "twoStarPercent",
                     u"1星": "oneStarPercent"}

    def getStarVal(self, key):
        return self.starsWightDic[key]

    def parse(self, respose):
        selector = scrapy.Selector(respose)
        item = MovieItem()

        item['name'] = selector.xpath('//div[@id="content"]/h1/span[@property="v:itemreviewed"]/text()').extract()[0]
        item['director'] = \
            selector.xpath('//div[@id="info"]/span/span[@class="attrs"]/a[@rel="v:directedBy"]/text()').extract()[0]
        item['editor'] = \
            selector.xpath(
                '//div[@id="info"]/span/span[@class="attrs"]/a[@href="/celebrity/1357205/"]/text()').extract()[
                0] + "," + selector.xpath(
                '//div[@id="info"]/span/span[@class="attrs"]/a[@href="/celebrity/1006330/"]/text()').extract()[0]

        actors = selector.xpath(
            '//div[@id="info"]/span[@class="actor"]/span[@class="attrs"]/a')
        actorsText = ""
        for actor in actors:
            actorText = actor.xpath('./text()').extract()[0]
            actorsText = actorsText + "," + actorText
        item['actors'] = actorsText[1:]

        categories = selector.xpath(
            '//div[@id="info"]/span[@property="v:genre"]')
        categoriesText = ""
        for category in categories:
            categoryText = category.xpath('./text()').extract()[0]
            categoriesText = categoriesText + "," + categoryText
        item['category'] = categoriesText[1:]

        # 提取非标签元素
        item['region'] = selector.xpath(
            u'//div[@id="info"]/span[contains(./text(), "制片国家/地区:")]/following::text()[1]').extract()[0]
        item['language'] = selector.xpath(
            u'//div[@id="info"]/span[contains(./text(), "语言:")]/following::text()[1]').extract()[0]

        item['releaseDay'] = \
            selector.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/text()').extract()[0]
        # 获取标签属性
        item['timeByMinute'] = selector.xpath('//div[@id="info"]/span[@property="v:runtime"]/@content').extract()[0]
        item['alias'] = selector.xpath(
            u'//div[@id="info"]/span[contains(./text(), "又名:")]/following::text()[1]').extract()[0]

        # 剧情简介
        synopsis = selector.xpath('//div[@id="link-report"]/span[@property="v:summary"]/text()').extract()[0]
        # strip()去除两端空格
        item['synopsis'] = synopsis.strip()

        # 评分解析
        item['doubanRating'] = selector.xpath(
            '//div[@id="interest_sectl"]/div[@class="rating_wrap clearbox"]/div[@class="rating_self clearfix"]/strong/text()').extract()[
            0]
        item['ratingPepoles'] = selector.xpath(
            '//div[@id="interest_sectl"]/div[@class="rating_wrap clearbox"]/div[@class="rating_self clearfix"]/div[@class="rating_right "]/div[@class="rating_sum"]/a/span/text()').extract()[
            0]

        # 豆瓣星评
        ratingWeightDivs = selector.xpath(
            '//div[@id="interest_sectl"]/div[@class="rating_wrap clearbox"]/div[@class="ratings-on-weight"]/div[@class="item"]')
        sum = 0
        for ratingWeightDiv in ratingWeightDivs:
            stars = ratingWeightDiv.xpath('./span[contains(@class,"starstop")]/text()').extract()[0]
            weights = ratingWeightDiv.xpath('./span[@class="rating_per"]/text()').extract()[0]
            star = int(stars.strip()[0:1])
            weight = float(weights[:-1])/100
            sum += star*weight

            item[self.getStarVal(stars.strip())] = weights

        item['doubanStars'] = sum
        print item['doubanStars']

        items = []
        items.append(item)
        return items

