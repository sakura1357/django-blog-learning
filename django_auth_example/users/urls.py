# encoding: utf-8

'''
@author: siar
@contact: xzt1357@gmail.com
@file: urls.py
@time: 2017/7/12 13:42
@desc:
'''

from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^$', views.index, name='index'),
]

