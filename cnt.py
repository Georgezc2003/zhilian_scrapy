# -*- coding: utf-8 -*-
# @Time    : 2017/7/7 10:35
# @Author  : Sunyan Gu
# @File    : cnt.py
# @Software: PyCharm Community Edition
# @function:

import pymongo

client = pymongo.MongoClient('localhost', 27017)
zhilian_test2 = client['zhilian_test3']
zhilian_step_1 = zhilian_test2['zhilian_step_1']
print(zhilian_step_1.count())
zhilian_qingfeng = client['zhilian_qingfeng']

# 前一天不重复的
today_temporary = client['today_temporary']
today_temporary = today_temporary['temporary']
print('临时不重复的%d条数据'%today_temporary.count())


# 当天爬取的数据
zhilian_temporary_data = client['zhilian_temporary_data']
temporary_data = zhilian_temporary_data['temporary_data']
print('当天爬取一共%d条数据'%temporary_data.count())


# 3000表的数据
job_name_tables = client['zhilian_job_name_tables']
cnt = 0
for i in job_name_tables.collection_names():
    cnt += job_name_tables[i].count()
    # if (job_name_tables[i].count()) >= 2999:
    #     print('%s表有%d条数据' % (i, (job_name_tables[i].count())))

        # for item in job_name_tables[i].find():
        #     zhilian_qingfeng[i].insert(item)
        # print('---%s表有%d条数据' % (i, (zhilian_qingfeng[i].count())))

    print('%s表有%d条数据' % (i, (job_name_tables[i].count())))
print('3000表一共有%d条数据'%cnt)


# 总表的数据
zhilian_data_tables = client['zhilian_data']
cnt = 0
for i in zhilian_data_tables.collection_names():
    cnt += zhilian_data_tables[i].count()
print('总表一共有%d条数据'%cnt)








# # 智联招聘预处理所需要的数据
# zhilian_temporary_data = client['zhilian_all_data']
# temporary_data = zhilian_temporary_data['zhilian_data']
# print(temporary_data.count())
# print('预处理有%d条数据'%temporary_data.count())



