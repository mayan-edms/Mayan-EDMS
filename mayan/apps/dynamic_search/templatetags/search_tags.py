from django.template import Library

from ..classes import SearchModel
from ..literals import SEARCH_MODEL_NAME_KWARG

register = Library()


@register.simple_tag
def search_get_search_models():
    return SearchModel.all()


@register.simple_tag
def search_get_search_model_name_query_variable():
    return '_{}'.format(SEARCH_MODEL_NAME_KWARG)
