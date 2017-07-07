# coding:utf-8
from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Post, Category, Tag
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q


# Create your views here.
# 主页视图
def index(request):
    # return HttpResponse("欢迎访问我的博客首页！")
    # return render(request, 'blog/index.html', context={
    #     'title': '我的博客首页',
    #     'welcome': '欢迎访问我的博客首页',
    # })
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 类视图中,ListView已经做好了分页逻辑,我们只需指定paginate_by属性来开启分页功能即可
# 使用类视图IndexView替代视图函数index
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定paginate_by 属性开启分页功能，其值表示每一页包含多少篇文章
    paginate_by = 3

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     paginator = context.get('paginator')
    #     page = context.get('page_obj')
    #     is_paginated = context.get('is_paginated')
    #
    #
    # def pagination_data(self, paginator, page, is_paginated):
    #     if not is_paginated:
    #         return {}
    #     left = []
    #     right = []
    #     left_has_more = False
    #     right_has_more = False
    #     first = False
    #     last = False
    #     page_number = page.number
    #     total_pages = paginator.num_pages
    #     page_range = paginator.page_range
    #     if page_number == 1:
    #         right = page_range[page_number: page_number + 2]


# 文章详情页视图
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # return render(request, 'blog/detail.html', context={'post': post})
    # 阅读量+1
    post.increase_views()
    # # 使用markdown语法渲染body，并支持代码格式扩展，代码语法高亮等
    # post.body = markdown.markdown(post.body, extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',
    #     'markdown.extensions.toc',
    # ])
    # 实例化一个Markdown对象，可以给post动态添加toc属性
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 处理目录的锚点显示问题
        TocExtension(slugify=slugify),
        # 'markdown.extensions.toc',
        ])
    post.body = md.convert(post.body)
    post.toc = md.toc

    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)


# 使用类视图PostDetailView替代视图函数detail
# PostDetailView 继承 DetailView，需求是从数据库中获取模型(Post)一条记录数据
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    # 复写父类的get方法，将post对象取出来，调用increase_views()，阅读量+1
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # self.object即为父类的get方法查询出来的Post类的对象实例
        self.object.increase_views()
        # 返回的是个HttpResponse对象
        return response

    # 对post对象的body进行markdown渲染
    # extensions参数
    # 'markdown.extensions.codehilite' 代码高亮拓展
    # 'markdown.extensions.toc' 自动生成目录的扩展
    # 这种直接调用markdown方法渲染post.body方法局限性在于只能通过[TOC]标记在文章内容中插入目录，而不能在页面其他地方插入。
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                        ])
        return post

    # 将commentform评论表单、post下的评论列表传递给模板
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context

    def get_queryset(self):
        return super(PostDetailView, self).get_queryset()


# 归档详情页视图
def archives(request, year, month):
    """
    点击某个归档时间，显示此归档时间下的文章列表
    :param request:
    :param year:
    :param month:
    :return:
    """
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 使用类视图ArchivesView替代视图函数archives
class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


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
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 使用类视图CategoryView替代视图函数category
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# 使用类视图TagView显示某个标签下的文章列表
class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键字"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg, 'post_list': post_list})
