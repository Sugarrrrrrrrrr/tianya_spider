# -*- coding: utf-8 -*-
import scrapy
from tianya_spider.items import ListItem
from utils import get_block_urls
import config


class ListSpider(scrapy.Spider):
    name = 'listSpider'
    allowed_domains = ['tianya.cn']
    start_urls = ["http://bbs.tianya.cn/list-free-1.shtml"]

    custom_settings = {
        'DEPTH_LIMIT': config.LISTSPIDER_DEPTH_LIMIT,
        'ITEM_PIPELINES': {
            'tianya_spider.pipelines.ListSpiderPipeline': 543,
        }
    }

    def __init__(self):
        super(ListSpider, self).__init__()
        # self.start_urls = ['http://bbs.tianya.cn/post-free-6029190-2.shtml']
        self.start_urls = get_block_urls()
        pass

    def parse(self, response):
        for i, each_tbody in enumerate(response.xpath("//tbody")):
            for j, each_tr in enumerate(each_tbody.xpath("./tr")):
                item = ListItem()

                face = each_tr.xpath("./td/span/@title").extract_first()
                if face:
                    post_href = each_tr.xpath("./td/a/@href").extract_first()
                    title = each_tr.xpath("./td/a/text()").extract_first().strip()
                    images = each_tr.xpath("./td/a/span/@title").extract_first()
                    author_href = each_tr.xpath("./td/a[@class='author']/@href").extract_first()
                    author = each_tr.xpath("./td/a[@class='author']/text()").extract_first()
                    click = each_tr.xpath("./td[3]/text()").extract_first()
                    reply = each_tr.xpath("./td[4]/text()").extract_first()
                    time = each_tr.xpath("./td[5]/@title").extract_first()

                    item['face'] = face
                    item['post_href'] = post_href
                    item['title'] = title
                    item['images'] = images
                    item['author_href'] = author_href
                    item['author'] = author
                    item['click'] = click
                    item['reply'] = reply
                    item['time'] = time
                    yield item
                else:
                    print("!!!!!!!!!!check!!!!!!!!!!")
                    pass
        next_page = response.xpath("//div[@id='main']/div/div[@class='links']/a[@rel='nofollow']/@href").extract_first()
        url = 'http://bbs.tianya.cn' + next_page
        yield scrapy.Request(url, callback=self.parse)
