# -*- coding: utf-8 -*-
# @Time    : 2017/1/7
# @Author  : Sunyan Gu, revised by Lang Fei
# @Site    : NJUPT


from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.http import Request
from zhilianzhaopingstep1.items import Zhilianzhaopingstep1Item
import re
from zhilianzhaopingstep1.first_configure import FirstConfigure
import datetime


class zhilianSpider(CrawlSpider):
    RuningUrlNum = 0
    name = 'zhilian_step1'
    CountTotal=0
    job_cnt_factor = 0  # 作用域有问题
    firstConfigure = FirstConfigure()  # 初始类实例
    # firstConfigure.create_url()
    # start_urls = firstConfigure.create_url() # 起始url的获得
    # start_urls = [
    #     "http://sou.zhaopin.com/jobs/searchresult.ashx?bj = 3010000 & sj = 329 & jl = 天津 & pd = 2"
    #     "http://sou.zhaopin.com/jobs/searchresult.ashx?bj = 3010000 & sj = 2144 & jl = 天津 & pd = 2"
    #     "http://sou.zhaopin.com/jobs/searchresult.ashx?bj = 7001000 & sj = 844 & jl = 河南 & pd = 2"
    #     "http://sou.zhaopin.com/jobs/searchresult.ashx?bj = 7001000 & sj = 845 & jl = 河南 & pd = 2"
    #     "http://sou.zhaopin.com/jobs/searchresult.ashx?bj = 7001000 & sj = 004 & jl = 河南 & pd = 2"
    #     ]
    print("start_urls prepared")
    start_urls = { #必须分开，否则识别有问题
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&pd=7&ispts=1&isfilter=1&p=1&bj=121100&sj=061",
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&pd=7&ispts=1&isfilter=1&p=1&bj=121100&sj=064",
        #  "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&pd=2&ispts=1&isfilter=1&p=1&bj=121100&sj=487"
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&pd=7&ispts=1&isfilter=1&p=1&bj=121100&sj=065",
    #     "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&pd=2&ispts=1&isfilter=1&p=1&bj=121100&sj=065",
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&pd=7&ispts=1&isfilter=1&p=1&bj=121100&sj=932"
        # "http://sou.zhaopin.com/jobs/searchresult.ashx?bj=121100&jl=北京&pd=2"
        # "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&isadv=0&ispts=1&isfilter=1&p=1&bj=160000&sj=861"
        # "http://sou.zhaopin.com/jobs/searchresult.ashx?bj=121300&jl=北京&pd=2"
     }
    print(len(start_urls))
    # ？有用吗headers？ 伪装成浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22158a570e1f4524-0630e0dd6ca1fc-5c4f231c-2073600-158a570e1f58e4%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%7D; dywez=95841923.1481543197.6.3.dywecsr=other|dyweccn=121124451|dywecmd=cnt; metroopen=0; notlogin=1; _zg=%7B%22uuid%22%3A%20%221596206e4bc9f-05a41ff602a077-5d4e211f-1fa400-1596206e4bd86e%22%2C%22sid%22%3A%201483408336.062%2C%22updated%22%3A%201483409337.614%2C%22info%22%3A%201483408336065%7D; __xsptplus30=30.5.1483751939.1483752824.2%233%7Cgraph.qq.com%7C%7C%7C%7C%23%23zMgznXAT5HqL1xmCpo5FyRwbRr4QWVCX%23; LastCity%5Fid=532; LastCity=%e6%b2%b3%e5%8c%97; _jzqckmp=1; JSSearchModel=0; _jzqx=1.1480244430.1483941230.4.jzqsr=jobs%2Ezhaopin%2Ecom|jzqct=/xining/sj659/.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx; jobtypeopen=1; firstchannelurl=https%3A//passport.zhaopin.com/account/login%3FbkUrl%3Dhttp%253A%252F%252Fsou.zhaopin.com%252Fjobs%252Fsearchresult.ashx%253Fispts%253D1%2526isfilter%253D1%2526p%253D1%2526bj%253D4082000%2526sj%253D2175; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; __utmt=1; JsNewlogin=2035029440; JSloginnamecookie=18801583533; JSShowname=%e9%a1%be%e5%ad%99%e7%82%8e; at=6f482ec4a3104559b5e3f609d95a5e13; Token=6f482ec4a3104559b5e3f609d95a5e13; rt=32eed09347204bccafdfe6cb2453f065; JSpUserInfo=24342E6955715D7943320B754A6A5F71076A5868456B4F7409333979246B4C345B6950715379443202754C6A5371076A5C68426B4A7409332079246B4C3414F1312AE5094F327675346A5671056A5868426B4174063347795C6B49345A695F712B7905324275576A08715B6A04684A6B2A74663348795B6B4A342B693C71567945321E75406A4B71066A59684B6B4C7400334E792B6B3D3457695971507921327275446A2171796A5E68496B4A74063346795B6B45345C695D71507921326775446A5A710F6A3A68386B447403334E793F6B2134246955710879163252754F6A5C71056A5168476B4B740B334D795D6B1334526909715879433203751F6A5B71026A5968126B4A74533313795A6B40340C6959715A79153208758; uiioit=213671340F69436B5A6A507947644774053505325D755D6D51683B7420734936053409698; lastchannelurl=https%3A//passport.zhaopin.com/account/login%3FbkUrl%3Dhttp%253A%252F%252Fjobs.zhaopin.com%252F456094211250032.htm; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1482847729,1483406511,1483751849,1483955363; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1483966360; loginreleased=1; LastJobTag=%e8%8a%82%e6%97%a5%e7%a6%8f%e5%88%a9%7c%e4%ba%94%e9%99%a9%e4%b8%80%e9%87%91%7c%e7%bb%a9%e6%95%88%e5%a5%96%e9%87%91%7c%e5%b8%a6%e8%96%aa%e5%b9%b4%e5%81%87%7c%e5%91%98%e5%b7%a5%e6%97%85%e6%b8%b8%7c%e5%85%a8%e5%8b%a4%e5%a5%96%7c%e9%a4%90%e8%a1%a5%7c%e4%ba%a4%e9%80%9a%e8%a1%a5%e5%8a%a9%7c%e9%80%9a%e8%ae%af%e8%a1%a5%e8%b4%b4%7c%e5%8c%85%e4%bd%8f%7c%e5%8a%a0%e7%8f%ad%e8%a1%a5%e5%8a%a9%7c%e5%bc%b9%e6%80%a7%e5%b7%a5%e4%bd%9c%7c%e5%ae%9a%e6%9c%9f%e4%bd%93%e6%a3%80%7c%e5%8c%85%e5%90%83%7c%e5%b9%b4%e5%ba%95%e5%8f%8c%e8%96%aa%7c%e5%b9%b4%e7%bb%88%e5%88%86%e7%ba%a2%7c%e8%a1%a5%e5%85%85%e5%8c%bb%e7%96%97%e4%bf%9d%e9%99%a9%7c%e9%ab%98%e6%b8%a9%e8%a1%a5%e8%b4%b4%7c%e5%85%8d%e8%b4%b9%e7%8f%ad%e8%bd%a6%7c%e6%88%bf%e8%a1%a5%7c%e8%82%a1%e7%a5%a8%e6%9c%9f%e6%9d%83%7c%e9%87%87%e6%9a%96%e8%a1%a5%e8%b4%b4; LastSearchHistory=%7b%22Id%22%3a%220a972eb0-24cb-43c8-b708-865c0d3c22d3%22%2c%22Name%22%3a%22%e6%b2%b3%e5%8c%97+%2b+%e5%b8%82%e5%9c%ba+%2b+%e5%b8%82%e5%9c%ba%e4%b8%93%e5%91%98%2f%e5%8a%a9%e7%90%86%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fispts%3d1%26isfilter%3d1%26p%3d1%26bj%3d4082000%26sj%3d171%22%2c%22SaveTime%22%3a%22%5c%2fDate(1483966362155%2b0800)%5c%2f%22%7d; SubscibeCaptcha=D581E43F8DA1E0FADD638C8103D7E943; dywea=95841923.4129866369659275300.1480244388.1483958334.1483962658.36; dywec=95841923; dyweb=95841923.50.9.1483966346266; __utma=269921210.177375426.1480244388.1483958334.1483962658.36; __utmb=269921210.50.9.1483966346268; __utmc=269921210; __utmz=269921210.1481543197.6.3.utmcsr=other|utmccn=121124451|utmcmd=cnt; _qzja=1.2044009355.1481260065167.1483954819479.1483962686038.1483966368288.1483966368729.0.0.0.365.23; _qzjb=1.1483962686038.31.0.0.0; _qzjc=1; _qzjto=41.4.0; _jzqa=1.411727141887181000.1480244430.1483958334.1483962686.32; _jzqc=1; _jzqb=1.46.10.1483962686.1'
    }

    # 被parse()调用，传参是如何完成的呢？ 还涉及callback函数，像是利用response，好像是框架系统定义的函数。
    def parse_item(self, response):
        selector = Selector(response)  # 为什么不可以直接用response.xpath,如parse()
        job_name = selector.xpath('//div[@class="inner-left fl"]/h1/text()').extract() # 普通招聘
        company_name = selector.xpath('//div[@class="inner-left fl"]/h2/a/text()').extract() # 普通招聘
        jx_name = selector.xpath('//h1[@class="cJobDetailInforTitle" and @id="JobName"]/text()').extract() # 校园招聘
        cx_name = selector.xpath('//li[@class="cJobDetailInforWd1 marb" and @id="jobCompany"]/a/text()').extract() # 校园招聘
        recruitment_link = response.url  # 招聘网址
        now = datetime.datetime.now()
        time = now.strftime('%Y-%m-%d')  # 当前时间，后面算法没托底，不确定该字段是否有用
        item = response.meta['item']

        if len(jx_name) != 0 and len(cx_name) != 0:
            # 校园招聘
            jx_description_list = selector.xpath('//p[@class="mt20"]/text()').extract() # 职位描述
            jx_description = ''
            for i in jx_description_list:
                a = i.strip()
                if len(a) > 0:
                    jx_description += a + '\n'
            xy_work_place = selector.xpath('//ul[@class ="cJobDetailInforBotWrap clearfix c3"]/li[2]/text()').extract()[0].strip()
            xy_job_type_list = selector.xpath('//ul[@class ="cJobDetailInforBotWrap clearfix c3"]/li[4]/text()').extract()
            if len(xy_job_type_list)!=0:
                xy_job_type = xy_job_type_list[0].strip()
            else:
                xy_job_type = ''
            # 发现网页此字段存在为空，当提取不到字段时，可能是空列表，但不会填充上空字符串''
            xy_recruiting_number = selector.xpath('//ul[@class ="cJobDetailInforBotWrap clearfix c3"]/li[6]/text()').extract()[0].strip()
            xy_release_date = selector.xpath('//ul[@class ="cJobDetailInforBotWrap clearfix c3"]/li[8]/text()').extract()[0].strip()
            # 共往 item中添加15项，与普通招聘缺月薪、最低学历，工作经验为空字符串
            item['company_name'] = cx_name[0].strip()
            item['job_category'] = '' # 工作性质，兼职还是全职，校园招聘为空（其实都是全职）
            item['job_description'] = jx_description
            item['job_name'] = jx_name[0].strip()
            item['job_type'] = xy_job_type
            item['minimum_education'] = '' # 校园招聘本身就没有这个数据提供
            item['monthly_salary'] = '' # 校园招聘本身就没有这个数据提供
            item['recruiting_number'] = xy_recruiting_number
            item['recruitment_link'] = recruitment_link  # 招聘网址
            item['release_date'] = xy_release_date
            item['time'] = time
            item['welfare'] = ''  # 校园招聘为空
            item['work_experience'] = '' # 校园招聘本身就没有这个数据提供
            item['work_place'] = xy_work_place
            item['company_job_name'] = cx_name[0] + ' ' + jx_name[0] + ' ' + xy_work_place
            item['job_compus'] = 1
            print('校园招聘出现一条')

        elif len(job_name) != 0 and len(company_name) != 0:
            # 普通招聘
            # job_name = selector.xpath('//div[@class="inner-left fl"]/h1/text()').extract()[0]
            # company_name = selector.xpath('//div[@class="inner-left fl"]/h2/a/text()').extract()[0]
            # -----
            # if selector.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]/p/text()').extract()[0] != "\r\n                            ":
            # job_description_list = selector.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]/p/text()').extract()
            job_description_list = selector.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]').extract()
            job_description_list1 = selector.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]') #//div[@class="tab-inner-cont"]
            info = job_description_list1.xpath('string(.)').extract()[0]
            company_description_list = selector.xpath('/html/body/div[6]/div[1]/div[1]/div/div[2]')
            company_description = company_description_list.xpath('string(.)').extract()[0]
            # print(company_description)
            # print(info)
            # else:# selector.xpath(' / html / body / div[6] / div[1] / div[1] / div / div[1] / p / span /text()| / html / body / div[6] / div[1] / div[1] / div / div[1] / p / strong /span /text()').extract()[0] != "\r\n                            ":
            #     job_description_list = selector.xpath(' / html / body / div[6] / div[1] / div[1] / div / div[1] / p / span /text()| / html / body / div[6] / div[1] / div[1] / div / div[1] / p / strong /span /text()').extract()
            #     print("empty1")
            # elif selector.xpath(' / html / body / div[6] / div[1] / div[1] / div / div[1] / p / strong /text()| / html / body / div[6] / div[1] / div[1] / div / div[1] / div /strong /text()').extract()[0] != "\r\n                            ":
            #     job_description_list = selector.xpath(' / html / body / div[6] / div[1] / div[1] / div / div[1] / p / strong /text()| / html / body / div[6] / div[1] / div[1] / div / div[1] / div /strong /text()').extract()
            # else:
            # print(selector.xpath(' / html / body / div[6] / div[1] / div[1] / div / div[1] / p / strong /text()| / html / body / div[6] / div[1] / div[1] / div / div[1] / div /strong /text()').extract()[0] != "\r\n                            ")
            # print(selector.xpath(' / html / body / div[6] / div[1] / div[1] / div / div[1] / p / strong /text()| / html / body / div[6] / div[1] / div[1] / div / div[1] / div /strong /text()').extract()[0] == -1)
                # print("empty2")
                # print(selector.xpath(' / html / body / div[6] / div[1] / div[1] / div / div[1] / p[1] / strong / span /text()').extract())
            # -----
            # print(job_description_list)
            # print(selector.xpath(' /html/body/div[6]/div[1]/div[1]/div/div[1]/p/text()').extract()[1])

            # job_description = ''
            job_description = info
            # for i in job_description_list:
            #     a = i.strip()
            #     if len(a) > 0:
            #         job_description += a + '\n'

            welfare = selector.xpath('//div[@class="welfare-tab-box"]/span/text()').extract()
            job_category = selector.xpath('//ul[@class="terminal-ul clearfix"]/li[4]/strong/text()').extract()[0].strip()
            monthly_salary = selector.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract()[0].strip()
            job_type = selector.xpath('//ul[@class="terminal-ul clearfix"]/li[8]/strong/a/text()').extract()[0].strip()
            minimum_education_list = selector.xpath('//ul[@class="terminal-ul clearfix"]/li[6]/strong/text()').extract()
            if len(minimum_education_list) != 0:
                minimum_education = minimum_education_list[0].strip()
            else:
                minimum_education = ''
            recruiting_number = selector.xpath('//ul[@class="terminal-ul clearfix"]/li[7]/strong/text()').extract()[0].strip()
            try:
                release_date = selector.xpath('//ul[@class="terminal-ul clearfix"]/li[3]/strong/span/text()').extract()[0].strip()
            except:
                release_date = selector.xpath('//ul[@class="terminal-ul clearfix"]/li[3]/strong/text()').extract()[0].strip()

            work_experience = selector.xpath('//ul[@class="terminal-ul clearfix"]/li[5]/strong/text()').extract()[0].strip()
            work_place = selector.xpath('//ul[@class="terminal-ul clearfix"]/li[2]/strong/a/text()').extract()[0].strip()

            # 共往item中添加15项
            item['company_name'] = company_name[0].strip()
            item['job_category'] = job_category  # 工作性质，兼职还是全职
            item['job_description'] = job_description
            item['company_description'] = company_description
            item['job_type'] = job_type
            item['job_name'] = job_name[0].strip()
            item['minimum_education'] = minimum_education
            item['monthly_salary'] = monthly_salary
            item['recruitment_link'] = recruitment_link  # 招聘网址
            item['recruiting_number'] = recruiting_number  #
            item['release_date'] = release_date
            item['time'] = time
            item['welfare'] = welfare
            item['work_experience'] = work_experience #
            item['work_place'] = work_place
            item['company_job_name'] = company_name[0]+' '+job_name[0]+' '+work_place
            item['job_compus'] = 0

            # 是否是校园招聘

        # makeLog.log4("爬取%s的招聘信息! ", recruitment_link)
        yield item

    # 官网：parse() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。
    # 该方法负责解析返回的数据(response data)，提取数据(生成item)  以及  生成需要进一步处理的URL的 Request 对象。
    def parse(self, response):
        # self.job_cnt_factor = self.job_cnt_factor - 1
        print("------------------------------------")
        item = Zhilianzhaopingstep1Item()
        # 感觉response返回的是查询页面
        item_urls = response.xpath('//td[@class="zwmc"]/div/a/@href').extract()
        # 找到该页面全部职位url链接共60个 本页所有工作 Url，type:list

        job_cnt = response.xpath('//span[@class="search_yx_tj"]/em/text()').extract()[0]
        # 计数器，在某一查询条件下总的职位数量，如2698
        print("Job_cnt:"+job_cnt)
        # self.CountTotal = self.CountTotal + int(job_cnt)
        job_cnt = int(job_cnt)
        # type: string2int
        # 5400 这里没有判断
        job_cnt_now = 0

        if job_cnt > 60:  # 应该是一页60个职位数量，？？item_urls的数量和job_cnt为什么会不一致？？

            for item_url in item_urls:  # 下面是生成需要进一步处理的URL的 Request 对象
                #print("Current Url:" + item_url)
                job_cnt_now = job_cnt_now +1
                self.CountTotal = self.CountTotal + 1
                print ("Url Requested "+str(self.job_cnt_factor * 60 + job_cnt_now)+" of "+str(job_cnt))
                yield Request(item_url,callback=self.parse_item,meta={'item': item},headers=self.headers)
            try:  # 下面代码：当本页url全部发送request之后，寻找下一页新的页面
                next_url = response.xpath('//li[@class="pagesDown-pos"]/a/@href').extract()[0]
                # self.job_cnt_factor = self.job_cnt_factor + 1
                self.RuningUrlNum = self.RuningUrlNum - 1
                print("next page")
                yield Request(next_url,headers=self.headers)
            except:
                pass
        else:
            for item_url in item_urls[:job_cnt]:
                #print("Current Url:" + item_url)
                job_cnt_now = job_cnt_now + 1
                self.CountTotal = self.CountTotal + 1
                print ("Url Requested "+str(job_cnt_now)+" of "+str(job_cnt))
                yield Request(item_url, callback=self.parse_item, meta={'item': item},headers=self.headers)

            try:
                next_url = response.xpath('//li[@class="pagesDown-pos"]/a/@href').extract()[0]
                # 好像是用不到的
                yield Request(next_url,headers=self.headers)
            except:
                pass

        self.RuningUrlNum = self.RuningUrlNum + 1
        print("Proccessed: Link No." + str(self.RuningUrlNum)+" of "+str(len(self.start_urls)))
        print(self.CountTotal)
        # Url 执行顺序是随机的，这个过程难以控制。
        # 当前如果要做按顺序执行的话：
        # 我们可以通过Request的priority控制url的请求的执行顺序，但由于网络请求的不确定性，
        # 不能保证返回也是按照顺序进行的，如果需要进行逐个url请求的话，吧url列表放在meta对
        # 象里面，在response的时候迭代返回下一个Request对象到调度器，达到顺序执行的目的，暂时没有更好的方案

