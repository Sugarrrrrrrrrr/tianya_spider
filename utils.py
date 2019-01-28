import re
import time
from mongoctl import MongoCtl

re_block_pid = None
re_click = None
re_time = None
re_reply_comment = None

re_common_post_url_type = None

mongoctl = MongoCtl()


def check_url_type(url):
    global re_common_post_url_type
    if re_common_post_url_type is None:
        re_common_post_url_type = re.compile(r'http://bbs.tianya.cn/post-[^-]*-[^-]*-[^-]*.shtml')
    rs = re_common_post_url_type.match(url)
    if rs:
        return True
    else:
        return False


def get_block_pid_from_post_url(url):
    global re_block_pid
    if re_block_pid is None:
        re_block_pid = re.compile(r'http://bbs.tianya.cn/post-([^-]*)-([^-]*)-(?:[^-]*).shtml')
    rs = re_block_pid.findall(url)
    if rs:
        return rs[0]


def get_click_for_post(click_str):
    global re_click
    if re_click is None:
        re_click = re.compile(r'点击：(.*)')
    rs = re_click.findall(click_str)
    if rs:
        return int(rs[0])


def get_time_for_post(time_str):
    global re_time
    if re_time is None:
        re_time = re.compile(r'时间：(.*)')
    rs = re_time.findall(time_str)
    if rs:
        return rs[0]


def get_reply_comment_for_post(reply_comment_str):
    global re_reply_comment
    if re_reply_comment is None:
        re_reply_comment = re.compile(r'共(.*)个回帖和(.*)个评论')
    rs = re_reply_comment.findall(reply_comment_str)
    if rs:
        return int(rs[0][0]), int(rs[0][1])


def get_block_urls():
    return mongoctl.get_block_urls()


def add_post_url(url):
    mongoctl.add_new_post_url(url)


def remove_post_url(url):
    mongoctl.remove_post_url(url)


def remove_user_url(url):
    mongoctl.remove_user_url(url)


def remove_reply_url(url):
    mongoctl.remove_reply_url(url)


def get_post_urls(n=10000):
    return mongoctl.get_post_urls(n)


def get_user_urls(n=10000):
    return mongoctl.get_user_urls(n)


def add_post_and_reply_url(data):
    mongoctl.add_new_post_and_reply_url(data)


def get_reply_urls(n=10000):
    return mongoctl.get_reply_urls(n)
    pass


def add_reply_and_update_comment(data):
    mongoctl.add_new_reply_and_update_reply_get(data)


def add_user(data):
    mongoctl.add_new_user(data)


def add_other_url(url):
    mongoctl.add_new_other_url(url)


def add_user_url(uid, name):
    mongoctl.add_new_user_url(uid, name)


def get_time():
    return time.asctime()


if __name__ == '__main__':
    url = 'http://bbs.tianya.cn/post-free-6029190-2.shtml'
    click = '点 击：3130'
    time = '时间：2019-01-11 17:21:46'
    reply_comment = '共128个回帖和351个评论'

    print(get_post_urls())
