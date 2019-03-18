# -*- coding: utf-8 -*-
import scrapy
from amazon.items import AmazonItem
from copy import deepcopy


class YmxSpider(scrapy.Spider):
    name = 'ymx'
    allowed_domains = ['amazon.cn']
    start_urls = ['https://www.amazon.cn/gp/site-directory/ref=nav_deepshopall_variant_fullstore_l1']

    def parse(self, response):
        # print(response.text)
        item = AmazonItem()
        div_list = response.xpath("//div[contains(@class,'a-spacing-top-medium')][7]")  # 选取第5个的分类来爬，全部爬取去掉[5]
        # 大分类分组
        for div in div_list:
            item['b_cate'] = div.xpath(".//span[contains(@class,'sd-fontSizeL1')]/a/text()").extract()
            # print(item['b_cate'])
            m_list = div.xpath(".//div[contains(@class,'sd-columnSize')]")
            # 中间分类分组
            for m in m_list:
                item['m_cate'] = m.xpath(".//span[@class='sd-fontSizeL2 a-text-bold']/a/text()").extract_first()
                # print(item['m_cate'])
                ul_list = m.xpath(".//div[@class='a-row']/ul//span[@class='sd-fontSizeL2']")
                # 小分类分组
                for ul in ul_list:
                    item['s_cate'] = ul.xpath("./a/text()").extract_first()
                    item['s_href'] = ul.xpath("./a/@href").extract_first()
                    item['s_href'] = 'https://www.amazon.cn' + item['s_href']
                    # print(item['s_cate'])
                    if item['s_href'] is not None:
                        yield scrapy.Request(
                            item['s_href'],
                            callback=self.parse_detial,
                            meta={"item": deepcopy(item)}
                        )

    def parse_detial(self, response):
        item = response.meta["item"]
        li_list = response.xpath("//div[@id='mainResults' or 'atfResults']/ul/li")
        for li in li_list:
            item["name"] = li.xpath(".//a[contains(@class,'s-access-detail-page')]/@title").extract_first()
            item["goods_url"] = li.xpath(".//a[contains(@class,'s-access-detail-page')]/@href").extract_first()
            item["brand"] = li.xpath(".//span[contains(@class,'a-size-small')][2]/text()").extract_first()
            item["price"] = li.xpath(".//span[contains(@class,'s-price')]/text()").extract_first()
            freight = li.xpath(".//div[contains(@class,'a-spacing-mini')][2]/div/span[2]/text()").extract_first()
            if freight is not None:
                item["freight"] = freight
            else:
                item["freight"] = '免运费'
            grade = li.xpath(".//span[contains(@class,'a-declarative')]//span/text()").extract_first()
            if grade is not None:
                item["grade"] = grade
            else:
                item["grade"] = '暂无评分'
            comment_count = li.xpath(".//span[contains(@class,'a-declarative')]/../../a[contains(@class,'a-size-small')]/text()").extract_first()
            if comment_count is not None:
                item["comment_count"] = comment_count
            else:
                item["comment_count"] = '暂无评论'
            # print(item)
            yield item

        #下一页
        next_url = response.xpath("//a[@id='pagnNextLink']/@href").extract_first()
        if next_url is not None:
            next_url = 'https://www.amazon.cn' + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse_detial,
                meta={"item": item}
            )



