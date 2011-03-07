from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.template import Library, Node, Variable, VariableDoesNotExist

from common.utils import return_attrib
from common.api import model_list_columns

register = Library()

@register.filter
def object_property(value, arg):
    return return_attrib(value, arg)
    
@register.filter
def get_model_list_columns(value):
    return model_list_columns.get(type(value), [])
