# encoding: utf-8

'''
@author: siar
@contact: xzt1357@gmail.com
@file: urls.py
@time: 2017/6/22 16:36
@desc:
'''

from django.conf.urls import url
from . import views

app_name = 'comment'
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment')
]
