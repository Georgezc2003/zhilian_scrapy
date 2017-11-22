# -*- coding: utf-8 -*-
# @Time    : 2017/7/29 19:20
# @Author  : Sunyan Gu
# @File    : test.py
# @Software: PyCharm Community Edition
# @function:
from pymongo import MongoClient
import json

client = MongoClient()
db1 = client ['zhilian_temporary_data']
coll1 = db1['temporary_data']  # 英文用 job title 比较好
db2 = client['recruitdb']
coll2 = db2.create_collection('data_10062134')
coll2 = coll1

# with open("d:/data/temporary_data1006.json",'w',encoding='utf-8') as json_file:
#          json.dump(coll1,json_file,ensure_ascii=False)

# import pandas as pd
# from datetime import datetime
# from datetime import timedelta
#
# now = datetime.now()
# now_time = now.strftime('%Y-%m-%d')
#
# data_range = pd.date_range(end=now_time,periods=7)
# data_range = [i.strftime('%Y-%m-%d') for i in data_range]
# print(data_range)



