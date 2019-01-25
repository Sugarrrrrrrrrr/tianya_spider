from scrapy.crawler import CrawlerProcess
from tianya_spider.spiders.listSpider import ListSpider
import time
from scrapy import cmdline


def run():
    cmdline.execute('scrapy crawl listSpider'.split())


if __name__ == '__main__':

    for i in range(2):
        print('begin')
        run()
        time.sleep(10)