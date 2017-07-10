import scrapy
from javadoc.spiders.java8.class_detail_spider import ClassDetailSpider


class ClassSpider(scrapy.Spider):
    name = 'class_java8'
    start_urls = ['https://docs.oracle.com/javase/8/docs/api/allclasses-noframe.html']

    def parse(self, response):
        limit = int(getattr(self, "limit", 1))
        count = 0
        for cls in response.css("div.indexContainer ul li a"):
            url = cls.css("::attr(href)").extract_first()
            yield response.follow(url, ClassDetailSpider().parse)
            count += 1
            if count >= limit >= 0:
                break
