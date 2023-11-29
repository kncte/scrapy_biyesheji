# -*- coding: utf-8 -*-
import json
import warnings

import redis
import scrapy
from scrapy import signals
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy_redis.spiders import RedisSpider
from biyesheji.items import MovieItem


class MovieSpider(RedisSpider):
    def __init__(self, *args, **kwargs):
        global nums  # 在函数外部也声明为全局变量
        nums = 0
        super(MovieSpider, self).__init__(*args, **kwargs)
        self.redis_client = redis.StrictRedis(host='8.134.56.160', port=6379, db=0, password=123456)
        self.queue_key = 'movie_key:start_urls'
        # try:
        #     self.redis_client.ping()
        #     self.redis_client.set('state', 'False')
        #     print('Connected to Redis')
        # except Exception as e:
        #     print(f'Failed to connect to Redis: {str(e)}')

    warnings.filterwarnings("ignore", category=ScrapyDeprecationWarning)

    custom_settings = {
        'ITEM_PIPELINES': {'biyesheji.pipelines.MoviePipeline': 300},
    }
    name = 'movie'
    redis_key = 'movie_key:start_urls'

    # allowed_domains = ['scrape.center']
    # base_url = 'https://ssr1.scrape.center/page/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    start_page = 1
    max_pages = 2

    # def spider_idle(self, spider):
    #     # 当爬虫空闲时，检查队列是否为空
    #     queue_length = self.redis_conn.llen(self.queue_key)
    #     if queue_length == 0:
    #         self.crawler.engine.close_spider(spider, 'Queue empty. Job completed.')

    # def start_requests(self):
    #     for page in range(self.start_page, self.start_page + self.max_pages):
    #         url = f'{self.base_url}{page}'
    #         yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def set_key_with_ttl(self, key, value, ttl_seconds):
        # 设置键值对
        self.redis_client.lpush(key, value)
        # 设置键的过期时间
        self.redis_client.expire(key, ttl_seconds)

    def parse(self, response):
        selector = scrapy.Selector(response=response)
        parent_divs = selector.xpath("//*[@id='index']/div[1]/div[1]/div")
        urls = 'https://ssr1.scrape.center'
        for div in parent_divs:
            item = MovieItem()

            title = div.xpath("./div/div/div[2]/a/h2/text()").extract_first()
            rating = div.xpath("./div/div/div[3]/p[1]/text()").extract_first()
            country = div.xpath("./div/div/div[2]/div[2]/span[1]/text()").extract_first()
            address = urls + div.xpath("./div/div/div[2]/a/@href").extract_first()
            type = div.xpath("./div/div[2]/div[1]/button[1]/span/text()").extract_first()
            duration = div.xpath("./div/div/div[2]/div[2]/span[3]/text()").extract_first()

            item['title'] = title.strip() if title else None
            item['rating'] = rating.strip() if rating else None
            item['country'] = country.strip() if country else None
            item['address'] = address.strip() if address else None
            item['type'] = type.strip() if type else None
            item['duration'] = duration.strip() if duration else None

            data_json = json.dumps(dict(item), ensure_ascii=False)

            page = self.redis_client.get('new_page')
            page = page.decode('utf-8')
            data = {'num': f"正在写入第{page}条数据  "}
            page = int(page) + 1
            self.redis_client.set('new_page', str(page))

            data2 = json.dumps(dict(data), ensure_ascii=False)
            self.redis_client.lpush('movie_data_list', data2)
            self.redis_client.lpush('movie_data_list', data_json)
            yield item
            # if self.redis_client.get('state') == b'True':
            #     self.log("Stopping spider due to state=True in Redis")
            #     self.crawler.engine.close_spider(self, 'crawling_finished')




