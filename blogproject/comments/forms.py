# encoding: utf-8
from django import forms
from .models import Comment

'''
@author: siar
@contact: xzt1357@gmail.com
@file: forms.py
@time: 2017/6/22 14:41
@desc: CommentForm评论表单类，需集成Django的forms.Form类或者forms.ModelForm类
'''


class CommentForm(forms.ModelForm):
    """
    使用内部类指定表单相关的东西，
    model=Comment表面这个表单对应的数据库模型是Comment类
    fields指定表单需要显示的字段
    """
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
