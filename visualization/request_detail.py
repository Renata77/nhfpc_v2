#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: 齐天亮
@license: Apache Licence  
@contact: qitianliang@outlook.com
@site: https://gitee.com/yongfeng006 
@software: PyCharm 
@file: request_detail.py
@time: 2017/11/5 20:22 
"""
from .models import DevQuestions,DevOptions,DevOptionsDescription
from collections import defaultdict

def get_detail_question(qid,tid):
    """
    :param qid: 问卷id
    :param tid: 问题id
    :return: 问题详细描述
    """
    data = []
    question = DevQuestions.objects.filter(qid=qid).filter(tid=tid).values()
    for q in question:

        q['options'] = q['options'].replace(';','<br>')
        ##print(q)
        data.append(q)
    # data = [q for q in question]

    return data

def get_detail_answer(qid,tid,p_type):
    """

    :param qid: 问卷id
    :param tid: 问题id
    :return: 答案详细描述
    """
    data = []
    answer = DevOptions.objects.filter(qid=qid).filter(tid=tid).values()
    # TODO 有选项合并，正确输出结果。
    descriptions = get_options_description(qid,tid)
    options_dict = defaultdict(str)
    p_type = str(p_type)
    if len(descriptions)>0:
        #print(descriptions,p_type)
        if p_type in ['1', '2']: #选择题
            #print(descriptions)
            for des in descriptions:
                option = des['options'].split(";")
                for opt in option:
                    options_dict[opt] = des['description']
            for a in answer:
                # TODO 多选题的多个标签
                if "**" in a['options']:#多选题
                    a_options_list = a['options'].split("**")
                    des_list = []
                    for a_option in a_options_list:
                        if options_dict.get(a_option,'null')== 'null':
                            continue
                        elif options_dict.get(a_option,'null') not in des_list:
                            des_list.append(options_dict.get(a_option))
                    if len(des_list)>0:
                        a['options_stat'] = '**'.join(des_list)
                else:#单选题
                    a['options_stat'] = options_dict.get(a['options'],a['options'])
                data.append(a)
            return data
        if p_type in ['3','4','5']: #填空题

            #print(descriptions)
            assert len(descriptions)==1
            interval_list = descriptions[0].get('options','').split(';')
            interval_number_list = []
            for interval in interval_list:
                try:
                    if p_type == '3':
                        interval = int(interval.strip())
                    if p_type in ['4','5']:
                        interval = float(interval.strip())
                except Exception as e:
                    #print('validate the description format',interval)
                    pass
                interval_number_list.append(interval)
            interval_description_group = []

            interval_description_group.append('0~'+str(interval_number_list[0]))
            for index,number in enumerate(interval_number_list[:-1]):
                interval_description_group.append(str(number)+'~'+str(interval_number_list[index+1]))
            if p_type in ['3', '4']:
                interval_description_group.append('大于'+str(interval_number_list[-1]))
            if p_type == '5':
                assert interval_number_list[-1] < 100
                interval_description_group.append(str(interval_number_list[-1])+'~100')
            for a in answer:
                try:
                    float(a.get('options','0.0'))
                except Exception as e:
                    #print(e)
                    pass
                desc_index = get_options_proper_index(float(a.get("options",'0.0')), interval_number_list)
                #print(desc_index,float(a.get("options",'0.0')),a.get("options",'0.0'),interval_number_list)
                a['options_stat'] = interval_description_group[desc_index]
                data.append(a)
            return data
            pass

    else:
        for a in answer:
            a['options_stat'] = a['options']
            data.append(a)
    return data

def get_options_description(qid,tid):
    data = []
    answer = DevOptionsDescription.objects.filter(qid=qid).filter(tid=tid).values()
    for a in answer:
        data.append(a)
    return data

def get_options_proper_index(x,interval_list):
    index = len(interval_list)
    for idx, y in enumerate(interval_list):
        if x < y :
            return idx
    return index

