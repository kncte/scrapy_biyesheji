# -*- coding: utf-8 -*-
import json
import warnings

import redis
import scrapy
from scrapy.exceptions import ScrapyDeprecationWarning

from biyesheji.items import MovieItem


class MovieSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        global nums  # 在函数外部也声明为全局变量
        nums = 0
        super(MovieSpider, self).__init__(*args, **kwargs)
        self.redis_client = redis.StrictRedis(host='121.196.205.18', port=6379, db=0, password=123456)
        try:
            self.redis_client.ping()
            self.redis_client.set('state', 'False')
            print('Connected to Redis')
        except Exception as e:
            print(f'Failed to connect to Redis: {str(e)}')

    warnings.filterwarnings("ignore", category=ScrapyDeprecationWarning)

    custom_settings = {
        'ITEM_PIPELINES': {'biyesheji.pipelines.MoviePipeline': 300},

    }
    name = 'movie'
    allowed_domains = ['scrape.center']
    base_url = 'https://ssr1.scrape.center/page/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    start_page = 1
    max_pages = 2

    def start_requests(self):
        for page in range(self.start_page, self.start_page + self.max_pages):
            url = f'{self.base_url}{page}'
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def set_key_with_ttl(self, key, value, ttl_seconds):
        # 设置键值对
        self.redis_client.lpush(key, value)
        # 设置键的过期时间
        self.redis_client.expire(key, ttl_seconds)

    def parse(self, response):
        global nums
        selector = scrapy.Selector(response=response)
        parent_divs = selector.xpath("//*[@id='index']/div[1]/div[1]/div")
        urls = 'https://ssr1.scrape.center'
        for div in parent_divs:
            item = MovieItem()

            title = div.xpath("./div/div/div[2]/a/h2/text()").extract_first()
            rating = div.xpath("./div/div/div[3]/p[1]/text()").extract_first()
            country = div.xpath("./div/div/div[2]/div[2]/span[1]/text()").extract_first()
            address = urls + div.xpath("./div/div/div[2]/a/@href").extract_first()

            item['title'] = title.strip() if title else None
            item['rating'] = rating.strip() if rating else None
            item['country'] = country.strip() if country else None
            item['address'] = address.strip() if address else None
            data_json = json.dumps(dict(item), ensure_ascii=False)
            # sio.emit('crawl_data', data_json, namespace='/crawl')
            # asyncio.create_task(self.process_data(data_json))
            # sio.emit('crawl_data', data_json, namespace='/crawl')
            nums = nums + 1
            print("nums", nums)
            data = {'num': f"正在写入第{nums}条数据  "}
            data2 = json.dumps(dict(data), ensure_ascii=False)
            self.redis_client.lpush('movie_data_list', data2)
            self.redis_client.lpush('movie_data_list', data_json)
            yield item
            if self.redis_client.get('state') == b'True':
                self.log("Stopping spider due to state=True in Redis")
                self.crawler.engine.close_spider(self, 'crawling_finished')

    def closed(self, reason):

        if reason == 'finished':
            self.logger.info('线程已结束')

        elif reason == 'canceled':
            self.logger.info('Spider已手动取消 ')
        else:
            self.logger.info(f'出问题了 : {reason}')
