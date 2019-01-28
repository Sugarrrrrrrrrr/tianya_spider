# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from tianya_spider.items import UserItem
from utils import get_user_urls
from utils import get_time
import config


class UserSpider(RedisSpider):
    name = 'userSpider'
    allowed_domains = ['tianya.cn']
    start_urls = ['http://www.tianya.cn/102020474']

    custom_settings = {
        'CONCURRENT_REQUESTS': 1024,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 512,
        'CONCURRENT_REQUESTS_PER_IP': 256,
        'DOWNLOAD_TIMEOUT': 30,
        'LOG_LEVEL': config.LOG_LEVEL,
        'DOWNLOADER_MIDDLEWARES': {
            'tianya_spider.middlewares.ProcessAllExceptionMiddleware': 120,
            'tianya_spider.middlewares.ProxyMiddleware': 543,
        },
        'ITEM_PIPELINES': {
            'tianya_spider.pipelines.UserSpiderPipeline': 543,
            # Store scraped item in redis for post-processing.
            # 'scrapy_redis.pipelines.RedisPipeline': 300,
        },
        # scrapy-redis
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
        'REDIS_HOST': config.REDIS_HOST,
        'REDIS_PORT': config.REDIS_PORT
    }

    def __init__(self):
        super(UserSpider, self).__init__()
        self.start_urls = get_user_urls()
        pass

    def parse(self, response):
        with open('data/user.txt', 'a') as f:
            line = get_time() + '\t' + response.url + '\n'
            f.write(line)

        try:
            name = response.xpath("//div[@class='left-area']//h2/a[1]/text()").extract_first()
            gender_str = response.xpath("//div[@class='left-area']//h2/a[2]/@class").extract_first()
            if gender_str.startswith('male'):
                gender = 'male'
            elif gender_str.startswith('female'):
                gender = 'female'
            elif gender_str.startswith('offline pngfix'):
                gender = 'unknown'
            elif gender_str.startswith('pngfix'):
                gender = 'unknown'
            else:
                with open('log/debug_gender_str.txt', 'a') as f:
                    f.write(gender_str + '\t' + response.url + '\n')
                    f.flush()

            uid = response.xpath("//div[@class='left-area']//h2/a[3]/@_data").extract_first()
            follow = response.xpath("//div[@class='relate-link']/div/p/a/text()").extract_first()
            fans = response.xpath("//div[@class='relate-link']/div[2]/p/a/text()").extract_first()
            score = response.xpath("//p[@class='u_tyf']/em/text()").extract_first()     # don't work
            date = response.xpath("//div[@class='userinfo']/p[2]/text()").extract_first()

            location = None
            birthday = None
            note = None
            career_category = None
            career = None
            tags = None
            school = None

            lis = response.xpath("//div[@class='left-area']/div[2]//ul/li")
            for li in lis:
                c = li.xpath("./i/@class").extract_first()
                if c == 'user-location':
                    location = li.xpath("./text()").extract_first()
                elif c == 'user-bir':
                    birthday = li.xpath("./text()").extract_first()
                elif c == 'career-category':
                    career_category = li.xpath("./text()").extract_first()
                elif c == 'user-career':
                    career = li.xpath("./text()").extract_first()
                elif c == 'user-note':
                    note = li.xpath("./text()").extract_first()
                elif c == 'user-tags':
                    tags = li.xpath("./text()").extract_first()
                elif c == 'user-school':
                    school = li.xpath("./text()").extract_first()
                else:
                    with open('log/debug_base_info.txt', 'a') as f:
                        f.write(c + '\t' + response.url + '\n')
                        f.flush()

            item = UserItem()
            item['uid'] = uid
            item['name'] = name
            item['gender'] = gender
            item['follow'] = follow
            item['fans'] = fans
            item['score'] = score
            item['date'] = date

            if location:
                item['location'] = location.strip()
            if birthday:
                item['birthday'] = birthday.strip()
            if note:
                item['note'] = note.strip()
            if career_category:
                item['career_category'] = career_category.strip()
            if career:
                item['career'] = career.strip()
            if tags:
                item['tags'] = tags.strip()
            if school:
                item['school'] = school.strip()

            item['url'] = response.url

            yield item
        except Exception as e:
            with open('log/debug_userSpider_exception.txt', 'a') as f:
                f.write(get_time() + '\t' + 'userSpider' + '\t' + response.url + '\t' + str(e) + '\n')
                f.flush()
