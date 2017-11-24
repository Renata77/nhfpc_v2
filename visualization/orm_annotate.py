#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: 齐天亮
@license: Apache Licence  
@contact: qitianliang@outlook.com
@site: https://gitee.com/yongfeng006 
@software: PyCharm 
@file: orm_annotate.py 
@time: 2017/11/9 15:34 
"""
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nhfpc_v2.settings")  # project_name 项目名称
django.setup()
from django.db.models import Count, Avg, Sum, Case, When, Value, CharField, FloatField
from django.db.models.functions import Cast
from django.db.models import Q
from visualization.models import DevOptions
from functools import reduce


# res = DevOptions.objects.filter(qid='bigdata').filter(tid=1).all().values('area').annotate(count=Count('area'))
# print(res)
# print(float('9'))
#
#
# res = DevOptions.objects.filter(qid='bigdata').filter(tid=1).filter(gather_level__isnull=False).all()\
#     .values('gather_level','area','options').annotate(count=Count('area'))
# for re in res:
#     print(re)
# print(res)
#
# res = DevOptions.objects.filter(qid='bigdata').filter(tid=1).all()\
#     .values('gather_level','area','options').annotate(count=Count('area'))
# for re in res:
#     print(re)
# print(res)
#
# description_option = ['基于wifi移动医护','基于物联网的业务','室内定位导航','PACS推车等图像','分级诊疗视频业务','外网互联网业务','掌上医院']
# res = DevOptions.objects.filter(qid='hospital').filter(tid=32).filter(reduce(lambda x, y: x | y, [Q(options__contains=item+"**") for item in description_option])).distinct().values('qid','tid','options','organ_level','organ_name').all().count()
# res1 = DevOptions.objects.filter(qid='hospital').filter(tid=32).filter(options__contains='未涉及**').all().count()
# print(res,res1,res+res1)
#
# #     .values('options')\
# # .values('gather_level','area','options').annotate(count=Count('options'))
# # for re in res:
# #     print(re)
# # print(res)
#     # .values('gather_level','area','options').annotate(count=Count('area'))
#
# # res = DevOptions.objects.filter(qid='hospital').filter(tid=18).all().values('gather_level','area').annotate(avg = Avg('options'))
# res1 = DevOptions.objects.filter(qid='hospital').filter(tid=18).all().values('qid').annotate(avg=Avg('options'))
# # for re in res:
# #     print(re)
#
#
# res = DevOptions.objects.filter(qid='hospital').filter(tid__in=[19,6]).all().values('gather_level','tid','area').annotate(avg = Avg('options'))
# print(res)
# # print(res1)
#
#
# res = DevOptions.objects.filter(qid='location').filter(tid=9).filter(gather_level__isnull=False).all().values( 'qid').annotate(avg=Avg('options'))
# print(res)

def get_options_proper_index(x, interval_list):
    index = len(interval_list)
    for idx, y in enumerate(interval_list):
        if x < y:
            return idx
    return index


interval_list = [100, 200, 300]
for x in [200, 100, 18, 290, 390]:
    y = get_options_proper_index(x, interval_list)
    print(y, x, interval_list)

for x, y in zip([], []):
    print('xy', x, y)
if not len([]):
    print('ok')
if not '':
    print('ok')

# x =
description_option = [100,200,300]
segment_option = []
segment_option.append((0,description_option[0]))
for idx,segment in enumerate(description_option[:-1]):
    segment_option.append((segment,description_option[idx+1]))

# list = [When(options__lte= x,options_gte=y,then=Value(str(x)+'~'+str(y)) for x,y  in description_option]
# reduce(lambda x,y: x|y , )

res = DevOptions.objects.filter(qid='hospital').filter(tid=6) \
    .all().values('area', 'organ_level').annotate(
    segment=Case(
         * [When(options__gte=x, options__lt=y,  then=Value(str(x) + '~' + str(y))) for x,y in segment_option],
        default=Value('大于'+str(description_option[-1])),
        output_field=CharField(),
    ),
).values('organ_level').annotate(count=Count('organ_level'))

print(res)

# res = DevOptions.objects.filter(qid='hospital').filter(tid=6).filter(gather_level__isnull=False) \
#     .all().values('area','organ_name','options')
# for re in res:
#     print(re)
# print(res)
print(description_option)
print(*description_option)


res_1 = DevOptions.objects.filter(qid='location').filter(tid__in=[10,11]).values('tid','organ_name','organ_level','area','options')

# for

print(res_1)
print(len(res_1))
res_2 = DevOptions.objects.filter(qid='location').filter(tid__in=[11]).values('tid','organ_name','organ_level','area','options')
print(res_2)
print(len(res_2))
