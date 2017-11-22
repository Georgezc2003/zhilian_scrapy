# -*- coding: utf-8 -*-
# @Time    : 2017/1/7
# @Author  : Sunyan Gu
# @Site    : NJUPT


from scrapy import cmdline

# 数据爬取开始（在url parse结束之后）——进入项目的根目录，执行下列命令启动
# spider:scrapy crawl 项目name，在zhilian_spider.py中定义
# cmdline.execute('scrapy crawl zhilian_step1 -L WARNING -s JOBDIR=Temp/temp1'.split())
# cmdline.execute('scrapy crawl zhilian_step1 -s JOBDIR=crawls/somespider-1'.split())
cmdline.execute('scrapy crawl zhilian_step1 -L WARNING'.split())
#cmdline.execute('scrapy crawl zhilian_step1'.split())










