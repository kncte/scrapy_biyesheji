# -*- coding: utf-8 -*-
import json
import redis
import scrapy
from scrapy import FormRequest
from ..items import NewsItem
import re
from bs4 import BeautifulSoup


# 清空表数据 TRUNCATE TABLE table_name;
# TRUNCATE TABLE newdatabase;


class NewSpider(scrapy.Spider):
    redis_key = "news:start_urls"
    custom_settings = {
        'ITEM_PIPELINES': {'biyesheji.pipelines.NewPipeline': 200},
    }
    name = 'news'
    # allowed_domains = ['music']
    base_url = 'https://sou.chinanews.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.140 Safari/537.36',
    }
    start_page = 0  # 起始页数
    max_pages = 10  # 最大页数，根据需求修改

    def __init__(self, key=None, *args, **kwargs):
        super(NewSpider, self).__init__(*args, **kwargs)
        global nums  # 在函数外部也声明为全局变量
        nums = 0
        self.key = key
        self.redis_client = redis.StrictRedis(host='121.196.205.18', port=6379, db=0, password=123456)
        try:
            self.redis_client.ping()
            self.redis_client.set('state', 'False')
            print('Connected to Redis')
        except Exception as e:
            print(f'Failed to connect to Redis: {str(e)}')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(NewSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.crawler = crawler
        return spider

    def start_requests(self):
        print("//////////////", self.key)
        for page in range(self.start_page, self.start_page + self.max_pages):
            page_offset = page * 10
            url = "https://sou.chinanews.com.cn/search.do"
            if page == 0:
                data_text = {
                    "q": self.key
                }
            else:
                data_text = {
                    "q": self.key,
                    "ps": str(page_offset),
                    "start": str(page_offset),
                    "type": "",
                    "sort": "pubtime",
                    "time_scope": "0",
                    "channel": "all",
                    "adv": "1",
                    "day1": "",
                    "day2": "",
                    "field": "",
                    "creator": ""
                }
            print(data_text)

            yield FormRequest(url, method='POST', headers=self.headers, formdata=data_text, callback=self.parse,
                              dont_filter=True)
        # print(data)json.dumps(data)

    def set_key_with_ttl(self, key, value, ttl_seconds):
        # 设置键值对
        self.redis_client.lpush(key, value)
        # 设置键的过期时间
        self.redis_client.expire(key, ttl_seconds)

    def parse(self, response, **kwargs):

        selector = scrapy.Selector(response=response)
        parent_divs = selector.xpath("//*[@id='news_list']/table")
        print("个数---------------------------------", len(parent_divs))
        for div in parent_divs:
            item = NewsItem()
            new_text = div.xpath("./tr[2]/td/ul/li/text()").extract_first()
            if new_text:
                new_text = parse_text(new_text)
                if new_text:
                    urls = new_text[0]
                    time = new_text[1]
                else:
                    urls = None
                    time = None
            else:
                urls = None
                time = None
            self.set_key_with_ttl(self.redis_key, urls.strip() if urls else None, 300)

            # item['title'] = title.strip() if title else None
            # item['content'] = cleaned_text if cleaned_text else None

            item['urls'] = urls.strip() if urls else None
            item['time'] = time.strip() if time else None
            # item['new_from'] = "中国新闻网"
            # print(item)

            yield scrapy.Request(urls, callback=self.sec_parse, meta={'item': item}, headers=self.headers)
            # yield item

    def sec_parse(self, response, **kwargs):
        global nums

        item = response.meta['item']
        selector = scrapy.Selector(response=response)
        new_from = selector.xpath('//*[@id="cont_1_1_2"]/div[2]/div[2]/a/text()').extract_first()
        title = selector.xpath('//*[@id="cont_1_1_2"]/div[2]/h1/text()').extract_first()
        if title is None:
            title = selector.xpath('//*[@id="playerwrap"]/div[1]/div[1]/text()').extract_first()

        xpath_list = [
            '//*[@id="cont_1_1_2"]/div[2]/div[4]/div[2]',
            '//*[@id="playerwrap"]/div[3]/p[1]',
            '//*[@id="cont_1_1_2"]/div[2]/div[4]/div[4]'
        ]
        contents = []

        for xpath in xpath_list:
            content = selector.xpath(xpath).extract_first()
            if content:
                contents.append(content)

        if contents:
            combined_content = '\n'.join(contents)
            soup = BeautifulSoup(combined_content, 'html.parser')
            content = soup.get_text(separator='\n', strip=True)
        else:
            content = None

        print("第一个new_from-----------", new_from)

        if new_from is None:
            new = selector.xpath('//*[@id="playerwrap"]/div[1]/div[2]/p').extract_first()
            if new is None:
                new = selector.xpath('//*[@id="cont_1_1_2"]/div[2]/div[2]/text()').extract_first()
            new_from = re_text(new)
        # 提取有用的文本和换行

        item['content'] = content
        item['title'] = title
        item['new_from'] = new_from

        item_dict = {
            'title': title,
            'content': content,
            'urls': item['urls'],
            'time': item['time'],
            'new_from': new_from
        }
        data_json = json.dumps(item_dict, ensure_ascii=False)
        nums = nums + 1
        data = {'num': f"正在写入第{nums}条数据  "}
        data2 = json.dumps(dict(data), ensure_ascii=False)
        self.redis_client.lpush('new_data_list', data2)
        self.redis_client.lpush('new_data_list', data_json)
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


def parse_text(text):
    text = text.replace("&nbsp;&nbsp;", "")
    pattern = r"(http[^\s]+)\s+([\d-]+\s[\d:]+)"

    matches = re.findall(pattern, text)
    if matches:
        return matches[0]
    else:
        return None


def re_text(text):
    source_pattern = re.compile(r'来源[：:\s]*([^<]+)')

    match = source_pattern.search(text)
    if match:
        source = match.group(1)
        return source.replace('\r\n', '').strip()
    else:
        return None
