# -*- coding: utf-8 -*-
import scrapy
from tianya_spider.items import PostItem
from utils import get_block_pid_from_post_url
from utils import get_click_for_post
from utils import get_time_for_post
from utils import get_reply_comment_for_post
from utils import get_post_urls


class PostSpider(scrapy.Spider):
    name = 'postSpider'
    allowed_domains = ['tianya.cn']
    start_urls = ['http://bbs.tianya.cn/post-free-6029190-1.shtml']

    custom_settings = {
        'ITEM_PIPELINES': {
            'tianya_spider.pipelines.PostSpiderPipeline': 543,
        }
    }

    def __init__(self):
        super(PostSpider, self).__init__()
        # self.start_urls = ['http://bbs.tianya.cn/post-free-6029190-2.shtml']
        self.start_urls = get_post_urls()
        pass

    def parse(self, response):
        try:
            # bd = response.xpath("//div[@id='bd']").extract_first()
            # post_head = response.xpath("//div[@id='post_head']").extract_first()

            title = response.xpath("//div[@id='post_head']/h1/span/span/text()").extract_first()
            url = response.url
            block_and_pid = get_block_pid_from_post_url(url)
            if block_and_pid:
                block, pid = block_and_pid
            uid = response.xpath("//div[@id='post_head']/div/div[@class='atl-info']/span/a/@uid").extract_first()
            time_str = response.xpath("//div[@id='post_head']/div/div[@class='atl-info']/span[2]/text()").extract_first()
            time = get_time_for_post(time_str)
            # uname = response.xpath("//div[@id='post_head']/div/div[@class='atl-info']/span/a/text()").extract_first()
            reply_and_comment_str = response.xpath("//div[@id='post_head']/div/div[@class='atl-info']/span[4]/@title").extract_first()
            reply, comment = get_reply_comment_for_post(reply_and_comment_str)
            click_str = response.xpath("//div[@id='post_head']/div/div[@class='atl-info']/span[3]/text()").extract_first()
            click = get_click_for_post(click_str)
            # atl_main = response.xpath("//div[@class='atl-main']").extract_first()
            if block == 'me':
                content = response.xpath("//div[@class='bbs-content bbs-me-content clearfix']").xpath('string(.)').extract_first().strip()
            else:
                content = response.xpath("//div[@class='bbs-content clearfix']").xpath('string(.)').extract_first().strip()

            item = PostItem()
            item['title'] = title
            item['pid'] = pid
            item['block'] = block
            item['uid'] = uid
            item['time'] = time
            item['content'] = content
            item['click'] = click
            item['reply'] = reply
            item['comment'] = comment
            item['url'] = url
            yield item
        except Exception as e:
            print("postSpider", type(e), e)
            # print(url)
            # print('----------')
