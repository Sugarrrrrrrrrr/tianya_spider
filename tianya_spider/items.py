# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # in use
    post_href = scrapy.Field()
    # unused
    face = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()
    author_href = scrapy.Field()
    author = scrapy.Field()
    click = scrapy.Field()
    reply = scrapy.Field()
    time = scrapy.Field()


class UserItem(scrapy.Item):
    uid = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    follow = scrapy.Field()
    fans = scrapy.Field()
    score = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    birthday = scrapy.Field()
    note = scrapy.Field()
    career_category = scrapy.Field()
    career = scrapy.Field()
    tags = scrapy.Field()
    school = scrapy.Field()
    url = scrapy.Field()


class PostItem(scrapy.Item):
    title = scrapy.Field()
    pid = scrapy.Field()
    block = scrapy.Field()
    uid = scrapy.Field()
    name = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    click = scrapy.Field()
    reply = scrapy.Field()
    comment = scrapy.Field()
    url = scrapy.Field()


class ReplyItem(scrapy.Item):
    floor = scrapy.Field()
    pid = scrapy.Field()
    block = scrapy.Field()
    uid = scrapy.Field()
    name = scrapy.Field()
    rid = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
