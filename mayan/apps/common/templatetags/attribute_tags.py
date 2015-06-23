from django.template import Library

from common.utils import return_attrib
from navigation.api import model_list_columns

register = Library()


@register.filter
def object_property(value, arg):
    return return_attrib(value, arg)


@register.filter
def get_model_list_columns(obj):
    try:
        # Is it a query set?
        obj = obj.model
    except AttributeError:
        # Is not a query set
        try:
            # Is iterable?
            obj = obj[0]
        except TypeError:
            # It is not
            pass
        except IndexError:
            # It a list and it's empty
            pass
        except KeyError:
            # It a list and it's empty
            pass

    for key, value in model_list_columns.items():
        if key == obj or isinstance(obj, key):
            return value

    return []
