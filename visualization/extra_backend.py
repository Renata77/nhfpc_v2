#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: 齐天亮
@license: Apache Licence  
@contact: qitianliang@outlook.com
@site: https://gitee.com/yongfeng006 
@software: PyCharm 
@file: extra_backend.py 
@time: 2017/11/10 3:48 
"""
from .models import DevOptions,RateTable
from .models import DevOptionsDescription, HospAllChoiceStat, HospAllMultiStat, DevPaper, DevOptions, DevQuestions
from decimal import *
from django.db.models import Count, Avg, Sum, Case, When, Value, CharField, FloatField, Q
from functools import reduce

map_id = {
    'hospital': 'd7773b71-6986-4cd7-b885-f77e21bd1549',
    'location': '36d06675-d061-4a1c-93df-1718fd267fff',
    'bigdata': 'a24a4001-6285-467b-a0d5-9be02379a3b0',
}
map_key = {
    '一级东部': 'level1_east',
    '二级东部': 'level2_east',
    '三级东部': 'level3_east',
    '未定级东部': 'level0_east',
    '一级小计': 'level0_count',
    '一级西部': 'level1_west',
    '二级西部': 'level2_west',
    '三级西部': 'level3_west',
    '未定级西部': 'level0_west',
    '二级小计': 'level2_count',
    '三级小计': 'level3_count',
    '一级中部': 'level1_middle',
    '二级中部': 'level2_middle',
    '三级中部': 'level3_middle',
    '未定级中部': 'level0_middle',
    '未定级小计': 'level0_count',
    '小计小计': 'sum',

}
area_list = ['东部', '中部', '西部']
area_map = {
    '东部': 'east',
    '中部': 'middle',
    '西部': 'west',
}
level_list = ['三级', '二级', '一级', '未定级']
level_map = {
    '三级': 'level3',
    '二级': 'level2',
    '一级': 'level1',
    '未定级': 'level0',
}
organ_level_list = ['省级卫计委', '市级卫计委']
organ_level_map = {
    '省级卫计委': 'province',
    '市级卫计委': 'city'
}

def extra_rate_health(qid,tid):
    data = []
    # DevOptions.objects.filter(qid=qid).filter(tid__in=tid_list).all().values('gather_level', 'tid',
    #                                                                               'area').annotate(avg=Avg('options'))
    # for tid in tid_list:
    theme = qid + '-' + str(tid[0:2]) + '-' + str(tid[2:])
    ##print(theme)

    # TODO 获取填报数值的区间进行处理

    def query_option_all():
        return RateTable.objects.filter(theme=theme).filter(organ_level__in=organ_level_list).all()

    ##print(query_option_all().count())
    tmp_level_area_set = query_option_all().values('organ_level', 'area').annotate(avg=Avg('rate'))
    tmp_set = query_option_all().values('theme').annotate(avg=Avg('rate'))
    stat_line = []
    line = {'option': '均值(%)'}
    if len(tmp_set):
        line['sum'] = str(round(float(tmp_set[0].get('avg', 0.0)) * 100, 1))
    else:
        return stat_line
    for level in organ_level_list:
        tmp_level_area_list = [x for x in tmp_level_area_set if x['organ_level'] == level]
        line[organ_level_map.get(level, '') + "_count"] = '0.0' if not len(tmp_level_area_list) else str(
            round(sum([x['avg'] for x in tmp_level_area_list]) / len(tmp_level_area_list) * 100, 1))
        for area in area_list:
            key = organ_level_map.get(level, '') + "_" + area_map.get(area, '')
            tmp_list = [x for x in tmp_level_area_list if len(tmp_level_area_list) and x['area'] == area]
            value = '0.0' if not len(tmp_list) else str(round(float(tmp_list[0].get('avg', 0.0)) * 100, 1))
            line[key] = value

    stat_line.append(line)
    params = DevOptionsDescription.objects.filter(qid=qid).filter(tid=tid).values()
    description_queryset = []
    if len(params):
        description_queryset = params
    else:
        return stat_line
    # description_list = [x['description'] for x in description_queryset if len(description_queryset)]
    description_segment_list = [x['options'].split(';') for x in description_queryset if len(description_queryset)]
    if len(description_segment_list):
        description_segment_list = description_segment_list[0]
    else:
        return stat_line
    ##print(description_segment_list)
    segment_option = []
    segment_option.append((0, description_segment_list[0]))
    for idx, segment in enumerate(description_segment_list[:-1]):
        segment_option.append((segment, description_segment_list[idx + 1]))
    segment_description = []
    segment_description.append('0~' + str(description_segment_list[0]))
    for index, number in enumerate(description_segment_list[:-1]):
        segment_description.append(str(number) + '~' + str(description_segment_list[index + 1]))
    segment_description.append('大于' + str(description_segment_list[-1]))

    def query_option(segment_option, description_segment_list):
        return RateTable.objects.filter(theme=theme).filter(
            organ_level__in=organ_level_list).all().annotate(
            segment=Case(
                *[When(rate__gte=x, rate__lt=y, then=Value(str(x) + '~' + str(y))) for x, y in segment_option],
                default=Value('大于' + str(description_segment_list[-1])),
                output_field=CharField(),
            ),
        )

    level_sum_set = query_option(segment_option, description_segment_list).values('organ_level').annotate(
        count=Count('organ_level'))
    level_area_sum_set = query_option(segment_option, description_segment_list).values('organ_level', 'area').annotate(
        count=Count('area'))
    ##print(level_sum_set, level_area_sum_set)
    count_all = RateTable.objects.filter(theme=theme).filter(organ_level__in=organ_level_list).all().count()
    option_count_set = query_option(segment_option, description_segment_list).values('segment').annotate(
        count=Count('segment'))
    level_count_set = query_option(segment_option, description_segment_list).values('organ_level').annotate(
        count=Count('organ_level'))
    level_area_count_set = query_option(segment_option, description_segment_list).values('organ_level',
                                                                                         'area').annotate(
        count=Count('area'))
    option_level_count_set = query_option(segment_option, description_segment_list).values('organ_level',
                                                                                           'segment').annotate(
        count=Count('segment'))
    option_level_area_count_set = query_option(segment_option, description_segment_list).values('organ_level',
                                                                                                'segment',
                                                                                                'area').annotate(
        count=Count('segment'))
    for option in segment_description:
        line = {'option': option}
        ##print(option_count_set)
        option_count_list = [x for x in option_count_set if x['segment'] == option]
        ##print('---------------------', option_count_list)
        option_count = get_proper_count(option_count_list)
        ##print('count---------------------------------', option_count, count_all)
        line['sum'] = get_proper_percent(option_count, count_all)
        for level in organ_level_list:
            option_level_count_list = [x for x in option_level_count_set if
                                       x['segment'] == option and x['organ_level'] == level]
            option_level_count = get_proper_count(option_level_count_list)
            key = organ_level_map.get(level, '') + "_count"
            level_count_list = [x for x in level_count_set if x['organ_level'] == level]
            level_count = get_proper_count(level_count_list)
            line[key] = get_proper_percent(option_level_count, level_count)
            for area in area_list:
                option_level_area_count_list = [x for x in option_level_area_count_set if
                                                x['segment'] == option and x['organ_level'] == level and x[
                                                    'area'] == area]
                option_level_area_count = get_proper_count(option_level_area_count_list)
                key = organ_level_map.get(level, '') + "_" + area_map.get(area, '')
                level_area_count_list = [x for x in level_area_count_set if
                                         x['area'] == area and x['organ_level'] == level]
                level_area_count = get_proper_count(level_area_count_list)
                line[key] = get_proper_percent(option_level_area_count, level_area_count)
        stat_line.append(line)
    return stat_line


def extra_rate(qid,tid):
    data = []
    # DevOptions.objects.filter(qid=qid).filter(tid__in=tid_list).all().values('gather_level', 'tid',
    #                                                                               'area').annotate(avg=Avg('options'))
    # for tid in tid_list:
    theme = qid+ '-'+str(tid[0:2])+'-'+str(tid[2:])
    ##print(theme)

    # TODO 获取填报数值的区间进行处理

    def query_option_all():
        return RateTable.objects.filter(theme=theme).filter(gather_level__in=level_list).all()
    ##print(query_option_all().count())
    tmp_level_area_set = query_option_all().values('gather_level', 'area').annotate(avg=Avg('rate'))
    tmp_set = query_option_all().values('theme').annotate(avg=Avg('rate'))
    stat_line = []
    line = {'option': '均值(%)'}
    if len(tmp_set):
        line['sum'] = str(round(float(tmp_set[0].get('avg', 0.0))*100, 1))
    else:
        return stat_line
    for level in level_list:
        tmp_level_area_list = [x for x in tmp_level_area_set if x['gather_level'] == level]
        line[level_map.get(level, '') + "_count"] = '0.0' if not len(tmp_level_area_list) else str(
            round(sum([x['avg'] for x in tmp_level_area_list]) / len(tmp_level_area_list)*100, 1))
        for area in area_list:
            key = level_map.get(level, '') + "_" + area_map.get(area, '')
            tmp_list = [x for x in tmp_level_area_list if len(tmp_level_area_list) and x['area'] == area]
            value = '0.0' if not len(tmp_list) else str(round(float(tmp_list[0].get('avg', 0.0))*100, 1))
            line[key] = value

    stat_line.append(line)
    params =  DevOptionsDescription.objects.filter(qid=qid).filter(tid=tid).values()
    description_queryset = []
    if  len(params):
        description_queryset = params
    else:
        return stat_line
    # description_list = [x['description'] for x in description_queryset if len(description_queryset)]
    description_segment_list = [x['options'].split(';') for x in description_queryset if len(description_queryset)]
    if len(description_segment_list):
        description_segment_list = description_segment_list[0]
    else:
        return stat_line
    ##print(description_segment_list)
    segment_option = []
    segment_option.append((0, description_segment_list[0]))
    for idx, segment in enumerate(description_segment_list[:-1]):
        segment_option.append((segment, description_segment_list[idx + 1]))
    segment_description = []
    segment_description.append('0~' + str(description_segment_list[0]))
    for index, number in enumerate(description_segment_list[:-1]):
        segment_description.append(str(number) + '~' + str(description_segment_list[index + 1]))
    segment_description.append('大于' + str(description_segment_list[-1]))

    def query_option(segment_option, description_segment_list):
        return RateTable.objects.filter(theme=theme).filter(
            gather_level__in=level_list).all().annotate(
            segment=Case(
                *[When(rate__gte=x, rate__lt=y, then=Value(str(x) + '~' + str(y))) for x, y in segment_option],
                default=Value('大于' + str(description_segment_list[-1])),
                output_field=CharField(),
            ),
        )


    level_sum_set = query_option(segment_option, description_segment_list).values('gather_level').annotate(
        count=Count('gather_level'))
    level_area_sum_set = query_option(segment_option, description_segment_list).values('gather_level', 'area').annotate(
        count=Count('area'))
    ##print(level_sum_set, level_area_sum_set)
    count_all = RateTable.objects.filter(theme=theme).filter(gather_level__in=level_list).all().count()
    option_count_set = query_option(segment_option, description_segment_list).values('segment').annotate(
        count=Count('segment'))
    level_count_set = query_option(segment_option, description_segment_list).values('gather_level').annotate(
        count=Count('gather_level'))
    level_area_count_set = query_option(segment_option, description_segment_list).values('gather_level',
                                                                                         'area').annotate(
        count=Count('area'))
    option_level_count_set = query_option(segment_option, description_segment_list).values('gather_level',
                                                                                           'segment').annotate(
        count=Count('segment'))
    option_level_area_count_set = query_option(segment_option, description_segment_list).values('gather_level',
                                                                                                'segment',
                                                                                                'area').annotate(
        count=Count('segment'))
    for option in segment_description:
        line = {'option': option}
        ##print(option_count_set)
        option_count_list = [x for x in option_count_set if x['segment'] == option]
        ##print('---------------------',option_count_list)
        option_count = get_proper_count(option_count_list)
        ##print('count---------------------------------',option_count,count_all)
        line['sum'] = get_proper_percent(option_count, count_all)
        for level in level_list:
            option_level_count_list = [x for x in option_level_count_set if
                                       x['segment'] == option and x['gather_level'] == level]
            option_level_count = get_proper_count(option_level_count_list)
            key = level_map.get(level, '') + "_count"
            level_count_list = [x for x in level_count_set if x['gather_level'] == level]
            level_count = get_proper_count(level_count_list)
            line[key] = get_proper_percent(option_level_count, level_count)
            for area in area_list:
                option_level_area_count_list = [x for x in option_level_area_count_set if
                                                x['segment'] == option and x['gather_level'] == level and x[
                                                    'area'] == area]
                option_level_area_count = get_proper_count(option_level_area_count_list)
                key = level_map.get(level, '') + "_" + area_map.get(area, '')
                level_area_count_list = [x for x in level_area_count_set if
                                         x['area'] == area and x['gather_level'] == level]
                level_area_count = get_proper_count(level_area_count_list)
                line[key] = get_proper_percent(option_level_area_count, level_area_count)
        stat_line.append(line)
    return stat_line
    # x = [0]*17
    # y = [1]*17
    # if '19' in tid_list:
    #     x = [7.6,	10.5,	11.8,	9.6,	10.1,	4.0,	4.8,	3.3,	4.0,	2.1,	1.6,	2.3,	2.4,	2.8,	3.1,2.4	,2.9]
    #     y = [739.9,1073.4,1121.7,1106.3,992.4,356.1,403.0,309.3,355.9,159.9,137.2,79.5,262.9,215.8,199.8,250.5,197.1]
    # if '11' in tid_list:
    #     x = [2320.2,2406.5,1421.0,3304.3,2494.1,1972.3,4445.3,247.6,1223.9,39.2,23.7,30.1,63.7,3742.7,4218.5,3261.0,3748.5]
    #     y = [43916.5,66513.6,85481.8,55325.7,58733.2,14409.1,18170.1,10197.2,14859.9,2051.5,1554.0,1171.9,3428.5,7235.7,8426.4,8934.3,4346.5]
    # key = ['sum','level3_count','level3_east','level3_middle','level3_west','level2_count','level2_east','level2_middle','level2_west','level1_count','level1_east','level1_middle','level1_west','level0_count','level0_east','level0_middle','level0_west']
    # line = {'option':'比例(%)'}
    # for m,n,o in zip(x,y,key):
    #     line[o] = str(round(m*100/n,1))
    # ##print(line)
    # data.append(line)
    # return data


def get_proper_percent(numerator, denominator):
    # #(denominator)
    # #(Decimal(numerator)/Decimal(denominator)*Decimal(100))
    if denominator != 0:
        return str(round(float(Decimal(numerator) / Decimal(denominator) * Decimal(100)), 1))
    else:
        return '0.0'


def get_proper_count_multi(count_list):
    return sum([x.get('count', 0) if len(count_list) else 0 for x in count_list])


def get_proper_count(count_list):
    return count_list[0].get('count', 0) if len(count_list) else 0