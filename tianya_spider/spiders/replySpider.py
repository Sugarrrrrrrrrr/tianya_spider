# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy_redis.spiders import RedisSpider
from tianya_spider.items import ReplyItem
from utils import get_block_pid_from_post_url
from utils import get_reply_urls
from utils import get_time
from utils import remove_reply_url
import config
import logging


class ReplySpider(RedisSpider):
    name = 'replySpider'
    allowed_domains = ['tianya.cn']
    start_urls = ['http://bbs.tianya.cn/post-free-6029190-1.shtml']

    custom_settings = {
        'CONCURRENT_REQUESTS': 256,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 128,
        'CONCURRENT_REQUESTS_PER_IP': 64,
        'DOWNLOAD_TIMEOUT': 30,
        'REDIRECT_ENABLED': False,
        'DEPTH_LIMIT': config.REPLYSPIDER_DEPTH_LIMIT,
        'LOG_LEVEL': config.LOG_LEVEL,
        'ITEM_PIPELINES': {
            'tianya_spider.pipelines.ReplySpiderPipeline': 543,
            # Store scraped item in redis for post-processing.
            # 'scrapy_redis.pipelines.RedisPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'tianya_spider.middlewares.statusCodeMiddleware': 120,
            'tianya_spider.middlewares.ProxyMiddleware': 543,
        },
        # scrapy-redis
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
        'REDIS_HOST': config.REDIS_HOST,
        'REDIS_PORT': config.REDIS_PORT
    }

    def __init__(self):
        super(ReplySpider, self).__init__()
        # self.start_urls = ['http://bbs.tianya.cn/post-free-6029190-2.shtml']
        self.start_urls = get_reply_urls()
        self.logger_ = logging.getLogger('main.debug_replySpider')
        pass

    def parse(self, response):
        # line = get_time() + '\t' + response.url
        # self.logger_.debug(line)

        try:
            url = response.url
            # delete reply_url
            depth = response.meta['depth']
            # input(depth)
            if depth == 0:
                remove_reply_url(url)

            block_and_pid = get_block_pid_from_post_url(url)
            if block_and_pid:
                block, pid = block_and_pid
            for i, alt_item in enumerate(response.xpath("//div[@class='atl-item']")):
                floor = alt_item.xpath("./@id").extract_first()
                # f_host = alt_item.xpath("./@_host").extract_first()
                uid = alt_item.xpath("./@_hostid").extract_first()
                name = alt_item.xpath("./@_host").extract_first()
                rid = alt_item.xpath("./@replyid").extract_first()
                time = alt_item.xpath("./@js_restime").extract_first()
                content = alt_item.xpath("./div[2]/div[2]/div/text()").extract_first().strip()

                item = ReplyItem()
                item['floor'] = int(floor)
                item['pid'] = pid
                item['block'] = block
                item['uid'] = uid
                item['name'] = name
                item['rid'] = rid
                item['time'] = time
                item['content'] = content
                yield item
            next_page = response.xpath("//a[@class='js-keyboard-next']/@href").extract_first()
            if next_page:
                url = 'http://bbs.tianya.cn' + next_page
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

        except Exception as e:
            line = get_time() + '\t' + 'replySpider' + '\t' + response.url + '\t' + type(e) + '\t' + str(e)
            self.logger_.debug(line)
