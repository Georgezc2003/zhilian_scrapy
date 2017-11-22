# _*_ coding:utf-8 _*_
"""
   @Author 李厚成
   @Date 2016/11/6 8:57
   @配置以省市，职位，时间区分的url,从网站中爬取出省及对应市，职位及其编号和所属类别编号，职位类别及编号
 """

import re
from bs4 import BeautifulSoup
import requests
import collections
#from hmc import ClassHierarchy
import time

header = {
        # 'Cookie':'_hc.v="\"4c951dd7-85a4-4bc2-bc1f-014990ccd929.1463272954\""; dper=baea8cdf709d160e0c1145f05c22aa203c14f91f225c80d0a099ab966d8c5089; ua=18801583533; __utma=205923334.752221830.1463899345.1463899345.1463899651.2; __utmb=205923334.44.10.1463899651; __utmc=205923334; __utmz=205923334.1463899651.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; JSESSIONID=7111686C9873CCC5F2EB3BD606FAAF67; cy=5; cye=nanjing; ll=7fd06e815b796be3df069dec7836c3df; PHOENIX_ID=0a010493-154d753ddfd-b575cc; _tr.u=ZQgMJdekTvHQphmS; _tr.s=rytGUeQGeLnWVuXq',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


class FirstConfigure(object):  # 配置以省市，职位，时间区分的url,从网站中爬取出省及对应市，职位及其编号和所属类别编号，职位类别及编号
    def __init__(self):
        #原取线上，但线上文件出现变化，爬不动了，改为本地文件
        # url_js = "http://sou.zhaopin.com/assets/javascript/basedata.js?v=20160421"  # js数据，包括城市，职位名
        # self.content_js = requests.get(url_js).text.replace(" ", "") # 获取js中内容

        file_object = open('./zhilianzhaopingstep1/basedata.js', 'r', encoding='utf-8')
        
        try:
            self.content_js = file_object.read().replace(" ", "")
        finally:
            file_object.close()
        print("urlup 输出：")
        print(self.content_js[:13])
        # if self.content_js[:13] != 'vardIndustry':
        #     raise TypeError('Whether access the network?')

        # self.url_front = "http://sou.zhaopin.com/jobs/searchresult.ashx?bj="  # URL前面部分
        print("urldown 输出：")
        self.result_index = [] #所有行业代码

    def _obtain_city(self):  # 从js 中提取省市名称,返回键为省，值为市列表的字典
        city = {}  # 存储处理完的省与市对应字典
        data_city = "@" + re.findall("vardCity='(.*?)'", self.content_js)[0].lstrip("var dCity='@489|全国|0")
        print (data_city)
        province = re.findall("(?:@)(\d{3})(.+)(?:\\1)", data_city)
        # foreign = re.findall("[|]0@\d{3}[|](.+?)[|]", data_city)

        for i in province:
            pro_single = re.findall("[\u4e00-\u9fa5]+", i[1])
            city[pro_single[0]] = pro_single[1:]
        #city['海南'].remove('洋浦市')
        #city['海南'].remove('洋浦经济开发区')
        #city['海南'].append('洋浦市%2F洋浦经济开发区')
        #city['广东'].remove('广州')
        if "北京" not in city.keys():
            city["北京"] = ["北京"]
        # if "天津" not in city.keys():
        #    city["天津"] = ["天津"]
        #if "上海" not in city.keys():
        #    city["上海"] = ["上海"]
        #if "重庆" not in city.keys():
        #    city["重庆"] = ["重庆"]

        print(city)
        print("------------")
        return city

    def _obtain_district(self):
        city_id = {}  # 存储处理完的省与市对应字典
        data_city = re.findall("vardCity='(.*?)'", self.content_js)[0].lstrip("var dCity='@489|全国|")
        city = re.findall("(.*?)[@](.*?)\|(.*?)\|", data_city,re.S)
        district_dic = collections.defaultdict(lambda :{})
        data_district = re.findall("vardDistrict='(.*?)'", self.content_js)[0].lstrip("@")
        district = re.findall("(.*?)\|(.*?)\|(.*?)[@]", data_district,re.S)
        city_district_dic = collections.defaultdict(lambda :{})
        for i in city:
            city_id[i[1]] = i[2]
        for i in district:
            district_dic[i[2]][i[0]] = i[1]

        for i in district_dic.keys():
            city_district_dic[city_id[i]] = district_dic[i]

        return city_district_dic

    def _obtain_jobtypeClass(self):  # 从js 中提取工作总类别,如金融、服务业等，返回键为职位总类别，值为其编号的字典
        job_type_class = {}  # 存储处理完的职位总类别序号
        data_job = list(eval(re.findall("varjobtypeClass=(.*?);", self.content_js)[0]))
        # print str(data_job).decode("string_escape")
        for i in data_job:
            job_type_class[i["name"]] = i["id"]
        return job_type_class

    #  从js 中提取工作类别，如软件/互联网/系统集成，硬件开发等
    def _obtain_jobtype(self):  # 返回键为职位类别，值为其所属总类别编号和其编号的列表字典
        job_type = collections.defaultdict(lambda :[])  # 存储处理完的职位字典

        data_job = re.findall("vardJobtype='(.*?)'", self.content_js)[0].lstrip("@")
        # print (str(data_job))
        job = re.findall("(.*?)\|(.*?)\|(.*?)[@]", data_job,re.S)
        # print(job)
        for i in job:
            job_type[i[1]].append(i[0])
            job_type[i[1]].append(i[2])
        return job_type

    #  从js 中提取子工作类别，如高级软件工程师，软件工程师等
    def _obtain_subjobtype(self):  # 返回键为职位，值为其所属类别编号和其编号的列表字典
        subjob_type = collections.defaultdict(lambda :[])  # 存储处理完的子职位字典
        #print (subjob_type)
        data_job = re.findall("vardSubjobtype='(.*?)'", self.content_js)[0].lstrip("@")
        # print (data_job)
        job = re.findall("(.*?)\|(.*?)\|(.*?)[@]", data_job)
        # print(job)
        for i in job:
            subjob_type[i[1]].append(i[0])
            subjob_type[i[1]].append(i[2])
        return subjob_type

    # @staticmethod
    # def class_job(dic0, dic1, dic2):  # 将职位类别及职位进行分类存储，总类别，类别，职位
    #     dic_re = {}
    #     for i in dic0.values():
    #         dic_re[i] = {}
    #         for j in dic1.values():
    #             if (i == j[0]) & (j[0] not in dic_re[i]):
    #                 dic_re[i][j[1]] = []
    #     for i in dic_re.keys():
    #         for j in dic2.values():
    #             if j[0] in dic_re[i]:
    #                 dic_re[i][j[0]].append(j[1])
    #     # print dic_re
    #     return dic_re  # 返回分类结果{:{:[]}}

    # def create_province_num(self):
    #     it_type = []
    #     dic_city = self._obtain_city()  # 省市对应的字典
    #     dic_jobtype = self._obtain_jobtype()  # 职位类别对应的字典
    #     province_dict = {}
    #     for i in dic_jobtype.values():
    #         it_type.append(i[1])
    #     p = dic_city  # 省与城市对应字典
    #     province = p.keys()  # 省名列表
    #     # print (str(p))
    #     for i in province:
    #         dic = {}
    #         for j in it_type:
    #             # 将连接分为两类，时间不限和时间限制为今天
    #             d = str(self.url_front + j + "&jl=" + i) + "&p=1&isadv=0&pd=-1"
    #             h = str(self.url_front + j + "&jl=" + i) + "&p=1&isadv=0&pd=1"
    #             dic[j] = {'unlimit_Date_Urllist': d, 'today_Urllist': h}
    #
    #         # star_url_dic.insert_one({i: dic})  # 以省的名称为key将前期配置的URL存入数据库
    #         province_dict[i] = dic
    #     return province_dict

    def create_jobtype_dic(self):
        dic_jobtypeClass = self._obtain_jobtypeClass()  # 职位总的类别对应的字典
        dic_jobtype = self._obtain_jobtype()  # 职位类别对应的字典
        subjob_type = self._obtain_subjobtype()

        dic_jobtypeClass_dic = {j:i for i,j in dic_jobtypeClass.items()}
        dic_jobtype_dic = {j[0]:i for i,j in dic_jobtype.items()}
        job_dic = collections.defaultdict(lambda :[])
        jobtype_dic = collections.defaultdict(lambda :[])
        subjob_dic = collections.defaultdict(lambda :[])
        jobtype_dic2 = {}

        for i,j in dic_jobtype.items():
            job_dic[j[1]].append(i)
        for i,j in dic_jobtypeClass_dic.items():
            jobtype_dic[j] = job_dic[i]
        for i,j in jobtype_dic.items():
            for m_job in j:
                jobtype_dic2[m_job] = i

        for i,j in subjob_type.items():
            if len(j) == 2:
                subjob_dic[i].append(jobtype_dic2[dic_jobtype_dic[j[1]]])
            elif len(j) == 4:
                subjob_dic[i].append(jobtype_dic2[dic_jobtype_dic[j[1]]])
                subjob_dic[i].append(jobtype_dic2[dic_jobtype_dic[j[3]]])

        return subjob_dic


    # def create_tree(self):
    #     ch = ClassHierarchy(u"智联招聘")
    #     dic_jobtypeClass = self._obtain_jobtypeClass() # 职位总的类别对应的字典
    #     dic_typejobClass = {j:i for i,j in dic_jobtypeClass.items()}
    #
    #     dic_jobtype = self._obtain_jobtype()  # 职位类别对应的字典
    #     dic_typejob = {j[0]:i for i,j in dic_jobtype.items()}
    #     subjob_type = self._obtain_subjobtype()
    #     for job_type_class in dic_jobtypeClass.keys():
    #         ch.add_node(job_type_class,u'智联招聘')
    #     for job_type,index in dic_jobtype.items():
    #         job_index = index[1]
    #         ch.add_node(job_type,dic_typejobClass[job_index])
    #     for sub_job,index in subjob_type.items():
    #         for i in range(1,len(index),2):
    #             # try:
    #             ch.add_node(sub_job, dic_typejob[index[i]])
    #             # except:
    #             #     # print(index)
    #             #     print(dic_typejob[index[i]])
    #     ch.print_()




    # def create_tree(self):
    #
    #     ch = ClassHierarchy(u"智联招聘（www.zhaopin.com）")
    #     dic_jobtypeClass = self._obtain_jobtypeClass()  # 职位总的类别对应的字典
    #     dic_typejobClass = {j: i for i, j in dic_jobtypeClass.items()}
    #
    #     dic_jobtype = self._obtain_jobtype()  # 职位类别对应的字典
    #     dic_typetype = {j[0]:j[1] for i,j in dic_jobtype.items()}
    #     dic_typejob = {j[0]: i for i, j in dic_jobtype.items()}
    #     subjob_type = self._obtain_subjobtype()
    #     for job_type_class in dic_jobtypeClass.items():
    #         job_type_class_index = job_type_class[0]+'('+job_type_class[1]+')'
    #         ch.add_node(job_type_class_index, u'智联招聘（www.zhaopin.com）')
    #     for job_type, index in dic_jobtype.items():
    #         job_index = index[1]
    #         job_type_class_index = dic_typejobClass[job_index]+'('+job_index+')'
    #         job = index[0]
    #         job_index = dic_typejob[job]+'\t('+job+')'
    #         ch.add_node(job_index, job_type_class_index)
    #     for sub_job, index in subjob_type.items():
    #         for i in range(1, len(index), 2):
    #             job_num = ' '.join(index[i-1:i+1])
    #             job_num = job_num + ' ' + dic_typetype[index[i]]
    #             job_num_index = sub_job+'\t('+job_num+')'
    #             ch.add_node(job_num_index, dic_typejob[index[i]]+'\t('+index[i]+')')
    #             if len(job_num_index.split()) < 3:
    #                 pass
    #     ch.print_()


    def statistics_num(self,url):
        try:
            web_page = requests.get(url, headers=header)
            soup = BeautifulSoup(web_page.text, 'lxml')
            num_text = soup.select('.search_yx_tj em')[0].text

            # pass
            if len(num_text) > 0:
                nums = int(num_text)
                return nums
            else:
                nums = 0
                return nums
        except Exception as e:
            print(Exception, ":", e)
            print ("url 输出：")
            print(url)
            nums = 0
            return nums


    def create_url(self):  # 创建起始url，我们是配出来的
        countnum = 0;
        index_list = []
        dic_jobtype = self._obtain_jobtype()  # 职位类别对应的字典
        print(dic_jobtype)
        dic_typetype = {j[0]:j[1] for i,j in dic_jobtype.items()}
        print(dic_typetype)
        subjob_type = self._obtain_subjobtype()
        print(subjob_type)



        for sub_job, index in subjob_type.items():
            for i in range(1, len(index), 2):
                job_num = ' '.join(index[i-1:i+1])
                job_num = job_num + ' ' + dic_typetype[index[i]]
                index_list.append(job_num)

        level_dic = collections.defaultdict(lambda :[])
        for i in index_list:
            a = i.split()
            level_dic[a[1]].append(a[0])

        # pd = -1是不限，1是当天
        url_list = []
        print("---------------------------")
        print(self._obtain_city().keys())

        for province in self._obtain_city().keys():
            for index in level_dic.keys():
                url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj={}&jl={}&pd=1'.format(index, province)
                num = self.statistics_num(url)

                #--------这里分级有问题---未测试
                if num > 5400:
                    for index2 in level_dic[index]:
                        url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj={}&sj={}&jl={}&pd=1'.format(index,index2, province)
                        url_list.append(url)
                        #print(url)
                        countnum = countnum + 1
                        print(countnum)
                        with open('List5400p.txt', 'a') as f:
                            f.write(url + "\n")
                else:
                    url_list.append(url)
                    countnum = countnum+1
                    print(countnum)
                    with open('List.txt', 'a') as f:
                        f.write(url+"\n")
                #--------------------
            #耗时长
        print(len(url_list))
        # 文件存储函数
        return url_list

    def get_job_dic(self):
        dic_jobtypeClass = self._obtain_jobtypeClass()  # 职位总的类别对应的字典
        dic_typejobClass = {j: i for i, j in dic_jobtypeClass.items()}
        dic_jobtype = self._obtain_jobtype()  # 职位类别对应的字典
        dic_typetype = {j[0]:j[1] for i,j in dic_jobtype.items()}
        subjob_type = self._obtain_subjobtype()
        job_dic = collections.defaultdict(lambda :[])
        result_list = []
        for sub_job, index in subjob_type.items():
            for i in range(1, len(index), 2):
                job_num = ' '.join(index[i-1:i+1])
                job_num = job_num + ' ' + dic_typetype[index[i]]
                job_num_index = sub_job+'\t('+job_num+')'
                result_list.append(job_num_index)
        for i in result_list:
            name = i.split('\t')[0]
            type = dic_typejobClass[i.split('\t')[1].split()[-1][:-1]]
            job_dic[name].append(type)
        for i,j in job_dic.items():
            job_dic[i] = set(j)
        return job_dic
#
# if __name__ == '__main__':
#     start = time.time()
#     firstConfigure = FirstConfigure()
#     # city_district_dic = firstConfigure._obtain_district()
#     # jobtype = firstConfigure._obtain_jobtype()
#     # province_dict_city = firstConfigure._obtain_city()  # 省与城市对应字典
#     # province_dict = firstConfigure.create_province_num()  #
#     # firstConfigure.get_job_dic()
#     # url_list = firstConfigure.create_url()
#     # print(len(url_list))
# #     end = time.time()
# #     print(end - start)
#
#     firstConfigure.create_url()

