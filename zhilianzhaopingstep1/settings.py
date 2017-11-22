# -*- coding: utf-8 -*-

# Scrapy settings for zhilianzhaopingstep1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhilianzhaopingstep1'

SPIDER_MODULES = ['zhilianzhaopingstep1.spiders']
NEWSPIDER_MODULE = 'zhilianzhaopingstep1.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhilianzhaopingstep1 (+http://www.yourdomain.com)'

ITEM_PIPELINES = {'zhilianzhaopingstep1.pipelines.Zhilianzhaopingstep1Pipeline':400,
                  # 'scrapy_redis.pipelines.RedisPipeline': 500
                  }

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

COOKIES_ENABLED = True
CONCURRENT_REQUESTS = 16
#REDIRECT_ENABLED = False

#SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# DUPEFILTER_CLASS = 'zhilianzhaopingstep1.custom_filters.CustomURLFilter'
DUPEFILTER_CLASS = 'zhilianzhaopingstep1.dupefilters1.RFPDupeFilter'
# 按照 URL 进行查重(文件功能已写，扔有重复)
#DUPEFILTER_CLASS = 'scrapy.dupefilters1.RFPDupeFilter'
# 按照默认过滤器进行查重
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'zhilian_temporary_data'
MONGODB_DOCNAME = 'temporary_data_temptemp'
