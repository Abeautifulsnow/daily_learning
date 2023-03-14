#!usr/bin/env python
# -*- coding:utf-8 -*-
from django import template

register = template.Library()


@register.simple_tag
def content_wordcount():
    pass
