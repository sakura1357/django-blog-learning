from django.db import models
from django.utils.six import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class Comment(models.Model):
    """
    评论用户的： name(用户), email(邮箱), url(个人网站), text(评论内容), created_time(评论时间)

    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    # auto_now_add=True 当评论数据保存到数据库时，自动把当前时间赋值给created_time
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]

