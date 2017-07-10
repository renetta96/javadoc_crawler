import scrapy
from javadoc.items import JavaItem
from javadoc.enums import Version


class PackageSpider(scrapy.Spider):
    name = 'package_java6'
    start_urls = ["https://docs.oracle.com/javase/6/docs/api/overview-summary.html"]

    def parse(self, response):
        limit = int(getattr(self, "limit", 1))
        count = 0

        rows = response.xpath('//table[2]/tr')
        for i in xrange(1, len(rows)):
            count += 1
            row = rows[i]
            cell = row.xpath('.//td[1]/b/a')
            package_name = cell.css("::text").extract_first()
            package_url = response.urljoin(cell.css("::attr(href)").extract_first())

            package_item = JavaItem(name=package_name,
                                    url=package_url,
                                    type='Package',
                                    parent=None,
                                    parent_type=None,
                                    version=Version.JAVA6)
            yield package_item

            if count >= limit >= 0:
                break

