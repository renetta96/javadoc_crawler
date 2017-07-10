import scrapy
from javadoc.items import JavaItem
from javadoc.enums import Version
from javadoc.utils import is_summary, is_new_page, get_summary_type
import traceback


def _get_item_from_header(header, url, version=Version.JAVA7, override_type=None):
    package = header.css('div.subTitle::text').extract_first()
    text = header.css('h2.title::text').extract_first()

    words = text.split()
    _type = override_type if override_type else " ".join(words[:len(words) - 1])
    cls_name = words[len(words) - 1]

    cls_item = JavaItem(name=cls_name, type=_type, parent=package, parent_type="Package", url=url, version=version)
    return cls_item


def _get_item_from_cell(cell, _type, url, parent, version=Version.JAVA7):
    item_name = cell.css("a::text").extract_first()
    parent_name = parent['parent'] + '.' + parent['name']
    parent_type = parent['type']

    item = JavaItem(name=item_name,
                    url=url,
                    type=_type,
                    version=version,
                    parent=parent_name,
                    parent_type=parent_type)
    return item


class ClassDetailSpider(scrapy.Spider):
    name = 'class_detail_java7'

    def __init__(self, _type=None, *args, **kwargs):
        super(ClassDetailSpider, self).__init__(*args, **kwargs)
        self._type = _type

        if kwargs.get('start_url', None):
            self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        if response.status != 200:
            with open("failed_urls.txt", "a") as failed_urls:
                failed_urls.write(response.url + '\n')

            return

        header = response.css("div.header")[0]

        cls_item = _get_item_from_header(header, response.url, override_type=self._type)
        yield cls_item

        try:
            for summary_name in response.css('div.subNav ul.subNavList')[0].css('li a::attr(href)').extract():
                summary_name = summary_name.lstrip("#")

                if not is_summary(summary_name):
                    continue
                
                location = response.xpath('//a[@name="%s"]' % summary_name)[0]
                table_header = location.xpath('.//following::h3[1]/text()').extract_first()
                _type = get_summary_type(table_header)

                table = location.xpath('.//following::table[1]')
                rows = table.css("tr")

                for i in xrange(1, len(rows)):
                    row = rows[i]
                    cells = row.css('td')
                    cell = cells[len(cells) - 1]

                    href = cell.css('a::attr(href)').extract_first()
                    url = response.urljoin(href)

                    if is_new_page(url, response.url):
                        yield response.follow(url, ClassDetailSpider(_type=_type).parse)
                    else:
                        sub_item = _get_item_from_cell(cell, _type, url, cls_item)
                        yield sub_item

        except Exception:
            with open('exceptions.txt', "a") as exceptions:
                exceptions.write('Exception at ' + response.url + '\n')
                exceptions.write(traceback.format_exc() + '\n')
                exceptions.write('=========================================\n')

            with open('retry_urls.txt', "a") as retry_urls:
                retry_urls.write(response.url + '\n')



