import scrapy
from javadoc.items import JavaItem
from javadoc.enums import Version
import traceback
from javadoc.utils import is_new_page, is_summary, get_summary_type


def _get_item_from_header(text, url, version=Version.JAVA6, override_type=None):
    package = None
    cls_name = None
    _type = None

    for t in text:
        t = t.rstrip("\n").lstrip("\n")
        if len(t) == 0:
            continue

        if not package:
            package = "%s" % t
        elif not (cls_name and _type):
            words = t.split()
            cls_name = words[-1]
            _type = override_type if override_type else " ".join(words[:-1])
            break

    cls_item = JavaItem(name=cls_name, type=_type, parent=package, parent_type="Package", url=url, version=version)
    return cls_item


def _get_item_from_cell(cell, _type, url, parent, version=Version.JAVA6):
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
    name = "class_detail_java6"

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

        header = response.css("h2")[0]
        header_text = header.css("::text").extract()

        cls_item = _get_item_from_header(header_text, response.url, override_type=self._type)
        yield cls_item

        try:
            summary = response.css("td.NavBarCell3")[0]
            for summary_name in summary.css("a").css("::attr(href)").extract():
                summary_name = summary_name.lstrip("#")

                if not is_summary(summary_name):
                    continue

                tables = response.xpath('//p/a[@name="%s"]/parent::p/following::table[1]' % summary_name)
                if len(tables) == 0:
                    tables = response.xpath('//a[@name="%s"]/following::table[1]' % summary_name)

                table = tables[0]

                table_rows = table.css("tr")

                # Handle type
                table_header = table_rows[0].css("b::text").extract_first()
                _type = get_summary_type(table_header)

                # Handler rows
                for i in xrange(1, len(table_rows)):
                    row = table_rows[i]
                    cells = row.css("td")
                    cell = cells[-1]
                    href = cell.css("a::attr(href)").extract_first()
                    url = response.urljoin(href)

                    if is_new_page(url, response.url):
                        yield response.follow(url, ClassDetailSpider(_type=_type).parse)
                    else:
                        sub_item = _get_item_from_cell(cell, _type, url, cls_item)
                        yield sub_item

        except Exception as e:
            with open('exceptions.txt', "a") as exceptions:
                exceptions.write('Exception at ' + response.url + '\n')
                exceptions.write(traceback.format_exc() + '\n')
                exceptions.write('=========================================\n')

            with open('retry_urls.txt', "a") as retry_urls:
                retry_urls.write(response.url + '\n')

