import pandas as pd
from datetime import datetime
from datetime import timedelta
import pymongo
from zhilianzhaopingstep1.first_configure import FirstConfigure
import re
# now = datetime.now()
# now_time = now.strftime('%Y-%m-%d')
# print(now)
# print(now_time)
# data_range = pd.date_range(end=now_time,periods=7)
# print(data_range)
# data_range = [i.strftime('%Y-%m-%d') for i in data_range]
#print(data_range)
client = pymongo.MongoClient('localhost', 27017)

#看某一天数量
# job_name_tables = client['zhilian_job_name_tables']
# db = job_name_tables['IT_互联网_通信:java工程师']
#
# results = db.find({ 'time': '2017-09-02'})
# print(results.count())

# 取3000张表
# zhilian_qingfeng = client['zhilian_qingfeng']
# for i in zhilian_qingfeng.collection_names():
#     print(i)
#     i = i.replace(':','[')
#     i = i+']'
#     print(i)

#print(db.find().sort("time",pymongo.DESCENDING))

# 1537(2017-9-2)
# for result in results:
#     print(result)
#print(db.find_one())

# 获取总类别，如{'能源|环保|农业|科研'}
# firstConfigure = FirstConfigure()
# job_dic = firstConfigure.get_job_dic()
# job = job_dic['园艺师']
# print(job)

# debug职位名称和青峰岗位的映射
# f_IT_category_stopword_path = './zhilianzhaopingstep1/IT_category_stopword.txt'
# stop_word_list1 = [word.strip() for word in \
#                    open(f_IT_category_stopword_path, 'r', encoding='utf-8')]
#
# stop_word_list = list(set(stop_word_list1))
#
# class test(object):
#     def __init__(self):
#         pass
#
#     def if_combine(self,job_name, raw_name):
#         sentence1 = set(job_name.split())
#         sentence2 = set(raw_name.split())
#
#         sentence1_len = len(job_name.split())
#         sentence2_len = len(raw_name.split())
#
#         sentence1_char = set(''.join(job_name.split()))
#         sentence2_char = set(''.join(raw_name.split()))
#
#         sentence2_char_len = len(sentence2_char)
#
#         if sentence1_len == 0 or sentence2_len == 0:
#             return False
#         if len(sentence1_char & sentence2_char) <= sentence2_char_len * 0.85:
#             return False
#         if sentence1_len > sentence2_len and len(sentence1 & sentence2) == sentence2_len:
#             return True
#         elif sentence1_len < sentence2_len and len(sentence1 & sentence2) == sentence1_len:
#             return True
#         elif sentence1_len == sentence2_len and len(sentence1 & sentence2) == sentence2_len:
#             return False
#         else:
#             return False
# import jieba
# seg_list = jieba.cut('Android软件工程师'.strip(), cut_all=False)
# job_name_fenci = ' '.join(seg_list)
# job_name_fenci = job_name_fenci.lower()
# job_name = [word for word in job_name_fenci.split() if word not in stop_word_list]
# job_name = ' '.join(job_name)
#
# test = test()
# result = test.if_combine(job_name,'android 工程师')
# print(result)
# result = test.if_combine(job_name,'android')
# print(result)
# result = test.if_combine(job_name,'android 工程师 测试 员 实习生')
# print(result)
# result = test.if_combine(job_name,'android 高级 工程师')
# print(result)
# result = test.if_combine(job_name,'android 实习生')
# print(result)
# result = test.if_combine(job_name,'android 软件 工程师')
# print(result)
# result = test.if_combine(job_name,'android 软件开发 工程师')
# print(result)
# result = test.if_combine(job_name,'android 应用 工程师')
# print(result)


job_name_tables = client['zhilian_job_name_tables']
db = job_name_tables['IT_互联网_通信:java工程师']
# test_0903 = client['test_0903']
# t0903 = test_0903['t0903']
# t0903.ensure_index('company_job_name', unique=True)
# for i in range(1,10):
#     item = db.find_one()
#     try:
#         t0903.insert_one(item)
#     except:
#         print('exiet')
#         pass
#out = db.find_one('job_name'.lower().find('java') == -1)
#out = db.find_one({'job_name':{'$regex':'java','$options': 'i' }},{'job_name':{'$regex':'Java','$options': 'i' }})

#out = db.find({'$or':[{'job_name':{'$regex':'java'}},{'job_name':{'$regex':'Java'}},{'job_name':{'$regex':'JAVA'}}]}).count()


req = '^((?!java).)*$'
req1 = '^((?!Java).)*$'
req2 = '^((?!JAVA).)*$'
out = db.find({'$and':[{'job_name':re.compile(req)},{'job_name':re.compile(req1)},{'job_name':re.compile(req2)}]}).count()
print(out)
out1 = db.find_one({'$and':[{'job_name':re.compile(req)},{'job_name':re.compile(req1)},{'job_name':re.compile(req2)}]})
print(out1)
