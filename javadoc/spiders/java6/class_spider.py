# -*- coding: utf-8 -*-
import scrapy
from javadoc.spiders.java6.class_detail_spider import ClassDetailSpider


class ClassSpider(scrapy.Spider):
    name = 'class_java6'
    # allowed_domains = ['example.com']

    start_urls = ['https://docs.oracle.com/javase/6/docs/api/allclasses-noframe.html']

    def parse(self, response):
        limit = int(getattr(self, "limit", 1))
        count = 0
        for cls in response.css("a"):
            url = cls.css("::attr(href)").extract_first()
            yield response.follow(url, ClassDetailSpider().parse)
            count += 1
            if count >= limit >= 0:
                break



