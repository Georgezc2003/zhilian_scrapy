# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class Zhilianzhaopingstep1Item(Item):
    # company_introduction = Field() # discarded
    # company_name = Field()
    # company_profile = Field() # discarded
    # job_description = Field()
    # job_name = Field()
    # job_profile = Field() # discarded
    # recruitment_link = Field()
    # welfare = Field()
    # release_date = Field()
    # work_place = Field()
    # time = Field()
    # job_category = Field()
    # job_type = Field()
    # company_job_name = Field()

    company_name = Field()
    job_category  = Field() # 工作性质，兼职还是全职
    job_description = Field()
    company_description = Field()
    job_type = Field()
    job_name = Field()
    minimum_education = Field() # new
    monthly_salary = Field() # new
    recruitment_link = Field()  # 招聘网址
    recruiting_number  = Field() # new
    release_date = Field()
    time = Field()
    welfare = Field()
    work_experience = Field() # new
    work_place = Field()
    company_job_name = Field() # ???
    job_compus = Field()