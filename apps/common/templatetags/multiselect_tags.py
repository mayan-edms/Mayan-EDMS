from django.template import Library
from django.utils.simplejson import dumps

from common.utils import return_attrib

register = Library()


@register.filter
def get_encoded_parameter(item, parameters_dict):
    result = {}
    for attrib_name, attrib in parameters_dict.items():
        result[attrib_name] = return_attrib(item, attrib)
    return dumps(result)
