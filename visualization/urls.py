#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: 齐天亮
@license: Apache Licence  
@contact: qitianliang@outlook.com
@site: https://gitee.com/yongfeng006 
@software: PyCharm 
@file: urls.py 
@time: 2017/11/2 20:37 
"""
from django.conf.urls import url
from django.contrib.auth import views as auth
from . import views

auth.LoginView.extra_context = {'title': '登录'}
auth.LogoutView.extra_context = {'title': '登出'}


urlpatterns = [
    url(r'^login/', auth.LoginView.as_view(template_name='components/login.html'), name="login"),
    url(r'^logout/', auth.LogoutView.as_view(template_name='components/logout.html'), name="logout"),
    url(r'^questionnaires/$', views.questionnaires, name="questionnaires"),
    #TODO 临时的额外表单

    url(r'^extra/$', views.extra, name="extra"),



    url(r'^details/(\w+)/([0-9]+)$', views.detail_question, name='visualization', ),
    url(r'^update_answer_options',views.update_answer_options,name='update_answer_options'),
    url(r'^update_options_description',views.update_options_description,name='update_options_description'),
    url(r'^update_options_segment',views.update_options_segment,name='update_options_segment'),
    url(r'^create_options_description',views.create_options_description,name='create_options_description'),
    url(r'^delete_options_description',views.delete_options_description,name='delete_options_description'),
    url(r'^update_question_helper',views.update_question_helper,name='update_question_helper'),
    url(r'^stat_answer_hospital$',views.stat_answer_hospital,name='stat_answer_hospital'),
    url(r'^stat_answer_health$',views.stat_answer_health,name='stat_answer_health'),
    url(r'^stat_extra_rate$',views.stat_extra_rate,name='stat_extra_rate'),
    url(r'^stat_extra_rate_health$',views.stat_extra_rate_health,name='stat_extra_rate_health'),



#TODO 有时间改一下shit code
url(r'^questionnaires/data$', views.questionnaires_data,name="data"),

    #TODO 测试页面ui
    url(r'^test/',views.test,name='test'),
]