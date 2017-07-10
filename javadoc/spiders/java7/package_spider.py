import scrapy
from javadoc.items import JavaItem
from javadoc.enums import Version


class PackageSpider(scrapy.Spider):
    name = 'package_java7'
    start_urls = ["https://docs.oracle.com/javase/7/docs/api/overview-summary.html"]

    def parse(self, response):
        limit = int(getattr(self, "limit", 1))
        count = 0

        cells = response.css('table.overviewSummary td.colFirst')
        for i in xrange(1, len(cells)):
            count += 1
            cell = cells[i]
            package_name = cell.css("a::text").extract_first()
            package_url = response.urljoin(cell.css("a::attr(href)").extract_first())

            package_item = JavaItem(name=package_name,
                                    url=package_url,
                                    type='Package',
                                    parent=None,
                                    parent_type=None,
                                    version=Version.JAVA7)
            yield package_item

            if count >= limit >= 0:
                break

