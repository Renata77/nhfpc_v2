#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: 齐天亮
@license: Apache Licence  
@contact: qitianliang@outlook.com
@site: https://gitee.com/yongfeng006 
@software: PyCharm 
@file: request_stat.py 
@time: 2017/11/8 20:56 
"""
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


def type1stat_hospital(params):
    qid = params.get('qid')
    tid = params.get('tid')
    option_list = params.get('options')
    description_queryset = params.get('description', [])
    # (description_queryset)
    description_list = [x['description'] for x in description_queryset if len(description_queryset)]
    description_option_list = [x['options'].split(';') for x in description_queryset if len(description_queryset)]

    # (description_option_list)
    def query_option():
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(gather_level__in=level_list).all()

    def query_description(description_option):
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(gather_level__in=level_list).filter(
            options__in=description_option).all()

    sum_all = query_option().count()
    level_sum_set = query_option().values('gather_level').annotate(count=Count('gather_level'))
    level_area_sum_set = query_option().values('gather_level', 'area').annotate(count=Count('area'))
    # (len(description_list))
    stat_line = []
    has_description = False
    for description, description_option in zip(description_list, description_option_list):
        has_description = True
        count_all = query_description(description_option).count()
        description_count_set = query_description(description_option).values('options').annotate(count=Count('options'))
        level_count_set = query_description(description_option).values('gather_level').annotate(
            count=Count('gather_level'))
        level_area_count_set = query_description(description_option).values('gather_level', 'area').annotate(
            count=Count('area'))
        option_level_count_set = query_description(description_option).values('gather_level', 'options').annotate(
            count=Count('options'))
        option_level_area_count_set = query_description(description_option).values('gather_level', 'options',
                                                                                   'area').annotate(
            count=Count('options'))
        if len(description_option) == 1 and description == description_option[0]:
            line = {'option': description}
        else:
            line = {'option': description + "(" + ';'.join(
                [x[:2] + "..." if len(x) > 4 else x for x in description_option]) + ")"}
            line = {'option': description}
        line['sum'] = get_proper_percent(count_all, sum_all)
        for level in level_list:

            key = level_map.get(level, '') + "_count"
            level_count_list = [x for x in level_count_set if x['gather_level'] == level]
            level_count = get_proper_count(level_count_list)
            level_sum_list = [x for x in level_sum_set if x['gather_level'] == level]
            level_sum = get_proper_count(level_sum_list)
            line[key] = get_proper_percent(level_count, level_sum)
            for area in area_list:
                key = level_map.get(level, '') + "_" + area_map.get(area, '')
                level_area_count_list = [x for x in level_area_count_set if
                                         x['area'] == area and x['gather_level'] == level]
                level_area_count = get_proper_count(level_area_count_list)
                level_area_sum_list = [x for x in level_area_sum_set if
                                       x['area'] == area and x['gather_level'] == level]
                level_area_sum = get_proper_count(level_area_sum_list)
                line[key] = get_proper_percent(level_area_count, level_area_sum)

        stat_line.append(line)
        if len(description_option) == 1 and description == description_option[0]:
            continue
        for option in description_option:
            line = {'option': option}
            option_count_list = [x for x in description_count_set if x['options'] == option]
            option_count = get_proper_count(option_count_list)
            line['sum'] = get_proper_percent(option_count, count_all)
            for level in level_list:
                option_level_count_list = [x for x in option_level_count_set if
                                           x['options'] == option and x['gather_level'] == level]
                option_level_count = get_proper_count(option_level_count_list)
                key = level_map.get(level, '') + "_count"
                level_count_list = [x for x in level_count_set if x['gather_level'] == level]
                level_count = get_proper_count(level_count_list)
                line[key] = get_proper_percent(option_level_count, level_count)
                for area in area_list:
                    option_level_area_count_list = [x for x in option_level_area_count_set if
                                                    x['options'] == option and x['gather_level'] == level and x[
                                                        'area'] == area]
                    option_level_area_count = get_proper_count(option_level_area_count_list)
                    key = level_map.get(level, '') + "_" + area_map.get(area, '')
                    level_area_count_list = [x for x in level_area_count_set if
                                             x['area'] == area and x['gather_level'] == level]
                    level_area_count = get_proper_count(level_area_count_list)
                    line[key] = get_proper_percent(option_level_area_count, level_area_count)
            stat_line.append(line)
    if has_description:
        return stat_line
    stat_line = []
    count_all = query_option().count()
    option_count_set = query_option().values('options').annotate(count=Count('options'))
    level_count_set = query_option().values('gather_level').annotate(count=Count('gather_level'))
    level_area_count_set = query_option().values('gather_level', 'area').annotate(count=Count('area'))
    option_level_count_set = query_option().values('gather_level', 'options').annotate(count=Count('options'))
    option_level_area_count_set = query_option().values('gather_level', 'options', 'area').annotate(
        count=Count('options'))
    for option in option_list:
        line = {'option': option}
        option_count_list = [x for x in option_count_set if x['options'] == option]
        option_count = get_proper_count(option_count_list)
        line['sum'] = get_proper_percent(option_count, count_all)
        for level in level_list:
            option_level_count_list = [x for x in option_level_count_set if
                                       x['options'] == option and x['gather_level'] == level]
            option_level_count = get_proper_count(option_level_count_list)
            key = level_map.get(level, '') + "_count"
            level_count_list = [x for x in level_count_set if x['gather_level'] == level]
            level_count = get_proper_count(level_count_list)
            line[key] = get_proper_percent(option_level_count, level_count)
            for area in area_list:
                option_level_area_count_list = [x for x in option_level_area_count_set if
                                                x['options'] == option and x['gather_level'] == level and x[
                                                    'area'] == area]
                option_level_area_count = get_proper_count(option_level_area_count_list)
                key = level_map.get(level, '') + "_" + area_map.get(area, '')
                level_area_count_list = [x for x in level_area_count_set if
                                         x['area'] == area and x['gather_level'] == level]
                level_area_count = get_proper_count(level_area_count_list)
                line[key] = get_proper_percent(option_level_area_count, level_area_count)
        stat_line.append(line)
    return stat_line


def type2stat_hospital(params):
    qid = params.get('qid')
    tid = params.get('tid')
    option_list = params.get('options')
    # (option_list)
    description_queryset = params.get('description', [])
    # (description_queryset)
    description_list = [x['description'] for x in description_queryset if len(description_queryset)]
    description_option_list = [x['options'].split(';') for x in description_queryset if len(description_queryset)]

    # (description_option_list)

    def query_option():
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(gather_level__isnull=False).all()

    def query_description(description_option):
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(gather_level__isnull=False).filter(
            reduce(lambda x, y: x | y, [Q(options__contains=item + "**") for item in description_option])).all()

    sum_all = query_option().count()
    level_sum_set = query_option().values('gather_level').annotate(count=Count('gather_level'))
    level_area_sum_set = query_option().values('gather_level', 'area').annotate(count=Count('area'))
    # (len(description_list))
    stat_line = []
    has_description = False
    for description, description_option in zip(description_list, description_option_list):
        has_description = True
        count_all = query_description(description_option).count()

        description_count_set = query_description(description_option).values('options').annotate(count=Count('options'))
        level_count_set = query_description(description_option).values('gather_level').annotate(
            count=Count('gather_level'))
        level_area_count_set = query_description(description_option).values('gather_level', 'area').annotate(
            count=Count('area'))
        option_level_count_set = query_description(description_option).values('gather_level', 'options').annotate(
            count=Count('options'))
        option_level_area_count_set = query_description(description_option).values('gather_level', 'options',
                                                                                   'area').annotate(
            count=Count('options'))
        if len(description_option) == 1 and description == description_option[0]:
            line = {'option': description}
        else:
            line = {'option': description + "(" + ';'.join(
                [x[:2] + "..." if len(x) > 4 else x for x in description_option]) + ")"}
            line = {'option': description}
        line['sum'] = get_proper_percent(count_all, sum_all)
        for level in level_list:

            key = level_map.get(level, '') + "_count"
            level_count_list = [x for x in level_count_set if x['gather_level'] == level]
            level_count = get_proper_count_multi(level_count_list)
            level_sum_list = [x for x in level_sum_set if x['gather_level'] == level]
            level_sum = get_proper_count_multi(level_sum_list)
            line[key] = get_proper_percent(level_count, level_sum)
            for area in area_list:
                key = level_map.get(level, '') + "_" + area_map.get(area, '')
                level_area_count_list = [x for x in level_area_count_set if
                                         x['area'] == area and x['gather_level'] == level]
                level_area_count = get_proper_count_multi(level_area_count_list)
                level_area_sum_list = [x for x in level_area_sum_set if
                                       x['area'] == area and x['gather_level'] == level]
                level_area_sum = get_proper_count_multi(level_area_sum_list)
                line[key] = get_proper_percent(level_area_count, level_area_sum)

        stat_line.append(line)
        if len(description_option) == 1 and description == description_option[0]:
            continue
        for option in description_option:
            line = {'option': option}
            option_count_list = [x for x in description_count_set if option in x['options']]
            option_count = get_proper_count_multi(option_count_list)
            line['sum'] = get_proper_percent(option_count, count_all)
            for level in level_list:
                option_level_count_list = [x for x in option_level_count_set if
                                           option in x['options'] and x['gather_level'] == level]
                option_level_count = get_proper_count_multi(option_level_count_list)
                key = level_map.get(level, '') + "_count"
                level_count_list = [x for x in level_count_set if x['gather_level'] == level]
                level_count = get_proper_count_multi(level_count_list)
                line[key] = get_proper_percent(option_level_count, level_count)
                for area in area_list:
                    option_level_area_count_list = [x for x in option_level_area_count_set if
                                                    option in x['options'] and x['gather_level'] == level and x[
                                                        'area'] == area]
                    option_level_area_count = get_proper_count_multi(option_level_area_count_list)
                    key = level_map.get(level, '') + "_" + area_map.get(area, '')
                    level_area_count_list = [x for x in level_area_count_set if
                                             x['area'] == area and x['gather_level'] == level]
                    level_area_count = get_proper_count_multi(level_area_count_list)
                    line[key] = get_proper_percent(option_level_area_count, level_area_count)
            stat_line.append(line)
    if has_description:
        return stat_line
    stat_line = []
    count_all = query_option().count()
    # ('without description',count_all)
    option_count_set = query_option().values('options').annotate(count=Count('options'))
    level_count_set = query_option().values('gather_level').annotate(count=Count('gather_level'))
    level_area_count_set = query_option().values('gather_level', 'area').annotate(count=Count('area'))
    option_level_count_set = query_option().values('gather_level', 'options').annotate(count=Count('options'))
    option_level_area_count_set = query_option().values('gather_level', 'options', 'area').annotate(
        count=Count('options'))
    for option in option_list:
        line = {'option': option}
        option_count_list = [x for x in option_count_set if option in x['options']]
        option_count = get_proper_count_multi(option_count_list)
        line['sum'] = get_proper_percent(option_count, count_all)
        for level in level_list:
            option_level_count_list = [x for x in option_level_count_set if
                                       option in x['options'] and x['gather_level'] == level]
            option_level_count = get_proper_count_multi(option_level_count_list)
            key = level_map.get(level, '') + "_count"
            level_count_list = [x for x in level_count_set if x['gather_level'] == level]
            level_count = get_proper_count_multi(level_count_list)
            line[key] = get_proper_percent(option_level_count, level_count)
            for area in area_list:
                option_level_area_count_list = [x for x in option_level_area_count_set if
                                                option in x['options'] and x['gather_level'] == level and x[
                                                    'area'] == area]
                option_level_area_count = get_proper_count_multi(option_level_area_count_list)
                key = level_map.get(level, '') + "_" + area_map.get(area, '')
                level_area_count_list = [x for x in level_area_count_set if
                                         x['area'] == area and x['gather_level'] == level]
                level_area_count = get_proper_count_multi(level_area_count_list)
                # #(level_area_count)
                line[key] = get_proper_percent(option_level_area_count, level_area_count)
        stat_line.append(line)
    return stat_line


def type3stat_hospital(params):
    # TODO 临时造出个均值
    qid = params.get('qid')
    tid = params.get('tid')

    # TODO 获取填报数值的区间进行处理


    def query_option():
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(gather_level__isnull=False).all()

    tmp_level_area_set = query_option().values('gather_level', 'area').annotate(avg=Avg('options'))
    tmp_set = query_option().values('options').annotate(avg=Avg('options'))
    stat_line = []
    line = {'option': '均值'}
    if len(tmp_set):
        line['sum'] = str(round(float(tmp_set[0].get('avg', 0.0)), 1))
    else:
        return stat_line
    for level in level_list:
        tmp_level_area_list = [x for x in tmp_level_area_set if x['gather_level'] == level]

        line[level_map.get(level, '') + "_count"] = '0.0' if not len(tmp_level_area_list) else str(
            round(sum([x['avg'] for x in tmp_level_area_list]) / len(tmp_level_area_list), 1))
        for area in area_list:
            key = level_map.get(level, '') + "_" + area_map.get(area, '')
            tmp_list = [x for x in tmp_level_area_list if len(tmp_level_area_list) and x['area'] == area]
            value = '0.0' if not len(tmp_list) else str(round(float(tmp_list[0].get('avg', 0.0)), 1))
            line[key] = value

    stat_line.append(line)

    description_queryset = params.get('description', [])
    # description_list = [x['description'] for x in description_queryset if len(description_queryset)]
    description_segment_list = [x['options'].split(';') for x in description_queryset if len(description_queryset)]
    if len(description_segment_list):
        description_segment_list = description_segment_list[0]
    else:
        return stat_line
    #print(description_segment_list)
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
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(
            gather_level__in=level_list).all().annotate(
            segment=Case(
                *[When(options__gte=x, options__lt=y, then=Value(str(x) + '~' + str(y))) for x, y in segment_option],
                default=Value('大于' + str(description_segment_list[-1])),
                output_field=CharField(),
            ),
        )

    def query_description(description_option):
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(organ_level__in=level_list).filter(
            options__in=description_option).all()

    level_sum_set = query_option(segment_option,description_segment_list).values('gather_level').annotate(count=Count('gather_level'))
    level_area_sum_set = query_option(segment_option,description_segment_list).values('gather_level', 'area').annotate(count=Count('area'))
    #print(level_sum_set,level_area_sum_set)
    count_all = query_option(segment_option,description_segment_list).count()
    option_count_set = query_option(segment_option,description_segment_list).values('segment').annotate(count=Count('segment'))
    level_count_set = query_option(segment_option,description_segment_list).values('gather_level').annotate(count=Count('gather_level'))
    level_area_count_set = query_option(segment_option,description_segment_list).values('gather_level', 'area').annotate(count=Count('area'))
    option_level_count_set = query_option(segment_option,description_segment_list).values('gather_level', 'segment').annotate(count=Count('segment'))
    option_level_area_count_set = query_option(segment_option,description_segment_list).values('gather_level', 'segment', 'area').annotate(
        count=Count('segment'))
    for option in segment_description:
        line = {'option': option}
        #print(option_count_set)
        option_count_list = [x for x in option_count_set if x['segment'] == option]
        #print(option_count_list)
        option_count = get_proper_count(option_count_list)
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

    pass


def type4stat_hospital(params):
    return type3stat_hospital(params)
    pass


def type5stat_hospital(params):
    pass


def type6stat_hospital(params):
    pass


def type7stat_hospital(params):
    pass


def type9stat_hospital(params):
    pass


map_hospital_function = {
    '0': type9stat_hospital,
    '1': type1stat_hospital,
    '2': type2stat_hospital,
    '3': type3stat_hospital,
    '4': type4stat_hospital,
    '5': type5stat_hospital,
    '6': type6stat_hospital,
    '7': type7stat_hospital,
    '8': type7stat_hospital,
    '9': type9stat_hospital,
}


def type0stat_health(params):
    pass


def type1stat_health(params):
    qid = params.get('qid')
    tid = params.get('tid')
    option_list = params.get('options')
    description_queryset = params.get('description', [])
    # (description_queryset)
    description_list = [x['description'] for x in description_queryset if len(description_queryset)]
    description_option_list = [x['options'].split(';') for x in description_queryset if len(description_queryset)]

    # (description_option_list)
    def query_option():
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(organ_level__in=organ_level_list).all()

    def query_description(description_option):
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(organ_level__in=organ_level_list).filter(
            options__in=description_option).all()

    sum_all = query_option().count()
    level_sum_set = query_option().values('organ_level').annotate(count=Count('organ_level'))
    level_area_sum_set = query_option().values('organ_level', 'area').annotate(count=Count('area'))
    # (len(description_list))
    stat_line = []
    has_description = False
    for description, description_option in zip(description_list, description_option_list):
        has_description = True
        count_all = query_description(description_option).count()
        description_count_set = query_description(description_option).values('options').annotate(count=Count('options'))
        level_count_set = query_description(description_option).values('organ_level').annotate(
            count=Count('organ_level'))
        level_area_count_set = query_description(description_option).values('organ_level', 'area').annotate(
            count=Count('area'))
        option_level_count_set = query_description(description_option).values('organ_level', 'options').annotate(
            count=Count('options'))
        option_level_area_count_set = query_description(description_option).values('organ_level', 'options',
                                                                                   'area').annotate(
            count=Count('options'))
        if len(description_option) == 1 and description == description_option[0]:
            line = {'option': description}
        else:
            line = {'option': description + "(" + ';'.join(
                [x[:2] + "..." if len(x) > 4 else x for x in description_option]) + ")"}
            line = {'option': description}
        line['sum'] = get_proper_percent(count_all, sum_all)
        for level in organ_level_list:

            key = organ_level_map.get(level, '') + "_count"
            level_count_list = [x for x in level_count_set if x['organ_level'] == level]
            level_count = get_proper_count(level_count_list)
            level_sum_list = [x for x in level_sum_set if x['organ_level'] == level]
            level_sum = get_proper_count(level_sum_list)
            line[key] = get_proper_percent(level_count, level_sum)
            for area in area_list:
                key = organ_level_map.get(level, '') + "_" + area_map.get(area, '')
                level_area_count_list = [x for x in level_area_count_set if
                                         x['area'] == area and x['organ_level'] == level]
                level_area_count = get_proper_count(level_area_count_list)
                level_area_sum_list = [x for x in level_area_sum_set if
                                       x['area'] == area and x['organ_level'] == level]
                level_area_sum = get_proper_count(level_area_sum_list)
                line[key] = get_proper_percent(level_area_count, level_area_sum)

        stat_line.append(line)
        if len(description_option) == 1 and description == description_option[0]:
            continue
        for option in description_option:
            line = {'option': option}
            option_count_list = [x for x in description_count_set if x['options'] == option]
            option_count = get_proper_count(option_count_list)
            line['sum'] = get_proper_percent(option_count, count_all)
            for level in organ_level_list:
                option_level_count_list = [x for x in option_level_count_set if
                                           x['options'] == option and x['organ_level'] == level]
                option_level_count = get_proper_count(option_level_count_list)
                key = organ_level_map.get(level, '') + "_count"
                level_count_list = [x for x in level_count_set if x['organ_level'] == level]
                level_count = get_proper_count(level_count_list)
                line[key] = get_proper_percent(option_level_count, level_count)
                for area in area_list:
                    option_level_area_count_list = [x for x in option_level_area_count_set if
                                                    x['options'] == option and x['organ_level'] == level and x[
                                                        'area'] == area]
                    option_level_area_count = get_proper_count(option_level_area_count_list)
                    key = organ_level_map.get(level, '') + "_" + area_map.get(area, '')
                    level_area_count_list = [x for x in level_area_count_set if
                                             x['area'] == area and x['organ_level'] == level]
                    level_area_count = get_proper_count(level_area_count_list)
                    line[key] = get_proper_percent(option_level_area_count, level_area_count)
            stat_line.append(line)
    if has_description:
        return stat_line
    stat_line = []
    count_all = query_option().count()
    option_count_set = query_option().values('options').annotate(count=Count('options'))
    level_count_set = query_option().values('organ_level').annotate(count=Count('organ_level'))
    level_area_count_set = query_option().values('organ_level', 'area').annotate(count=Count('area'))
    option_level_count_set = query_option().values('organ_level', 'options').annotate(count=Count('options'))
    option_level_area_count_set = query_option().values('organ_level', 'options', 'area').annotate(
        count=Count('options'))
    for option in option_list:
        line = {'option': option}
        option_count_list = [x for x in option_count_set if x['options'] == option]
        option_count = get_proper_count(option_count_list)
        line['sum'] = get_proper_percent(option_count, count_all)
        for level in organ_level_list:
            option_level_count_list = [x for x in option_level_count_set if
                                       x['options'] == option and x['organ_level'] == level]
            option_level_count = get_proper_count(option_level_count_list)
            key = organ_level_map.get(level, '') + "_count"
            level_count_list = [x for x in level_count_set if x['organ_level'] == level]
            level_count = get_proper_count(level_count_list)
            line[key] = get_proper_percent(option_level_count, level_count)
            for area in area_list:
                option_level_area_count_list = [x for x in option_level_area_count_set if
                                                x['options'] == option and x['organ_level'] == level and x[
                                                    'area'] == area]
                option_level_area_count = get_proper_count(option_level_area_count_list)
                key = organ_level_map.get(level, '') + "_" + area_map.get(area, '')
                level_area_count_list = [x for x in level_area_count_set if
                                         x['area'] == area and x['organ_level'] == level]
                level_area_count = get_proper_count(level_area_count_list)
                line[key] = get_proper_percent(option_level_area_count, level_area_count)
        stat_line.append(line)
    return stat_line
    pass


def type2stat_health(params):
    qid = params.get('qid')
    tid = params.get('tid')
    option_list = params.get('options')
    # (option_list)
    description_queryset = params.get('description', [])
    # (description_queryset)
    description_list = [x['description'] for x in description_queryset if len(description_queryset)]
    description_option_list = [x['options'].split(';') for x in description_queryset if len(description_queryset)]

    # (description_option_list)

    def query_option():
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(organ_level__in=organ_level_list).all()

    def query_description(description_option):
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(organ_level__in=organ_level_list).filter(
            reduce(lambda x, y: x | y, [Q(options__contains=item + "**") for item in description_option])).all()

    sum_all = query_option().count()
    level_sum_set = query_option().values('organ_level').annotate(count=Count('organ_level'))
    level_area_sum_set = query_option().values('organ_level', 'area').annotate(count=Count('area'))
    # (len(description_list))
    stat_line = []
    has_description = False
    for description, description_option in zip(description_list, description_option_list):
        has_description = True
        count_all = query_description(description_option).count()

        description_count_set = query_description(description_option).values('options').annotate(count=Count('options'))
        level_count_set = query_description(description_option).values('organ_level').annotate(
            count=Count('organ_level'))
        level_area_count_set = query_description(description_option).values('organ_level', 'area').annotate(
            count=Count('area'))
        option_level_count_set = query_description(description_option).values('organ_level', 'options').annotate(
            count=Count('options'))
        option_level_area_count_set = query_description(description_option).values('organ_level', 'options',
                                                                                   'area').annotate(
            count=Count('options'))
        if len(description_option) == 1 and description == description_option[0]:
            line = {'option': description}
        else:
            line = {'option': description + "(" + ';'.join(
                [x[:2] + "..." if len(x) > 4 else x for x in description_option]) + ")"}
            line = {'option': description}
        line['sum'] = get_proper_percent(count_all, sum_all)
        for level in organ_level_list:

            key = organ_level_map.get(level, '') + "_count"
            level_count_list = [x for x in level_count_set if x['organ_level'] == level]
            level_count = get_proper_count_multi(level_count_list)
            level_sum_list = [x for x in level_sum_set if x['organ_level'] == level]
            level_sum = get_proper_count_multi(level_sum_list)
            line[key] = get_proper_percent(level_count, level_sum)
            for area in area_list:
                key = organ_level_map.get(level, '') + "_" + area_map.get(area, '')
                level_area_count_list = [x for x in level_area_count_set if
                                         x['area'] == area and x['organ_level'] == level]
                level_area_count = get_proper_count_multi(level_area_count_list)
                level_area_sum_list = [x for x in level_area_sum_set if
                                       x['area'] == area and x['organ_level'] == level]
                level_area_sum = get_proper_count_multi(level_area_sum_list)
                line[key] = get_proper_percent(level_area_count, level_area_sum)

        stat_line.append(line)
        if len(description_option) == 1 and description == description_option[0]:
            continue
        for option in description_option:
            line = {'option': option}
            option_count_list = [x for x in description_count_set if option in x['options']]
            option_count = get_proper_count_multi(option_count_list)
            line['sum'] = get_proper_percent(option_count, count_all)
            for level in organ_level_list:
                option_level_count_list = [x for x in option_level_count_set if
                                           option in x['options'] and x['organ_level'] == level]
                option_level_count = get_proper_count_multi(option_level_count_list)
                key = organ_level_map.get(level, '') + "_count"
                level_count_list = [x for x in level_count_set if x['organ_level'] == level]
                level_count = get_proper_count_multi(level_count_list)
                line[key] = get_proper_percent(option_level_count, level_count)
                for area in area_list:
                    option_level_area_count_list = [x for x in option_level_area_count_set if
                                                    option in x['options'] and x['organ_level'] == level and x[
                                                        'area'] == area]
                    option_level_area_count = get_proper_count_multi(option_level_area_count_list)
                    key = organ_level_map.get(level, '') + "_" + area_map.get(area, '')
                    level_area_count_list = [x for x in level_area_count_set if
                                             x['area'] == area and x['organ_level'] == level]
                    level_area_count = get_proper_count_multi(level_area_count_list)
                    line[key] = get_proper_percent(option_level_area_count, level_area_count)
            stat_line.append(line)
    if has_description:
        return stat_line
    stat_line = []
    count_all = query_option().count()
    # ('without description',count_all)
    option_count_set = query_option().values('options').annotate(count=Count('options'))
    level_count_set = query_option().values('organ_level').annotate(count=Count('organ_level'))
    level_area_count_set = query_option().values('organ_level', 'area').annotate(count=Count('area'))
    option_level_count_set = query_option().values('organ_level', 'options').annotate(count=Count('options'))
    option_level_area_count_set = query_option().values('organ_level', 'options', 'area').annotate(
        count=Count('options'))
    for option in option_list:
        line = {'option': option}
        option_count_list = [x for x in option_count_set if option in x['options']]
        option_count = get_proper_count_multi(option_count_list)
        line['sum'] = get_proper_percent(option_count, count_all)
        for level in organ_level_list:
            option_level_count_list = [x for x in option_level_count_set if
                                       option in x['options'] and x['organ_level'] == level]
            option_level_count = get_proper_count_multi(option_level_count_list)
            key = organ_level_map.get(level, '') + "_count"
            level_count_list = [x for x in level_count_set if x['organ_level'] == level]
            level_count = get_proper_count_multi(level_count_list)
            line[key] = get_proper_percent(option_level_count, level_count)
            for area in area_list:
                option_level_area_count_list = [x for x in option_level_area_count_set if
                                                option in x['options'] and x['organ_level'] == level and x[
                                                    'area'] == area]
                option_level_area_count = get_proper_count_multi(option_level_area_count_list)
                key = organ_level_map.get(level, '') + "_" + area_map.get(area, '')
                level_area_count_list = [x for x in level_area_count_set if
                                         x['area'] == area and x['organ_level'] == level]
                level_area_count = get_proper_count_multi(level_area_count_list)
                # #(level_area_count)
                line[key] = get_proper_percent(option_level_area_count, level_area_count)
        stat_line.append(line)
    return stat_line
    pass


def type3stat_health(params):
    qid = params.get('qid')
    tid = params.get('tid')

    # TODO 获取填报数值的区间进行处理


    def query_option():
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(organ_level__in=organ_level_list).all()

    tmp_level_area_set = query_option().values('organ_level', 'area').annotate(avg=Avg('options'))
    tmp_set = query_option().values('options').annotate(avg=Avg('options'))
    stat_line = []
    line = {'option': '均值'}
    if len(tmp_set):
        line['sum'] = str(round(float(tmp_set[0].get('avg', 0.0)), 1))
    else:
        return stat_line
    for level in organ_level_list:
        tmp_level_area_list = [x for x in tmp_level_area_set if x['organ_level'] == level]

        line[organ_level_map.get(level, '') + "_count"] = '0.0' if not len(tmp_level_area_list) else str(
            round(sum([x['avg'] for x in tmp_level_area_list]) / len(tmp_level_area_list), 1))
        for area in area_list:
            key = organ_level_map.get(level, '') + "_" + area_map.get(area, '')
            tmp_list = [x for x in tmp_level_area_list if len(tmp_level_area_list) and x['area'] == area]
            value = '0.0' if not len(tmp_list) else str(round(float(tmp_list[0].get('avg', 0.0)), 1))
            line[key] = value

    stat_line.append(line)

    description_queryset = params.get('description', [])
    description_segment_list = [x['options'].split(';') for x in description_queryset if len(description_queryset)]
    if len(description_segment_list):
        description_segment_list = description_segment_list[0]
    else:
        return stat_line
    #print(description_segment_list)
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
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(
            organ_level__in=organ_level_list).all().annotate(
            segment=Case(
                *[When(options__gte=x, options__lt=y, then=Value(str(x) + '~' + str(y))) for x, y in segment_option],
                default=Value('大于' + str(description_segment_list[-1])),
                output_field=CharField(),
            ),
        )

    def query_description(description_option):
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(organ_level__in=organ_level_list).filter(
            options__in=description_option).all()

    level_sum_set = query_option(segment_option, description_segment_list).values('organ_level').annotate(
        count=Count('organ_level'))
    level_area_sum_set = query_option(segment_option, description_segment_list).values('organ_level', 'area').annotate(
        count=Count('area'))
    #print(level_sum_set, level_area_sum_set)
    count_all = query_option(segment_option, description_segment_list).count()
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
        #print(option_count_set)
        option_count_list = [x for x in option_count_set if x['segment'] == option]
        #print(option_count_list)
        option_count = get_proper_count(option_count_list)
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


def type4stat_health(params):
    return type3stat_health(params)
    pass


def type5stat_health(params):
    qid = params.get('qid')
    tid = params.get('tid')

    # TODO 获取填报数值的区间进行处理


    def query_option():
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(organ_level__in=organ_level_list).all()

    tmp_level_area_set = query_option().values('organ_level', 'area').annotate(avg=Avg('options'))
    tmp_set = query_option().values('options').annotate(avg=Avg('options'))
    stat_line = []
    line = {'option': '均值'}
    if len(tmp_set):
        line['sum'] = str(round(float(tmp_set[0].get('avg', 0.0)), 1))
    else:
        return stat_line
    for level in organ_level_list:
        tmp_level_area_list = [x for x in tmp_level_area_set if x['organ_level'] == level]

        line[organ_level_map.get(level, '') + "_count"] = '0.0' if not len(tmp_level_area_list) else str(
            round(sum([x['avg'] for x in tmp_level_area_list]) / len(tmp_level_area_list), 1))
        for area in area_list:
            key = organ_level_map.get(level, '') + "_" + area_map.get(area, '')
            tmp_list = [x for x in tmp_level_area_list if len(tmp_level_area_list) and x['area'] == area]
            value = '0.0' if not len(tmp_list) else str(round(float(tmp_list[0].get('avg', 0.0)), 1))
            line[key] = value

    stat_line.append(line)

    description_queryset = params.get('description', [])
    description_segment_list = [x['options'].split(';') for x in description_queryset if len(description_queryset)]
    if len(description_segment_list):
        description_segment_list = description_segment_list[0]
    else:
        return stat_line
    #print(description_segment_list)
    segment_option = []
    segment_option.append((0, description_segment_list[0]))
    for idx, segment in enumerate(description_segment_list[:-1]):
        segment_option.append((segment, description_segment_list[idx + 1]))
    segment_description = []
    segment_description.append('0~' + str(description_segment_list[0]))
    for index, number in enumerate(description_segment_list[:-1]):
        segment_description.append(str(number) + '~' + str(description_segment_list[index + 1]))
    segment_description.append(str(description_segment_list[-1])+'~100')

    def query_option(segment_option, description_segment_list):
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(
            organ_level__in=organ_level_list).all().annotate(
            segment=Case(
                *[When(options__gte=x, options__lt=y, then=Value(str(x) + '~' + str(y))) for x, y in segment_option],
                default=Value(str(description_segment_list[-1])+'~100'),
                output_field=CharField(),
            ),
        )

    def query_description(description_option):
        return DevOptions.objects.filter(qid=qid).filter(tid=tid).filter(organ_level__in=organ_level_list).filter(
            options__in=description_option).all()

    level_sum_set = query_option(segment_option, description_segment_list).values('organ_level').annotate(
        count=Count('organ_level'))
    level_area_sum_set = query_option(segment_option, description_segment_list).values('organ_level', 'area').annotate(
        count=Count('area'))
    #print(level_sum_set, level_area_sum_set)
    count_all = query_option(segment_option, description_segment_list).count()
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
        #print(option_count_set)
        option_count_list = [x for x in option_count_set if x['segment'] == option]
        #print(option_count_list)
        option_count = get_proper_count(option_count_list)
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
    pass


def type6stat_health(params):
    pass


def type7stat_health(params):
    pass


def type8stat_health(params):
    pass


def type9stat_health(params):
    pass


map_health_function = {
    '0': type0stat_health,
    '1': type1stat_health,
    '2': type2stat_health,
    '3': type3stat_health,
    '4': type4stat_health,
    '5': type5stat_health,
    '6': type6stat_health,
    '7': type7stat_health,
    '8': type7stat_health,
    '9': type9stat_health,
}


def stat_hospital(front_qid, front_tid, front_type):
    #print(front_qid, front_tid, front_type)
    data = []
    try:
        back_tid = int(front_tid)
        back_type = int(front_type)
    except Exception as e:
        return data

    option_list = DevQuestions.objects.filter(qid=front_qid).filter(tid=back_tid).values()[0].get("options", "").split(
        ";")

    description = check_description(front_qid, back_tid)
    params = {
        'qid': front_qid,
        'tid': back_tid,
        'options': option_list,
        'description': description,
    }

    data = map_hospital_function.get(front_type)(params)
    return data


def stat_health(front_qid, front_tid, front_type):
    #print(front_qid, front_tid, front_type)
    data = []
    try:
        back_tid = int(front_tid)
        back_type = int(front_type)
    except Exception as e:
        return data
    option_list = DevQuestions.objects.filter(qid=front_qid).filter(tid=back_tid).values()[0].get("options", "").split(
        ";")

    description = check_description(front_qid, back_tid)
    params = {
        'qid': front_qid,
        'tid': back_tid,
        'options': option_list,
        'description': description,
    }

    data = map_health_function.get(front_type)(params)
    return data


def check_description(qid, tid):
    rows = DevOptionsDescription.objects.filter(qid=qid).filter(tid=tid).values()
    if len(rows) > 0:
        return rows
    else:
        return []


def get_proper_table(type):
    if type == 1:
        return HospAllChoiceStat
    if type == 2:
        return HospAllMultiStat
    else:
        return DevPaper


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
