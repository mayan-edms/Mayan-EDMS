from django.template import Library

from common.utils import return_attrib

register = Library()


@register.filter
def object_property(value, arg):
    return return_attrib(value, arg)
