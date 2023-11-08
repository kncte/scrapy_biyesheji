# -*- coding: utf-8 -*-
import hashlib
import json
import re
import time

import redis
import requests
import scrapy
from scrapy import FormRequest

from ..items import MusicItem


# class MusicSpider(scrapy.Spider):
class MusicSpider(scrapy.Spider):
    name = 'music'
    redis_key = 'music:start_keys'
    custom_settings = {
        'ITEM_PIPELINES': {'biyesheji.pipelines.MusicPipeline': 300},
    }

    # allowed_domains = ['music']
    base_url = 'kugou.com'

    def __init__(self, key=None, *args, **kwargs):
        super(MusicSpider, self).__init__(*args, **kwargs)
        # 初始化 Redis 客户端连接

        self.key = key
        if self.key is None:
            self.key = '邓紫棋'
        self.redis_client = redis.StrictRedis(host='121.196.205.18', port=6379, db=0, password=123456)
        try:
            self.redis_client.ping()
            self.redis_client.set('state', 'False')
            print('Connected to Redis')
        except Exception as e:
            print(f'Failed to connect to Redis: {str(e)}')

    def start_requests(self):
        keyword = self.key

        print("//////////////", self.key)
        date = int(time.time() * 1000)
        url = 'https://complexsearch.kugou.com/v2/search/song'
        signature = md5_hash(date=date, word=keyword)
        headers = {
            'Referer': 'https://www.kugou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
        link_data = {
            'callback': 'callback123',
            'srcappid': '2919',
            'clientver': '1000',
            'clienttime': str(date),
            'mid': '6cff5eec372eb97a1152cedd1d7c9fd5',
            'uuid': '6cff5eec372eb97a1152cedd1d7c9fd5',
            'dfid': '2UHYNz3g5BlC1P5mfH2586l5',
            'keyword': str(keyword),
            'page': '1',
            'pagesize': '30',
            'bitrate': '0',
            'isfuzzy': '0',
            'inputtype': '0',
            'platform': 'WebFilter',
            'userid': '458167322',
            'iscorrection': '1',
            'privilege_filter': '0',
            'filter': '10',
            'token': '84444db71f298ea679c54e933acfdbe5065b7e0dd17b6bd7c2384cccde1f45c0',
            'appid': '1014',
            'signature': str(signature),
        }
        yield FormRequest(url=url, formdata=link_data, callback=self.parse, headers=headers, method='Get')

    def set_key_with_ttl(self, key, value, ttl_seconds):
        # 设置键值对
        self.redis_client.lpush(key, value)
        # 设置键的过期时间
        self.redis_client.expire(key, ttl_seconds)

    def parse(self, response, **kwargs):
        print("*************", response.text)
        html_data = re.findall('callback123\((.*)', response.text)[0].replace(')', '')
        item = MusicItem()
        try:
            json_data = json.loads(html_data)
            for index in json_data['data']['lists']:

                item['name'] = index['SongName']
                item['singer'] = index['SingerName']
                item['Album_Name'] = index['AlbumName']
                item['music_id'] = index['EMixSongID']
                item['Album_pic'] = index['AlbumImage'].replace('{size}/', '')
                time.sleep(2)
                item['mp3_url'] = save(index['EMixSongID'])
                item_dict = {
                    'name': item['name'],
                    'singer': item['singer'],
                    'Album_Name': item['Album_Name'],
                    'music_id': item['music_id'],
                    'Album_pic': item['Album_pic'],
                    'mp3_url': item['mp3_url'],
                }
                self.set_key_with_ttl(self.redis_key, item['name'].strip() if item['name'] else None, 300)
                data_json = json.dumps(item_dict, ensure_ascii=False)
                page = self.redis_client.get('new_page')
                page = page.decode('utf-8')
                data = {'num': f"正在写入第{page}条数据  "}
                page = int(page) + 1
                self.redis_client.set('new_page', str(page))
                data2 = json.dumps(dict(data), ensure_ascii=False)
                self.redis_client.lpush('music_data_list', data2)
                self.redis_client.lpush('music_data_list', data_json)
                print(item)
                yield item
                if self.redis_client.get('state') == b'True':
                    print("已结束")
                    self.log("Stopping spider due to state=True in Redis")
                    self.crawler.engine.close_spider(self, 'crawling_finished')
                time.sleep(1)
        except json.JSONDecodeError as e:
            self.logger.error("JSON decoding error: %s", str(e))

    def closed(self, reason):

        if reason == 'finished':
            self.logger.info('线程已结束')

        elif reason == 'canceled':
            self.logger.info('Spider已手动取消 ')
        else:
            self.logger.info(f'出问题了 : {reason}')


def md5_hash(date, word):
    text = [
        'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt',
        'appid=1014',
        'bitrate=0',
        'callback=callback123',
        f'clienttime={date}',
        'clientver=1000',
        'dfid=2UHYNz3g5BlC1P5mfH2586l5',
        'filter=10',
        'inputtype=0',
        'iscorrection=1',
        'isfuzzy=0',
        f'keyword={word}',
        'mid=6cff5eec372eb97a1152cedd1d7c9fd5',
        'page=1',
        'pagesize=30',
        'platform=WebFilter',
        'privilege_filter=0',
        'srcappid=2919',
        'token=84444db71f298ea679c54e933acfdbe5065b7e0dd17b6bd7c2384cccde1f45c0',
        'userid=458167322',
        'uuid=6cff5eec372eb97a1152cedd1d7c9fd5',
        'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt'
    ]
    string = ''.join(text)
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    signature = md5.hexdigest()
    print(signature)
    return signature


def save(music_id):
    # 请求链接, 数据包链接地址
    url = 'https://wwwapi.kugou.com/yy/index.php'
    headers = {
        'Referer': 'https://www.kugou.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    # 请求参数 -> 使用data字典接收请求参数
    data = {
        'r': 'play/getdata',
        # 'callback': 'jQuery1910438191389285846_1693915941407',
        'dfid': '2UHYNz3g5BlC1P5mfH2586l5',
        'appid': '1014',
        'mid': '6cff5eec372eb97a1152cedd1d7c9fd5',
        'platid': '4',
        'encode_album_audio_id': music_id,
        '_': '1693915941408',
    }
    response = requests.get(url=url, params=data, headers=headers)

    play_url = response.json()['data']['play_url']
    # 对于音频链接发送请求, 获取二进制数据

    return play_url
