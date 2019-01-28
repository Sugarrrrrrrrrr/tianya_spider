import time
from mongoctl import MongoCtl
from utils import get_block_urls
from utils import get_post_urls
from utils import get_reply_urls
from utils import get_user_urls
import redis
import config


def run_list_spider(r):
    block_urls = get_block_urls()
    for url in block_urls:
        r.lpush('listSpider:start_urls', url)


def run_post_spider(r, n):
    post_urls = get_post_urls(n)
    for url in post_urls:
        r.lpush('postSpider:start_urls', url)


def run_reply_spider(r, n):
    reply_urls = get_reply_urls(n)
    for url in reply_urls:
        r.lpush('replySpider:start_urls', url)


def run_user_spider(r, n):
    user_urls = get_user_urls(n)
    for url in user_urls:
        r.lpush('userSpider:start_urls', url)


def run():
    mongoctl = MongoCtl()
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

    while True:
        block_urls_num = mongoctl.block_urls.count()
        post_urls_num = mongoctl.post_urls.count()
        reply_urls_num = mongoctl.reply_urls.count()
        user_urls_num = mongoctl.user_urls.count()

        listSpider_start_urls_num = r.llen('listSpider:start_urls')
        postSpider_start_urls_num = r.llen('postSpider:start_urls')
        replySpider_start_urls_num = r.llen('replySpider:start_urls')
        userSpider_start_urls_num = r.llen('userSpider:start_urls')

        s = '(%d, %d, %d, %d), (%d, %d, %d, %d)' % \
            (block_urls_num, post_urls_num, reply_urls_num, user_urls_num,
             listSpider_start_urls_num, postSpider_start_urls_num,
             replySpider_start_urls_num, userSpider_start_urls_num)

        print(time.asctime()+ '\t' + 'begin' + '\t' + s)

        if user_urls_num != 0:
            if userSpider_start_urls_num == 0:
                print(time.asctime() + '\t' + 'run_user_spider')
                run_user_spider(r, 50)

        if reply_urls_num != 0:
            if replySpider_start_urls_num == 0:
                print(time.asctime() + '\t' + 'run_reply_spider')
                run_reply_spider(r, 1000)
        elif post_urls_num != 0:
            if postSpider_start_urls_num == 0:
                print(time.asctime() + '\t' + 'run_post_spider')
                run_post_spider(r, 1000)
        else:
            if listSpider_start_urls_num == 0:
                print(time.asctime() + '\t' + 'run_list_spider')
                run_list_spider(r)

        # print(time.asctime() + '\t' + 'sleep')
        time.sleep(30)


if __name__ == '__main__':
    run()




