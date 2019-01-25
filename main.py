from scrapy.crawler import CrawlerProcess
from tianya_spider.spiders.listSpider import ListSpider
from tianya_spider.spiders.postSpider import PostSpider
from tianya_spider.spiders.replySpider import ReplySpider
from tianya_spider.spiders.userSpider import UserSpider


if __name__ == '__main__':
    process = CrawlerProcess()
    # process.crawl(ListSpider)
    # process.crawl(PostSpider)
    # process.crawl(ReplySpider)
    process.crawl(UserSpider)
    process.start()
