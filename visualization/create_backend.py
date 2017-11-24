#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: 齐天亮
@license: Apache Licence  
@contact: qitianliang@outlook.com
@site: https://gitee.com/yongfeng006 
@software: PyCharm 
@file: create_backend.py 
@time: 2017/11/7 23:26 
"""
from .models import DevOptionsDescription
def create_description(front_qid,front_tid,new_description,options):
    """
    创建option_description中的记录
    :param front_qid: 表格里获取的问卷简称
    :param front_tid: 表格里获取的问题编号
    :param modified_helper: 修改后的description字段
    :return: 修改记录状态
    """
    #print(front_qid,front_tid,new_description,options)
    success = {'status': 200}
    failed = {'status': 500}
    back_tid = 0
    # assert isinstance(front_tid,int)
    try:
        back_tid = int(front_tid)
    except Exception as e:
        return failed
    if new_description == 'None':
        return failed
    assert isinstance(back_tid, int)
    # TODO save record
    if isinstance(options,list):
        record = DevOptionsDescription(qid=front_qid,tid=front_tid,description=new_description,options=";".join(options))
    else:
        record = DevOptionsDescription(qid=front_qid,tid=front_tid,description=new_description,options=options)
    record.save()
    # #print(new_description)
    # row = DevOptionsDescription.objects.filter(qid=front_qid).filter(tid=back_tid).save(
    #     description=new_description)
    # #print('update lines', row)
    return success