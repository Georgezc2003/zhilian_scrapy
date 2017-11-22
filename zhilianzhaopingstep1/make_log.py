# -*- coding: utf-8 -*-
"""
   @Author 马能宇
   @Date 2016/11/7 16:59
   @生成抓取信息时的日志并保存
 """
import logging


class MakeLog(object):
    def __init__(self):  # 配置日志信息
        LOGGING_MSG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(lineno)d] %(message)s'
        LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
        logging.basicConfig(level=logging.DEBUG,
                            format=LOGGING_MSG_FORMAT,
                            datefmt=LOGGING_DATE_FORMAT,
                            filename='zhilian_web_page.log',
                            filemode='a')
        # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # 设置日志打印格式
        formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')
        console.setFormatter(formatter)
        # 将定义好的console日志handler添加到root logger
        logging.getLogger('').addHandler(console)
        self.logger = logging.getLogger('zhilian_web_page')

    def log4(self, txt, url):
        self.logger.debug(txt % (url))



