# -*- coding: utf-8 -*-
# @Time    : 2017/7/23 20:41
# @Author  : Sunyan Gu
# @File    : create_dbs.py
# @Software: PyCharm Community Edition
# @function:
# @debug    :2017/8/5 Chanying Chen

import pymongo
from zhilianzhaopingstep1.first_configure import FirstConfigure
import jieba
import os
import xlrd
import time
from datetime import datetime
from datetime import timedelta
import pandas as pd

class Create_dbs(object):

    def __init__(self):

        # 初始化数据库
        client = pymongo.MongoClient('localhost', 27017)
        zhilian_temporary_data = client['zhilian_temporary_data']
        self.temporary_data = zhilian_temporary_data['temporary_data']

        # 前一天不重复的
        today_temporary = client['today_temporary']
        self.today_temporary = today_temporary['temporary']
        self.today_temporary.remove()
        self.today_temporary.ensure_index('company_job_name',unique=True)
        # 索引

        # 总表，url去重就行
        self.zhilian_data = client['zhilian_data']

        # 3000张表
        self.job_name_tables = client['zhilian_job_name_tables']

        # 七天以内临时存放，数据库名字起得不好，是out...
        week_temporary = client['out_week_temporary']
        self.week_temporary = week_temporary['out_week_temporary']
        self.week_temporary.ensure_index('company_job_name',unique=True)

        # 从之前的config里面提取职位名
        firstConfigure = FirstConfigure()
        self.job_dic = firstConfigure.get_job_dic()

        # 停用词库
        f_IT_category_stopword_path = './zhilianzhaopingstep1/IT_category_stopword.txt'
        stop_word_list1 = [word.strip() for word in \
                           open(f_IT_category_stopword_path, 'r', encoding='utf-8')]

        self.stop_word_list = list(set(stop_word_list1))

        # 从csv中读出已定义的青峰岗位
        self.job_name_dic = self.create_job_name_dic()

        # 生成青峰岗位的3000张数据库表
        zhilian_job_name = []
        for i,j in self.job_name_dic.items():
            total_name = '|'.join(i.strip().split('_'))
            total_name_db = self.zhilian_data[total_name]
            try:
                total_name_db.ensure_index('recruitment_link',unique=True,sparse=True) # 索引，去重
            except:
                pass
            for a,b in j.items():
                zhilian_job_name.append(i + ':' + b)
                if b == '':
                    raise NameError('the name of {} is in {} empty?'.format(a,i))
        for i in set(zhilian_job_name):
            job_title_db = self.job_name_tables[i]
            try:
                job_title_db.ensure_index('recruitment_link',unique=True,sparse=True)
            except:
                pass
        print('The initialization is completed')

    # 判断job_name是否属于raw_name，raw_name是什么？早先定义的？
    def if_combine(self,job_name, raw_name):
        sentence1 = set(job_name.split())
        sentence2 = set(raw_name.split())

        sentence1_len = len(job_name.split())
        sentence2_len = len(raw_name.split())

        sentence1_char = set(''.join(job_name.split()))
        sentence2_char = set(''.join(raw_name.split()))

        sentence2_char_len = len(sentence2_char)

        if sentence1_len == 0 or sentence2_len == 0:
            return False
        if len(sentence1_char & sentence2_char) <= sentence2_char_len * 0.85:
            return False
        if sentence1_len > sentence2_len and len(sentence1 & sentence2) == sentence2_len:
            return True
        elif sentence1_len < sentence2_len and len(sentence1 & sentence2) == sentence1_len:
            return True
        elif sentence1_len == sentence2_len and len(sentence1 & sentence2) == sentence2_len:
            return False
        else:
            return False

    # 计算精确时间， 2017.9.29发现智联招聘日期变了，变成2017-09-28 09:14:09 的形式，这段代码可能不用了，还有时间是0002-01-01 00:00:00 估计是老数据？？
    def cal_real_date(self,time,release_date):
        if release_date == '今天' or release_date == '刚刚' or release_date == '1小时前'\
            or release_date == '1小时前' or release_date == '2小时前' or release_date == '3小时前'\
            or release_date == '4小时前' or release_date == '5小时前':
            return str(datetime.strptime(time, '%Y-%m-%d')).split()[0]
        elif release_date == '昨天':
            return str(datetime.strptime(time, '%Y-%m-%d') - timedelta(1)).split()[0]
        elif release_date == '前天':
            return str(datetime.strptime(time, '%Y-%m-%d') - timedelta(2)).split()[0]
        elif len(release_date.split('-')) == 3:
            return release_date
        elif release_date == '15天前':
            return release_date

    # 打开excel，由excel_table_byindex()调用
    def open_excel(self,file):
        try:
            data = xlrd.open_workbook(file)
            return data
        except Exception as e:
            print(str(e))

    # 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
    # 返回招聘原始名称为key，青峰岗位名称为value的字典
    def excel_table_byindex(self,file, colnameindex=0, by_index=0):
        # 被create_job_name_dic()调用
        data = self.open_excel(file)
        if data == None:
            raise ValueError('Please check the special characters in {}'.format(file))
        table = data.sheets()[by_index]
        nrows = table.nrows  # 行数
        colnames = table.row_values(colnameindex)  # 某一行数据
        list = []
        raw_dic = {}

        for rownum in range(1, nrows):
            row = table.row_values(rownum)
            if '可删除行' == row[0]:
                pass
            elif row[2] == '否':
                pass
            else:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                list.append(app)
                raw_name = row[1].split('    ')[0]
                raw_dic[raw_name] = row[3]
        return raw_dic

    # 读取csv文件，获得青峰岗位名称。每个大类下，以聚合的招聘原始名称为key，青峰岗位名称为value的字典
    def create_job_name_dic(self):
        job_name_dic = {}
        if os.path.exists('./zhilianzhaopingstep1/cluster_result'):
            for filename in os.listdir('./zhilianzhaopingstep1/cluster_result'):
                for result in os.listdir('./zhilianzhaopingstep1/cluster_result/' + filename):
                    if result[-4:] == '.csv':
                        result = './zhilianzhaopingstep1/cluster_result/' + filename + '/' +result
                        raw_dic = self.excel_table_byindex(result)  # 对excel文件进行分析提取出 key-value
                        job_name_dic[filename[:-5]] = raw_dic
        else:
            raise ValueError('The file is not exist.')
        return job_name_dic

    # 将实际发布时间（处理为如2017-08-05） 和 公司名称与职位名称 字段处理后，放入today_temporary数据库
    # 为考虑一周去重用？ 逻辑上有问题，和小伟那边不容易对上。
    def create_temporary_dbs(self):
        start = time.time()
        for information in self.temporary_data.find({},{'_id':0}):   # ？ {'_id':0} 什么意思？就是把_id字段隐藏
            spider_time = information['time']
            release_date = information['release_date']
            # 将日期后的时间去掉
            if len(release_date.split(' ')) == 2:
                real_time = release_date.split(' ')[0]
            else:
                real_time = release_date
            # real_time = self.cal_real_date(spider_time,release_date)
            now = datetime.now()  #调取当前日期
            now_time = now.strftime('%Y-%m-%d')
            yesterday = str(datetime.strptime(now_time, '%Y-%m-%d') - timedelta(1)).split()[0]
            information['real_time'] = real_time  # 增加了一个字段 real_time？
            seg_list = jieba.cut(information['company_job_name'].strip(), cut_all=False)
            company_job_name_fenci = ' '.join(seg_list)
            company_job_name_fenci = company_job_name_fenci.lower()
            company_job_name = [word for word in company_job_name_fenci.split() if word not in self.stop_word_list]
            # ？ 去停用词的目的 ？ 为什么放在？
            company_job_name = ' '.join(company_job_name)
            information['company_job_name'] = company_job_name  # 对该字段做编辑
            try:
                self.today_temporary.insert_one(information) # 创建today_temporary数据库
            except:
                pass
        end = time.time()
        print('昨天的数据已经写入数据库')
        # 写入数据是，对时间做了缩减（只保留天），对company_job_name做了去停用词处理
        # 主要目的是转移数据。但是这个字段company_job_name不应该在爬虫时出现，此时出现比较适合。否则和小伟无法对接上哦。
        print('花了{}s'.format(str(end-start)))


    # 构建总表，只放发布日期为昨天的数据;还是只能根据智联的job_type得知招聘属于哪一大类
    def create_total_zhilian_data(self):
        start = time.time()
        for information in self.today_temporary.find({},{'_id':0}):
            job_type = self.job_dic[information['job_type']]
            for type in job_type:
                try:
                    self.zhilian_data[type].insert_one(information)
                except:
                    pass
            # if information['release_date'] == '昨天':
            #     job_type = self.job_dic[information['job_type']]
            #     for type in job_type:
            #         try:
            #             self.zhilian_data[type].insert_one(information)
            #         except:
            #             pass
        end = time.time()
        print('总表更新完毕')
        print('花了{}s'.format(str(end-start)))

    # 分发职位，每个职位一个表
    def create_job_name_dbs(self):
        start = time.time()

        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d')
        data_range = pd.date_range(end=now_time, periods=7) # 错误，对每个记录参照点应该不一样。选的real_time
        data_range = [i.strftime('%Y-%m-%d') for i in data_range]

        for information in self.today_temporary.find({},{'_id':0}):
            #将非一周前的数据和非15天前的数据，放入3000表中
            if information['real_time'] not in data_range and information['real_time'] != '15天前': # 15天前还是这样吗？
                # ？这个if语句用来做什么的呢？ 答：超过一周的数据不需要去重，15天前的数据为什么也不要？
                # ？这个地方是一个算法错误？
                seg_list = jieba.cut(information['job_name'].strip(), cut_all=False)
                job_name_fenci = ' '.join(seg_list)
                job_name_fenci = job_name_fenci.lower()
                job_name = [word for word in job_name_fenci.split() if word not in self.stop_word_list]
                # ？为什么要去停用词
                job_name = ' '.join(job_name)
                for i in self.job_dic[information['job_type']]:
                    i = '_'.join(i.split('|'))
                    for j in self.job_name_dic[i].keys():
                        if self.if_combine(job_name, j) == True:  # ？这步是什么意思？ 判断新名字和原定义名字是否包含
                            job_title_db = self.job_name_tables[i+':'+self.job_name_dic[i][j]]
                            # 去掉3000张表 10000条的限制
                            # cnt = job_title_db.count()
                            # if cnt >= 10000:
                            #     temp = job_title_db.find_one()
                            #     job_title_db.remove(temp)
                            try:
                                job_title_db.insert_one(information)
                            except:
                                pass
                        else:
                            pass
            elif information['real_time'] in data_range:
                try:
                    self.week_temporary.insert_one(information)
                except:
                    pass
        time.sleep(1)
        # 一周内的数据放在一起了，用唯一性去掉了重复数据
        # todo: 是否速度慢的原因？
        for information in self.week_temporary.find({},{'_id':0}):
            seg_list = jieba.cut(information['job_name'].strip(), cut_all=False)
            job_name_fenci = ' '.join(seg_list)
            job_name_fenci = job_name_fenci.lower()
            job_name = [word for word in job_name_fenci.split() if word not in self.stop_word_list]
            job_name = ' '.join(job_name)
            for i in self.job_dic[information['job_type']]:
                i = '_'.join(i.split('|'))
                for j in self.job_name_dic[i].keys():
                    if self.if_combine(job_name, j) == True:
                        job_title_db = self.job_name_tables[i + ':' + self.job_name_dic[i][j]]
                        # 去掉10000条的限制
                        # cnt = job_title_db.count()
                        # if cnt >= 10000:
                        #     temp = job_title_db.find_one()
                        #     job_title_db.remove(temp)
                        try:
                            job_title_db.insert_one(information)
                        except:
                            pass
                    else:
                        pass
        self.week_temporary.remove()

        end = time.time()
        print('数据分发完毕。')
        print('花了{}s'.format(str(end-start)))



    def run(self):
        self.create_temporary_dbs()
        self.create_total_zhilian_data()
        self.create_job_name_dbs()



import time
start = time.time()
create_dbs = Create_dbs()
create_dbs.run()
end = time.time()
print('创建数据库一共用时{}s'.format(end-start))
print(end-start)
























