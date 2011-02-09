from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.template import Library, Node, Variable, VariableDoesNotExist

from common.utils import return_attrib

register = Library()

@register.filter
def object_property(value, arg):
    return return_attrib(value, arg)
