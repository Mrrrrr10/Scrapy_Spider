# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_Spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_Spider'

SPIDER_MODULES = ['Scrapy_Spider.spiders']
NEWSPIDER_MODULE = 'Scrapy_Spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Scrapy_Project (+http://www.yourdomain.com)'


# 是否遵守机器人协议
ROBOTSTXT_OBEY = False  # # False:不会过滤任何页面


# 配置Scrapy执行的最大并发请求（默认值：16）
# CONCURRENT_REQUESTS = 32


# ------ 下载延迟设置 ------
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# ------ 是否启用cookie,默认为不启用 ------
# COOKIES_ENABLED = False


# ------ 禁用Telnet控制台（默认启用） ------
# TELNETCONSOLE_ENABLED = False


# ------ 可在特定的爬虫spider文件设置 ------
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }


# ---------- Middleware ----------
# 启用或者禁用 spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Scrapy_Spider.middlewares.ScrapyProjectSpiderMiddleware': 543,
# }

# 启用或者禁用 downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'Scrapy_Spider.middlewares.ScrapySpiderDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,     # 禁用scrapy原有的User-Agent
    'Scrapy_Spider.middlewares.RandomUserAgentMiddleware': 300,
    'Scrapy_Spider.middlewares.RandomProxyMiddleware': 554,        # Proxy Pool
    # 'Scrapy_Spider.middlewares.JSPageMiddleware': 230,
}

RANDOM_UA_TYPE = "random"                           # todo:既可以选择浏览器又可以随机切换
HTTP_PROXY = 'http://127.0.0.1:8123'                # Tor
PROXY_POOL_URL = 'http://localhost:5555/random'     # Proxy Pool

# -------------------------------------------------
# 启用或者禁用扩展
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#    'scrapy.extensions.closespider.CloseSpider': 500
# }
# CLOSESPIDER_TIMEOUT = 84600   # 爬虫运行超过23.5小时，如果爬虫还没有结束，则自动关闭


# 配置pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Scrapy_Spider.pipelines.TimePipeline': 300,
    'Scrapy_Spider.pipelines.MongoPipeline': 301,
}

# MongoDB数据库配置
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DBNAME = 'Spider'

# Redis
REDIS_URL = "redis://root:@127.0.0.1:6379"
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# MySQL数据库配置
MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "spider"
MYSQL_USER = "your_username"
MYSQL_PASSWORD = "your_password"

# SQL相关
SQL_DATE_FORMAT = "%Y-%m-%d"
SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# 时间处理
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
GMT_FORMAT = "%a %b %d %H:%M:%S +0800 %Y"

RETRY_HTTP_CODES = [401, 403, 407, 408, 414, 429, 500, 502, 503, 504]

# ---------- 自动限速(AutoThrottle)扩展 ----------
# 启用并配置AutoThrottle扩展（默认情况下禁用）
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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


# 启用并配置HTTP缓存（默认情况下禁用）
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# HTTPERROR_ALLOWED_CODES = [429, 403]

