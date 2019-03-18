# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    collection = 'amazon'  # 数据表

    b_cate = scrapy.Field()  # 大分类
    m_cate = scrapy.Field()  # 中分类
    s_cate = scrapy.Field()  # 小分类
    s_href = scrapy.Field()  # 小分类url
    name = scrapy.Field()  # 商品名称
    goods_url = scrapy.Field()  # 商品url
    brand = scrapy.Field()  # 商品品牌
    price = scrapy.Field()  # 商品价格
    freight = scrapy.Field()  # 运费
    grade = scrapy.Field()  # 评分（满分5分）
    comment_count = scrapy.Field()  # 评论人数

