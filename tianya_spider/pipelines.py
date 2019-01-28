# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from utils import add_post_url
from utils import add_user_url
from utils import add_other_url
from utils import add_post_and_reply_url
from utils import add_reply_and_update_comment
from utils import add_user
from utils import remove_user_url
from utils import remove_post_url
from utils import check_url_type


class ListSpiderPipeline(object):
    def __init__(self):
        # self.file = open('data/list.txt', 'w')
        pass

    def process_item(self, item, spider):
        # content = item['post_href'] + '\n'
        # self.file.write(content)

        url = "http://bbs.tianya.cn" + item['post_href']
        url_type = check_url_type(url)
        if url_type:
            add_post_url(url)
        else:
            add_other_url(url)

        return item

    def close_spider(self, spider):
        # self.file.close()
        pass


class PostSpiderPipeline(object):
    def __init__(self):
        # self.file = open('data/post.txt', 'w', encoding='utf-8')
        pass

    def process_item(self, item, spider):
        # content = "%s\t%s\t%s\t%s\t%s\t%s\t%d\t%d\t%d\n" % (item['title'], item['pid'], item['block'], item['uid'], item['time'], '##content##', item['click'], item['reply'], item['comment'])
        # self.file.write(content)

        data = dict(item)
        add_post_and_reply_url(data)
        remove_post_url(data['url'])

        add_user_url(data['uid'], data['name'])

        return item

    def close_spider(self, spider):
        # self.file.close()
        pass


class UserSpiderPipeline(object):
    def __init__(self):
        # self.file = open('data/user.txt', 'w', encoding='utf-8')
        pass

    def process_item(self, item, spider):
        # content = "%s\t%s\n" % (item['uid'], item['name'])
        # self.file.write(content)
        # self.file.flush()

        data = dict(item)
        add_user(data)
        remove_user_url(data['url'])

        return item

    def close_spider(self, spider):
        # self.file.close()
        pass


class ReplySpiderPipeline(object):
    def __init__(self):
        # self.file = open('data/reply.txt', 'w', encoding='utf-8')
        pass

    def process_item(self, item, spider):
        # content = "%s\t%s\t%d\t%s\t%s\t%s\t%s\n" % (item['block'], item['pid'], item['floor'], item['uid'], item['rid'], item['time'], item['content'])
        # self.file.write(content)

        data = dict(item)
        add_reply_and_update_comment(data)

        add_user_url(data['uid'], data['name'])

        return item

    def close_spider(self, spider):
        # self.file.close()
        pass