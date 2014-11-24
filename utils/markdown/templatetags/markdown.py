from __future__ import absolute_import
from markdown import markdown
from django.template import Library
__author__ = 'timirlan'

register = Library()


@register.filter
def mkd(text):
    return markdown(text)