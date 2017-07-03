# encoding: utf-8
from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count
'''
@author: siar
@contact: xzt1357@gmail.com
@file: blog_tags.py
@time: 2017/6/22 10:14
@desc: 自定义模板标签代码
'''
# 使用装饰器，将函数注册为模板标签
register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    """
    最新文章模板标签
    返回最新的5篇文章
    :param num:
    :return:
    """
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    """
    归档模板标签
    返回归档列表，列表中的元素为每个Post的创建时间，按月归档
    且是Python的date对象，精确到月份，降序排列
    date(arg1, arg2, arg3)
    arg1: 创建时间
    arg2: 精度
    arg3: 排序
    :return:
    """
    # print(type(Post.objects.date('created_time', 'month', order='DESC')))
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    """
    分类模板标签
    返回文章分类
    :return:
    """
    # return Category.objects.all()
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
# 统计某一标签下的文章数：
tag_list = Tag.objects.annotate(num_posts=Count('post'))

