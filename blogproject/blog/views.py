# coding:utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category
import markdown
from blogproject.comments.forms import CommentForm

import sys
sys.path.append('f:\joe\Workspace\/blogproject\comments\/forms.py')
# import forms

# Create your views here.
# 主页视图
def index(request):
    # return HttpResponse("欢迎访问我的博客首页！")
    # return render(request, 'blog/index.html', context={
    #     'title': '我的博客首页',
    #     'welcome': '欢迎访问我的博客首页',
    # })
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 文章详情页视图
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # return render(request, 'blog/detail.html', context={'post': post})
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    # import CommentForm, 新建CommentForm实例对象
    form = CommentForm()
    # 获取这篇post文章下的全部评论
    comment_list = post.comment_set.all()
    # 将post, form, comment_list作为模板变量传给detail.html模板进行渲染
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)


# 归档详情页视图
def archives(request, year, month):
    """
    点击某个归档时间，显示此归档时间下的文章列表
    :param request:
    :param year:
    :param month:
    :return:
    """
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 分类详情页视图
def category(request, pk):
    """
    点击某个分类，显示此分类下的文章列表
    :param request:
    :param pk:
    :return: 此分类下的文章列表
    """
    cate = get_object_or_404(Category, pk=pk)
    # post_list = cate.post_set.all().order_by('-created_time')
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


