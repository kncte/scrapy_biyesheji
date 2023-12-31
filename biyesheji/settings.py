# Scrapy settings for biyesheji project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import signal
from scrapy.signalmanager import dispatcher
from scrapy import signals


# def stop_spider(spider):
#     # 在这里执行停止任务的操作
#     print("Received signal to stop spider")
#     raise SystemExit


# 添加信号处理器
#dispatcher.connect(stop_spider, signal=signals.spider_closed)

BOT_NAME = "biyesheji"

SPIDER_MODULES = ["biyesheji.spiders"]
NEWSPIDER_MODULE = "biyesheji.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "biyesheji (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
#
# REDIS_HOST = '8.134.56.160'
# REDIS_PORT = 6379
# # REDIS_PASSWORD = '123456'
# REDIS_PARAMS = {'password': '123456'}

# # 调度器启用Redis存储Requests队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#
REDIS_URL = 'redis://:123456@8.134.56.160:6379/0'
# # 确保所有的爬虫实例使用Redis进行重复过滤
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#
# # 将Requests队列持久化到Redis，可支持暂停或重启爬虫
SCHEDULER_PERSIST = True
#

DUPEFILTER_DEBUG = True

# # Requests的调度策略，默认优先级队列
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# 将爬取到的items保存到Redis 以便进行后续处理
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 100
}
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }
DOWNLOAD_DELAY = 3  # 固定延迟，单位为秒
RANDOMIZE_DOWNLOAD_DELAY = True  # 开启随机延迟
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "biyesheji.middlewares.BiyeshejiSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "biyesheji.middlewares.BiyeshejiDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html

# WEBSOCKET_SERVER = 'redis://:123456@8.134.56.160:6379/0'


# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "biyesheji.pipelines.MusicPipeline": 200,
#    "biyesheji.pipelines.MoviePipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
