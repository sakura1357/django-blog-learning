# encoding: utf-8
from django.conf.urls import url
from . import views


'''
@author: siar
@contact: xzt1357@gmail.com
@file: urls.py
@time: 2017/6/28 16:14
@desc:
'''

app_name = 'comments'
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment')
]