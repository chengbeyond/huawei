# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re


class HwSpider(scrapy.Spider):
    name = 'hw'
    allowed_domains = ['vmall.com']
    start_urls = ['https://www.vmall.com']

    def parse(self, response):
        # phone_type = response.xpath("//li[@id='zxnav_0']//ul/li")[1:-1]
        phone_type = response.xpath("//ol[@class='category-list']/li/div[2]/ul/li[@class='subcate-item']")
        for phone in phone_type:
            item = dict()
            item['type'] = phone.xpath("./a/span/text()").extract_first()
            item['link'] = "https://www.vmall.com" + phone.xpath("./a/@href").extract_first()
            yield scrapy.Request(
                item['link'],
                callback=self.parse_info,
                meta={"item": deepcopy(item)}
            )

    def parse_info(self, response):
        item = response.meta['item']
        goods_list = response.xpath("//div[@class='pro-list clearfix']/ul/li")
        for goods in goods_list:
            item['img'] = goods.xpath("./div/p[1]/a/img/@src").extract_first()
            item['title'] = goods.xpath("./div/p[2]/a/@title").extract_first()
            item['href'] = "https://www.vmall.com" + goods.xpath("./div/p[2]/a/@href").extract_first()
            yield scrapy.Request(
                item['href'],
                callback=self.parse_price,
                meta={"item": item}
            )

    def parse_price(self, response):
        item = response.meta['item']
        item['price'] = re.findall(r"\"\", price : \"(.*?)\",", response.body.decode())[0]
        print(item)
        yield item
