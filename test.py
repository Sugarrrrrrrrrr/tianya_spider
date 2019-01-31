import re
import time
from mongoctl import MongoCtl
from utils import get_block_urls
from utils import get_post_urls
from utils import get_reply_urls
from utils import get_user_urls
import redis
import config
import requests


if __name__ == '__main__':
    mongoctl = MongoCtl()

    # run_list_spider()
    # run_post_spider()
    # run_reply_spider()
    # run_user_spider(1081)

    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    # r.lpush('listSpider:start_urls', 'http://bbs.tianya.cn/list-free-1.shtml')
    # r.lpush('postSpider:start_urls', 'http://bbs.tianya.cn/post-free-4099410-1.shtml')
    # r.lpush('replySpider:start_urls', 'http://bbs.tianya.cn/post-free-5818726-1.shtml')
    # r.lpush('userSpider:start_urls', 'http://www.tianya.cn/138344770')

    # reply_urls = get_reply_urls()
    # url = reply_urls[0]
    # print(url)
    # r.lpush('replySpider:start_urls', url)

    print(r.llen('listSpider:start_urls'), r.llen('postSpider:start_urls'),
          r.llen('replySpider:start_urls'), r.llen('userSpider:start_urls'))

    block_urls = {
        'http://bbs.tianya.cn/list-funinfo-1.shtml',
        'http://bbs.tianya.cn/list-feeling-1.shtml',
        'http://bbs.tianya.cn/list-1095-1.shtml',
        'http://bbs.tianya.cn/list-develop-1.shtml',
        'http://bbs.tianya.cn/list-worldlook-1.shtml',
        'http://bbs.tianya.cn/list-free-1.shtml',
        'http://bbs.tianya.cn/list-no05-1.shtml',
        'http://bbs.tianya.cn/list-16-1.shtml',
        'http://bbs.tianya.cn/list-333-1.shtml',
        'http://bbs.tianya.cn/list-934-1.shtml',
    }

    for url in block_urls:
        mongoctl.add_new_block_url(url)



