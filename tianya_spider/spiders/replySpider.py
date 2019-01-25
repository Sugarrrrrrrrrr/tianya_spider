# -*- coding: utf-8 -*-
import scrapy
from tianya_spider.items import ReplyItem
from utils import get_block_pid_from_post_url
from utils import get_reply_urls
import config


class ReplySpider(scrapy.Spider):
    name = 'replySpider'
    allowed_domains = ['tianya.cn']
    start_urls = ['http://bbs.tianya.cn/post-free-6029190-1.shtml']

    custom_settings = {
        'CONCURRENT_REQUESTS': 128,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 64,
        'CONCURRENT_REQUESTS_PER_IP': 32,
        'DEPTH_LIMIT': config.REPLYSPIDER_DEPTH_LIMIT,
        'ITEM_PIPELINES': {
            'tianya_spider.pipelines.ReplySpiderPipeline': 543,
        }
    }

    def __init__(self):
        super(ReplySpider, self).__init__()
        # self.start_urls = ['http://bbs.tianya.cn/post-free-6029190-2.shtml']
        self.start_urls = get_reply_urls()
        pass

    def parse(self, response):
        try:
            url = response.url
            block_and_pid = get_block_pid_from_post_url(url)
            if block_and_pid:
                block, pid = block_and_pid
            for i, alt_item in enumerate(response.xpath("//div[@class='atl-item']")):
                floor = alt_item.xpath("./@id").extract_first()
                # f_host = alt_item.xpath("./@_host").extract_first()
                uid = alt_item.xpath("./@_hostid").extract_first()
                rid = alt_item.xpath("./@replyid").extract_first()
                time = alt_item.xpath("./@js_restime").extract_first()
                content = alt_item.xpath("./div[2]/div[2]/div/text()").extract_first().strip()

                item = ReplyItem()
                item['floor'] = int(floor)
                item['pid'] = pid
                item['block'] = block
                item['uid'] = uid
                item['rid'] = rid
                item['time'] = time
                item['content'] = content
                yield item
            next_page = response.xpath("//a[@class='js-keyboard-next']/@href").extract_first()
            if next_page:
                url = 'http://bbs.tianya.cn' + next_page
                print(url)
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)
        except Exception as e:
            print(2, e)

