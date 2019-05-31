# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from utils import remove_reply_url
from utils import remove_post_url
from utils import remove_user_url
from utils import get_time
import logging


class TianyaSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TianyaSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        if spider.name in ['userSpider']:
            request.meta['proxy'] = 'http://10.168.103.145:3128'
        elif spider.name in ['listSpider', 'postSpider', 'replySpider']:
            # request.meta['proxy'] = 'http://10.168.103.145:8888'
            pass


class statusCodeMiddleware(object):
    ALL_EXCEPTIONS = ()

    def __init__(self):
        super(statusCodeMiddleware, self).__init__()
        self.logger_ = logging.getLogger('main.statusCodeMiddleware')

    def process_response(self, request, response, spider):
        if response.status in (200, ):
            return response

        if response.status in (404, 301, 500):
            if spider.name == 'replySpider':
                remove_reply_url(response.url)
            elif spider.name == 'postSpider':
                remove_post_url(response.url)
            elif spider.name == 'userSpider':
                remove_user_url(response.url)
            else:
                line = get_time() + '\t' + 'ProcessAllExceptionMiddleware' + '\t' + str(response.status) + '\t' \
                       + spider.name + '\t' + response.url
                self.logger_.debug(line)
        else:
            line = get_time() + '\t' + 'ProcessAllExceptionMiddleware' + '\t' + str(response.status) + '\t' \
                   + spider.name + '\t' + response.url
            self.logger_.debug(line)

        return response

    def process_exception(self, request, exception, spider):
        line = get_time() + '\t' + 'ProcessAllExceptionMiddleware' + '\t' + spider.name + '\t' + str(exception) \
               + '\t' + request.url
        self.logger_.debug(line)