from django.template import Library

from ..classes import SearchModel

register = Library()


@register.simple_tag
def search_get_search_models():
    return SearchModel.all()
