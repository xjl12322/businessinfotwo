# -*- coding: utf-8 -*-

# Scrapy settings for businessinfo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'businessinfotwo'

SPIDER_MODULES = ['businessinfotwo.spiders']
NEWSPIDER_MODULE = 'businessinfotwo.spiders'

# # 1(必须). 使用了scrapy_redis的去重组件，在redis数据库里做去重
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#
#
# # 2(必须). 使用了scrapy_redis的调度器，在redis里分配请求
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#
# # 3(必须). 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复，也就是不清理redis queues
# SCHEDULER_PERSIST = True


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.15 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS =3
DOWNLOAD_DELAY = 1
# 当访问异常时是否进行重试
RETRY_ENABLED = True
# 当遇到以下http状态码时进行重试
# RETRY_HTTP_CODES = [500, 502, 503, 504, 403, 408,429,502]
# 重试次数
# RETRY_TIMES = 3
DOWNLOAD_TIMEOUT=50
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.03
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 1
# CONCURRENT_REQUESTS_PER_IP = 5
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'businessinfo.middlewares.BusinessinfoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'businessinfotwo.middlewares.BusinessinfoDownloaderMiddleware': 543,
    #'businessinfotwo.middlewares.MyUserAgentMiddleware': 1,
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 90,
    'businessinfotwo.middlewares.HttpbinProxyMiddlewares': 80,
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware':50
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
     #'scrapy_redis.pipelines.RedisPipeline': 100,
     'businessinfotwo.pipelines.mysql_yi_pipelines': 302,
     # 'businessinfo.pipelines.redisinsert': 301
#    'businessinfo.pipelines.BusinessinfoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#LOG_FILE = "mySpider.log"



CONRENT_CONF = "line87"
# CONRENT_CONF = "local"
SQLDB = {
    "local":{"MYSQL_HOST": "127.0.0.1",
"MYSQL_DBNAME" : "ecms72",
"MYSQL_PORT" : 3306,
"MYSQL_USER" : "py",
"MYSQL_PASSWD" : "py"},

    "line":{"MYSQL_HOST": "119.10.116.237",
"MYSQL_DBNAME" : "whois",
"MYSQL_PORT" : 3306,
"MYSQL_USER" : "py",
"MYSQL_PASSWD" : "py"},
    "line87":{"MYSQL_HOST": "10.2.2.103",
"MYSQL_DBNAME" : "whois_python",
"MYSQL_PORT" : 3306,
"MYSQL_USER" : "whois_pythonuser",
"MYSQL_PASSWD" : "p6l6agW5FSu9FYzq"},

}
REDISDB = {
    "local":{"REDIS_HOST": "127.0.0.1",
            "REDIS_PORT" : 6379,
            "REDIS_DB":8,
            "REDIS_PASSWORD" : None},

    "line":{"REDIS_HOST": "119.10.116.237",
"REDIS_PORT" : 6379,
"REDIS_DB":2,
"REDIS_PASSWORD" : "xinnet"},

    "line87": {"REDIS_HOST": "10.2.2.87",
               "REDIS_PORT": 6379,
               "REDIS_DB": 6,
               "REDIS_PASSWORD": "xinnet123"},
}

# REDIS_HOST= "127.0.0.1"
# REDIS_PORT = 6379
# REDIS_DB = 1
# REDIS_PASSWORD = None

# REDIS_HOST= "119.10.116.237"
# REDIS_PORT = 6379
# REDIS_DB = 1
# REDIS_PASSWORD = None

#scrapy-redis 指定数据库
# REDIS_URL = 'redis://:xinnet@127.0.0.1:6379'
# REDIS_URL = 'redis://:xinnet123@127.0.0.1:6379'
# REDIS_URL = 'redis://@127.0.0.1:6379'