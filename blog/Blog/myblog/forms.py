# -*- coding:utf-8 -*-
__author__ = 'dapeng'
__date__ = '18-11-2 下午6:52'

from django import forms
from myblog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content', 'blog']