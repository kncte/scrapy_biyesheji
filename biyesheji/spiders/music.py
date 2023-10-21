# -*- coding: utf-8 -*-
import json
import time

import redis
import scrapy
from scrapy import FormRequest
from ..items import MusicItem
from scrapy_redis.spiders import RedisSpider
import base64
from Crypto.Cipher import AES

from biyesheji.musicsss.dowm_music import Download
# class MusicSpider(scrapy.Spider):
class MusicSpider(scrapy.Spider):
    redis_key = 'music:start_keys'
    custom_settings = {
        'ITEM_PIPELINES': {'biyesheji.pipelines.MusicPipeline': 300},
    }
    name = 'music'
    # allowed_domains = ['music']
    base_url = 'https://music.163.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.140 Safari/537.36',
        'Referer': 'https://music.163.com/search/',
        'Origin': 'http://music.163.com',
        'Host': 'music.163.com'
    }

    def __init__(self, key=None, *args, **kwargs):
        super(MusicSpider, self).__init__(*args, **kwargs)
        # 初始化 Redis 客户端连接
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

    def start_requests(self):
        keyword = self.key
        print("//////////////", self.key)
        data = get_musicc(keyword)
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='


        form_data = {
            "params": data["params"],
            "encSecKey": data["encSecKey"]
        }

        # yield scrapy.Request(url, method='POST', headers=self.headers, body=data, callback=self.parse)
        # yield FormRequest(url, method='POST', headers=self.headers, formdata=form_data, callback=self.parse)
        yield FormRequest(url, method='POST', headers=self.headers, formdata=form_data, callback=self.parse,
                          dont_filter=True)

    def parse(self, response, **kwargs):

        # self.logger.debug("Received response: %s", response.text)
        item = MusicItem()
        # print("-----------------------------", response.text, response)
        global nums
        try:
            json_dict = json.loads(response.text)
            # ...（处理 JSON 数据的代码）
            self.logger.debug("Received JSON response: %s", json_dict)

            for directory_temp in json_dict['result']['songs']:
                item['name'] = directory_temp['name']
                item['music_id'] = directory_temp['id']
                item['singer'] = directory_temp['ar'][0]['name']
                item['Album_Name'] = directory_temp['al']['name']
                item['Album_pic'] = directory_temp['al']['picUrl']
                mp3 = Download(item['music_id'])
                if mp3 == 0:
                    item['mp3_url'] = "空"
                else:
                    item['mp3_url'] = mp3

                item_dict = {
                    'name': item['name'],
                    'music_id': item['music_id'],
                    'singer': item['singer'],
                    'Album_Name': item['Album_Name'],
                    'Album_pic': item['Album_pic'],
                    'mp3_url': item['mp3_url']
                }
                self.redis_client.lpush(self.redis_key, item['music_id'])
                data_json = json.dumps(item_dict, ensure_ascii=False)
                print("------66666666666666666-", item)
                print("----------------", data_json)
                nums = nums + 1
                print("nums", nums)
                data = {'num': f"正在写入第{nums}条数据  "}
                data2 = json.dumps(dict(data), ensure_ascii=False)
                self.redis_client.lpush('music_data_list', data2)
                self.redis_client.lpush('music_data_list', data_json)
                yield item
                if self.redis_client.get('state') == b'True':
                    self.log("Stopping spider due to state=True in Redis")
                    self.crawler.engine.close_spider(self, 'crawling_finished')
                time.sleep(2)
        except json.JSONDecodeError as e:
            self.logger.error("JSON decoding error: %s", str(e))

    def closed(self, reason):

        if reason == 'finished':
            self.logger.info('线程已结束')

        elif reason == 'canceled':
            self.logger.info('Spider已手动取消 ')
        else:
            self.logger.info(f'出问题了 : {reason}')


second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"


def pkcs7padding(text):

    bs = AES.block_size  # 16
    length = len(text)
    bytes_length = len(bytes(text, encoding='utf-8'))
    # tips：utf-8编码时，英文占1个byte，而中文占3个byte
    padding_size = length if (bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
    padding_text = chr(padding) * padding
    return text + padding_text


def aes_en(text, key, iv):
    # print('pkcs7padding处理之前：',text)
    text = pkcs7padding(text)
    # print('pkcs7padding处理之后：',text)
    # entext = text + ('\0' * add)
    # 初始化加密器
    aes = AES.new(key.encode(encoding='utf-8'), AES.MODE_CBC, iv)
    enaes_text = str(base64.b64encode(aes.encrypt(str.encode(text))), encoding='utf-8')
    return enaes_text


def get_params(first_param):
    iv = b"0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'

    h_encText = aes_en(first_param, first_key, iv)
    h_encText = aes_en(h_encText, second_key, iv)
    return h_encText


def get_musicc(name):
    search_name = name
    page = "0"
    if page != 0:
        if_firstPage = "true"  # 如果是第一页(即page=0)则if_firstPage为false，否则都为true
    else:
        if_firstPage = "false"  # page为0，这是评论第一页则if_firstPage为false

    first_param = "{\"hlpretag\":\"<span class=\\\"s-fc7\\\">\",\"hlposttag\":\"</span>\",\"s\":\"%s\",\"type\":\"1\",\"offset\":\"%s\",\"total\":\"%s\",\"limit\":\"30\",\"csrf_token\":\"\"}" % (
        search_name, page, if_firstPage)

    user_data = {
        'params': get_params(first_param),
        'encSecKey': "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    }

    # response = requests.post(Search_api, headers=search_headers, data=user_data)

    # print(response.text)
    # json_dict = json.loads(response.text)

    return user_data

    # for directory_temp in json_dict['result']['songs']:
    #     song_name = directory_temp['name']
    #     song_id = directory_temp['id']
    #
