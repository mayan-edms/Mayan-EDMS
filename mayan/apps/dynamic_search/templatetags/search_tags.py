from __future__ import unicode_literals

from django.template import Library

from ..classes import SearchModel

register = Library()


@register.simple_tag
def get_search_models():
    return SearchModel.all()
