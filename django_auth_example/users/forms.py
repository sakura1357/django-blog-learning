# encoding: utf-8

from django.contrib.auth.forms import UserCreationForm
from .models import User

'''
@author: siar
@contact: xzt1357@gmail.com
@file: forms.py
@time: 2017/7/12 10:54
@desc:
'''


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")