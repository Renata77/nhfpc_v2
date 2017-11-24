#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: 齐天亮
@license: Apache Licence  
@contact: qitianliang@outlook.com
@site: https://gitee.com/yongfeng006 
@software: PyCharm 
@file: process_data.py 
@time: 2017/11/6 21:07 
"""
from script_4_process_data.pretreatment_v2 import get_option
from sqlalchemy import create_engine
from sqlalchemy.types import String, Date, DateTime,Integer,STRINGTYPE
from sqlalchemy.dialects.oracle import \
            BFILE, BLOB, CHAR, CLOB, DATE, \
            DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
            NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
            VARCHAR2
import pandas
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

#create your engine
engine = create_engine('oracle://xjtu_nhfpc:xjtu123@202.117.15.161:15211/XE',encoding='latin1')
conn = engine.connect()
res = conn.execute("select * from XJTU_NHFPC.DEV_RECORD WHERE QUESTIONNAIRE_STATUS = '5' and OPTIONS is not NULL  and OPTIONS != 'undefined'")
df = pandas.read_sql("select * from XJTU_NHFPC.DEV_RECORD WHERE QUESTIONNAIRE_STATUS = '5' and OPTIONS is not NULL  and OPTIONS != 'undefined'",con=conn)
print(df.dtypes)
print(len(df))
# tdf = df[['questionnaire_name','type','organ_name','organ_level','gather_level','province_name']]
d = {
    '医院信息化建设现状调查表（20170303）':'hospital',
    '医疗健康大数据调查问卷表（20170303）':'bigdata',
    '区域人口健康信息化建设调查表（20170303）':'location'
}
def func(x):
    return get_option(x['type'],x['options'],x['unit'])
tdf = pandas.DataFrame()
print(df.head(1))
tdf['qid'] = df['questionnaire_name'].map(lambda x:d[x])
tdf['tid'] = df['test_questions_id'].astype('int')
tdf['p_type'] = df['type'].astype('int8')
tdf['origin_options'] = df['options'].astype(str)
tdf['options'] = df.apply(func,axis=1).astype(str)
tdf['organ_name'] = df['organ_name'].astype(str)
tdf['organ_level'] = df['organ_level'].astype(str)
tdf['gather_level'] = df['gather_level']
tdf['province'] = df['province_name'].astype(str)
tdf['area'] = df['area'].astype(str)
print(tdf.dtypes)
print(len(tdf))
print(tdf.head(1))
tdf.to_pickle('tdf.pkl')
d_type = {'qid':NVARCHAR2(64),'tid':NUMBER(4),'p_type':NUMBER(4),'origin_options':NVARCHAR2(1024),
          'options':NVARCHAR2(1024),'organ_name':NVARCHAR2(64),'organ_level':NVARCHAR2(24),'gather_level':NVARCHAR2(24),
          'province':NVARCHAR2(24),'area':NVARCHAR2(24)

          }

tdf.to_sql("DEV_OPTION",con=conn,if_exists='replace',index_label='id',dtype=d_type)
# tdf.to_sql("DEV_OPTIONS_TEST1",con=conn,if_exists='replace',index_label='id',chunksize=1000)
# print(len(res))
# for x in res:
#     print(x)
#     break