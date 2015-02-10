from __future__ import unicode_literals

from django.template import Library

register = Library()


@register.filter
def make_non_breakable(value):
    return value.replace('-', '\u2011')
