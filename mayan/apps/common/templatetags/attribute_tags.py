from django.template import Library

from common.utils import return_attrib
from navigation.api import model_list_columns

register = Library()


@register.filter
def object_property(value, arg):
    return return_attrib(value, arg)


@register.filter
def get_model_list_columns(obj):
    for key, value in model_list_columns.items():
        if isinstance(obj, key):
            return value

    return []
