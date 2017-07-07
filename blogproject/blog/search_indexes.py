# encoding: utf-8

'''
@author: siar
@contact: xzt1357@gmail.com
@file: search_indexes.py
@time: 2017/7/7 14:36
@desc: 全文检索
'''

from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

