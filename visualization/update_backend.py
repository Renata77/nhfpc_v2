#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: 齐天亮
@license: Apache Licence  
@contact: qitianliang@outlook.com
@site: https://gitee.com/yongfeng006 
@software: PyCharm 
@file: update_backend.py 
@time: 2017/11/7 22:18 
"""
from .models import DevQuestions,DevOptions,DevOptionsDescription
def update_options(front_id,modified_options):
    """
    更新answer中的options字段
    :param id: 记录的id
    :param modified_options:修改数据库options
    :return: 修改记录状态
    """
    success={'status':200}
    failed = {'status':500}
    back_id = 0
    try:
        back_id = int(front_id)
    except Exception as e:
        return failed
    if modified_options=='None':
        return failed
    row = DevOptions.objects.filter(id=back_id).update(options = modified_options)
    #print('update lines',row)
    return success


def update_helper(front_qid,front_tid,modified_helper):
    """
    更新question中的helper字段
    :param front_qid: 表格里获取的问卷简称
    :param front_tid: 表格里获取的问题编号
    :param modified_helper: 修改后的helper字段
    :return: 修改记录状态
    """
    success = {'status': 200}
    failed = {'status': 500}
    back_tid = 0
    # assert isinstance(front_tid,int)
    try:
        back_tid = int(front_tid)
    except Exception as e:
        return failed
    if modified_helper == 'None':
        return failed
    assert isinstance(back_tid,int)
    row = DevQuestions.objects.filter(qid=front_qid).filter(tid=back_tid).update(helper=modified_helper)
    ##print('update lines', row)
    return success

def update_description(front_id,modified_description):
    """
    更新option_description中的description字段
    :param front_qid: 表格里获取的问卷简称
    :param front_tid: 表格里获取的问题编号
    :param modified_helper: 修改后的description字段
    :return: 修改记录状态
    """
    success = {'status': 200}
    failed = {'status': 500}
    back_tid = 0
    # assert isinstance(front_tid,int)
    try:
        back_id = int(front_id)
    except Exception as e:
        return failed
    if modified_description == 'None':
        return failed
    assert isinstance(back_tid,int)
    ##print(back_tid,modified_description)
    row = DevOptionsDescription.objects.filter(id=front_id).update(description=modified_description)
    ##print('update lines', row)
    return success

def update_segment(front_id,modified_segment):
    """
    更新option_description中的description字段
    :param front_qid: 表格里获取的问卷简称
    :param front_tid: 表格里获取的问题编号
    :param modified_helper: 修改后的description字段
    :return: 修改记录状态
    """
    success = {'status': 200}
    failed = {'status': 500}
    back_tid = 0
    # assert isinstance(front_tid,int)
    try:
        back_id = int(front_id)
    except Exception as e:
        return failed
    if modified_segment == 'None':
        return failed
    assert isinstance(back_tid,int)
    ##print(back_tid,modified_description)
    row = DevOptionsDescription.objects.filter(id=front_id).update(options=modified_segment)
    #print('update lines', row)
    return success