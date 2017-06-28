from django.shortcuts import render, get_object_or_404
from .models import Comment
from .forms import CommentForm

from blog.models import Post

# Create your views here.
def post_comment(request, post_pk):

    post = get_object_or_404(Post, pk=post_pk)

