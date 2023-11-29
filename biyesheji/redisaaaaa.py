import redis
import json

# 连接到 Redis 服务器
redis_host = '8.134.56.160'  # 你的 Redis 服务器地址
redis_port = 6379  # 你的 Redis 服务器端口
redis_db = 0  # Redis 数据库编号
redis_password = '123456'  # Redis 访问密码


class redis_:
    def __init__(self):
        self.redis_host = '8.134.56.160'  # 你的 Redis 服务器地址
        self.redis_port = 6379  # 你的 Redis 服务器端口
        self.redis_db = 0  # Redis 数据库编号
        self.redis_password = '123456'  # Redis 访问密码
        self.redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)

    def movie(self):
        # 创建 Redis 连接对象
        # 定义关键字和 URL 列表
        keywords = ['4', '5', '6']
        base_url = 'https://ssr1.scrape.center/page/'

        # 循环构建要推送的数据结构并推送到 Redis 队列
        queue_name = 'movie_key:start_urls'
        # queue_name = 'news_key:start_urls'

        for keyword in range(1, 10):
            url = f'{base_url}{keyword}'  # 修改这里以构建完整的 URL
            data = {'url': url, 'data': {'keyword': keyword}}
            data_json = json.dumps(data)
            self.redis_conn.lpush(queue_name, data_json)
            print(f'Successfully pushed keyword "{keyword}" to the Redis queue "{queue_name}"')
        return "任务完成投递"

    def news(self, key):
        data = {'url': 'https://sou.chinanews.com.cn/', 'key': key}
        data_json = json.dumps(data)
        self.redis_conn.lpush('news_key:start_urls', data_json)
        return "任务完成投递"

    def music(self, key):
        data = {'url': 'https://complexsearch.kugou.com/', 'key': key}
        data_json = json.dumps(data)
        self.redis_conn.lpush('music_key:start_urls', data_json)
        return "任务完成投递"


if __name__ == '__main__':
    aaa = redis_()
    print(aaa.movie())
