from blogproject.blog.models import Post
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from .forms import CommentForm


# Create your views here.
# 视图函数处理逻辑
def post_comment(request, post_pk):
    """
    1.获取被评论的文章，后面将评论与被评论的文章关联
    2.get_object_or_404函数，当获取的文章存在时，则获取；否则返回404页面
    :param request:
    :param post_pk:
    :return:
    """
    post = get_object_or_404(Post, pk=post_pk)

    # 处理post请求，用户通过表单提交数据一般都是post请求
    if request.method == 'POST':
        # 用户提交的数据存在request.POST中，这是个类字典对象
        # 构造CommentForm实例，生成Django表单
        form = CommentForm(request.POST)
        # 判断数据是否符合格式要求
        if form.is_valid():
            # save()方法保存数据到数据库
            # commit=False表明使用表单数据生成Comment类的实例，但不保存评论数据到数据库
            comment = Comment(form.save(commit=False))
            # 关联评论和被评论的文章
            comment.post = post
            # 最终将评论数据保存到数据库
            comment.save()

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL
            return redirect(post)

        else:
            # 数据不合法，重新渲染详情页，并渲染生成表单的错误
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。

            # comment = form.save(commit=False)
            # comment.post = post
            # comment_list = Post.objects.filter(comment=comment,pk=post_pk).order_by('-created_time')
            # comment_list = post.objects.filter(comment=comment).oder_by('-created_time')
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)
    # 不是post请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)

