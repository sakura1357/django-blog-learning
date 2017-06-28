# encoding: utf-8
from django import forms
from .models import Comment

'''
@author: siar
@contact: xzt1357@gmail.com
@file: forms.py
@time: 2017/6/27 15:19
@desc:
'''

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

