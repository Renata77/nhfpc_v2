#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: 齐天亮
@license: Apache Licence  
@contact: qitianliang@outlook.com
@site: https://gitee.com/yongfeng006 
@software: PyCharm 
@file: delete_backend.py 
@time: 2017/11/8 15:32 
"""
from .models import DevOptionsDescription
def delete_description(ids):
    """
    创建option_description中的记录
    :param front_qid: 表格里获取的问卷简称
    :param front_tid: 表格里获取的问题编号
    :param modified_helper: 修改后的description字段
    :return: 修改记录状态
    """
    #print(ids)
    success = {'status': 200}
    failed = {'status': 500}
    back_tid = 0
    # assert isinstance(front_tid,int)
    # TODO delete record
    # record = DevOptionsDescription(qid=front_qid,tid=front_tid,description=new_description,options=";".join(options))
    # record.save()
    # #print(new_description)
    # row = DevOptionsDescription.objects.filter(qid=front_qid).filter(tid=back_tid).save(
    #     description=new_description)
    # #print('update lines', row)
    rows = DevOptionsDescription.objects.filter(id__in=ids).delete()
    #print('del lines',rows)
    if rows != len(ids):
        return failed
    return success