import config
from pymongo import MongoClient, ASCENDING
import time
from dateutil import parser


def gen_reply_start_url(block, pid, comment_get):
    page = int(comment_get/100) + 1
    return 'http://bbs.tianya.cn/post-%s-%s-%d.shtml' % (block, pid, page)


def gen_user_url(uid):
    return 'http://www.tianya.cn/%s' % uid


class MongoCtl:
    def __init__(self):
        self.client = MongoClient(host=config.MONGODB_IP, port=config.MONGODB_PORT)
        self.client.admin.authenticate(config.MONGODB_USER, config.MONGODB_PWD)
        self.tianya = self.client.tianya

        # urls queue
        self.block_urls = self.tianya.block_urls
        self.post_urls = self.tianya.post_urls
        self.reply_urls = self.tianya.reply_urls
        self.user_urls = self.tianya.user_urls
        self.other_urls = self.tianya.other_urls

        # data
        self.posts = self.tianya.posts
        self.replys = self.tianya.replys
        self.users = self.tianya.users

        # config
        self.config = self.tianya.config

    def add_new_block_url(self, url):
        if self.block_urls.find_one({'url': url}):
            return False
        else:
            data = {
                'url': url,
                'status': config.STATUS_OUTSTANDING
            }
            self.block_urls.update(
                {'url': url},
                data,
                upsert=True
            )
            return True

    def add_new_post_url(self, url):
        if self.post_urls.find_one({'url': url}):
            return False
        else:
            data = {
                'url': url,
                'status': config.STATUS_OUTSTANDING
            }
            self.post_urls.update(
                {'url': url},
                data,
                upsert=True
            )
            return True

    def add_new_other_url(self, url):
        if self.other_urls.find_one({'url': url}):
            return False
        else:
            data = {
                'url': url,
                'status': config.STATUS_OUTSTANDING
            }
            self.other_urls.update(
                {'url': url},
                data,
                upsert=True
            )
            return True

    def add_new_user_url(self, uid, name):
        if self.users.find_one({'uid': uid}):
            return False
        else:
            self.add_new_user(
                {
                    'uid': uid,
                    'name': name
                })

            # add_new_user_url
            # to be rewrite
            if False:
                data = {
                    'uid': uid,
                    'url': gen_user_url(uid),
                    'status': config.STATUS_OUTSTANDING
                }
                self.user_urls.update(
                    {'uid': uid},
                    data,
                    upsert=True
                )
            return True

    def remove_post_url(self, url):
        self.post_urls.remove({'url': url})

    def remove_user_url(self, url):
        self.user_urls.remove({'url': url})

    def remove_reply_url(self, url):
        result = self.reply_urls.remove({'url': url})
        if result['ok'] == 1:
            if result['n'] == 1:
                return True
            elif result['n'] == 0:
                return False
        return False

    def add_new_post_and_reply_url(self, data):
        block = data['block']
        pid = data['pid']
        record = self.posts.find_one({
            'block': block,
            'pid': pid
        })
        if record:
            reply_get = record['reply_get']
            data['reply_get'] = reply_get
        else:
            reply_get = 0
            data['reply_get'] = 0

        # add new post
        self.posts.update(
            {
                'block': block,
                'pid': pid
            },
            data,
            upsert=True
        )
        # add new reply url
        if reply_get < data['reply']:
            self.reply_urls.update(
                {
                    'block': block,
                    'pid': pid
                },
                {
                    'block': block,
                    'pid': pid,
                    'url': gen_reply_start_url(block, pid, reply_get),
                    'status': config.STATUS_OUTSTANDING
                },
                upsert=True
            )

    def add_new_user(self, data):
        uid = data['uid']
        data['update'] = time.time()
        self.users.update(
            {'uid': uid},
            {'$set': data},
            upsert=True
        )

    def add_new_reply_and_update_reply_get(self, data):
        block = data['block']
        pid = data['pid']
        rid = data['rid']
        floor = data['floor']
        record = self.replys.find_one({
            'block': block,
            'pid': pid,
            'rid': rid
        })
        if record:
            pass
        else:
            # add new reply
            try:
                data['myTime'] = parser.parse(data['time'])
            except Exception as e:
                pass

            self.replys.update(
                {
                    'block': block,
                    'pid': pid,
                    'rid': rid
                },
                data,
                upsert=True
            )
            # update comment
            post_record = self.posts.find_one({
                'block': block,
                'pid': pid
            })
            if post_record:
                reply_get = post_record['reply_get']
                if floor > reply_get:
                    self.posts.update_one(
                        {
                            'block': block,
                            'pid': pid
                        },
                        {
                            '$set': {
                                'reply_get': floor
                            }
                        }
                    )

    def get_block_urls(self):
        urls = list()
        data = self.block_urls.find()
        for record in data:
            url = record['url']
            urls.append(url)
        return urls

    def get_post_urls(self, n):
        urls = list()
        data = self.post_urls.find().limit(n)
        for record in data:
            url = record['url']
            urls.append(url)
        return urls

    def get_user_urls(self, n):
        urls = list()
        data = self.users.find(
            sort=[('update', ASCENDING)]
        ).limit(n)
        for record in data:
            uid = record['uid']
            self.users.update(
                {'uid': uid},
                {'$set': {'update': time.time()}}
            )
            url = gen_user_url(uid)
            urls.append(url)
        return urls

    def get_reply_urls(self, n):
        urls = list()
        data = self.reply_urls.find().limit(n)
        for record in data:
            url = record['url']
            urls.append(url)
        return urls


if __name__ == '__main__':
    mongoctl = MongoCtl()
    # url = "http://bbs.tianya.cn/post-free-5922783-1.shtml"
    url = "http://bbs.tianya.cn/post-worldlook-1876813-11.shtml"

    print(url)
    pass



