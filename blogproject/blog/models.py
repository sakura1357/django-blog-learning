# coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
# Create your models here.
# 默认创建表格的时候，Django会自动创建id字段，无需在model中手动声明
# 使用装饰器decorator，修饰类


@python_2_unicode_compatible
class Category(models.Model):
    """
    分类
    """
    # 分类名称
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    """
    标签
    """
    # 标签名称
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    """
    文章
    """
    # 文章标题 短字符串
    title = models.CharField(max_length=70)

    # 文章正文，字段类型TextField
    body = models.TextField()

    # 文章创建时间和最后一次修改时间，字段类型DateTimeField
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要，可以为空，只需设置blank=True即可，否则为空时会报错
    excerpt = models.CharField(max_length=200, blank=True)

    # 关联文章与分类、标签，实际是按照自动创建的id来进行关联
    # 一篇文章只能对应一个分类，一个分类下有多篇文章  1:n  ForeignKey 一对多关联关系 外键关联
    # 一篇文章可以有多个标签，同一个标签下可以有多篇文章， m:n  ManyToManyField 多对多关联关系  中间表post.id-tag.id关联
    # 规定文章可以没有标签，即设置tags blank=True
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 导入Django内置应用django.contrib.auth.models里的User model
    # 一篇文章只能有一个作者，一个作者可以写多篇文章，1:n ForeignKey 一对多关联关系
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 从django.urls 导入 reverser函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

