import logging
import types

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db.models.constants import LOOKUP_SEP
from django.urls import resolve as django_resolve
from django.urls.base import get_script_prefix
from django.utils.encoding import force_text
from django.utils.six.moves import reduce as reduce_function

from mayan.apps.common.compat import dict_type, dictionary_type

from .literals import DJANGO_SQLITE_BACKEND

logger = logging.getLogger(name=__name__)


def check_for_sqlite():
    return settings.DATABASES['default']['ENGINE'] == DJANGO_SQLITE_BACKEND and settings.DEBUG is False


def convert_to_id_list(items):
    return ','.join(map(force_text, items))


def get_related_field(model, related_field_name):
    try:
        local_field_name, remaining_field_path = related_field_name.split(
            LOOKUP_SEP, 1
        )
    except ValueError:
        local_field_name = related_field_name
        remaining_field_path = None

    related_field = model._meta.get_field(local_field_name)

    if remaining_field_path:
        return get_related_field(
            model=related_field.related_model,
            related_field_name=remaining_field_path
        )

    return related_field


def introspect_attribute(attribute_name, obj):
    """
    Resolve the attribute of model. Supports nested reference using dotted
    paths or double underscore.
    """
    try:
        # Try as a related field
        obj._meta.get_field(field_name=attribute_name)
    except (AttributeError, FieldDoesNotExist):
        attribute_name = attribute_name.replace('__', '.')

        try:
            # If there are separators in the attribute name, traverse them
            # to the final attribute
            attribute_part, attribute_remaining = attribute_name.split(
                '.', 1
            )
        except ValueError:
            return attribute_name, obj
        else:
            related_field = obj._meta.get_field(field_name=attribute_part)
            return introspect_attribute(
                attribute_name=attribute_part,
                obj=related_field.related_model,
            )
    else:
        return attribute_name, obj


def resolve(path, urlconf=None):
    path = '/{}'.format(path.replace(get_script_prefix(), '', 1))
    return django_resolve(path=path, urlconf=urlconf)


def resolve_attribute(attribute, obj, kwargs=None):
    """
    Resolve the attribute of an object. Behaves like the Python REPL but with
    an unified dotted path schema regardless of the attribute type.
    Supports callables, dictionaries, properties, related model fields.
    """
    if not kwargs:
        kwargs = {}

    # Try as a callable
    try:
        return attribute(obj, **kwargs)
    except TypeError:
        # Try as a dictionary
        try:
            return obj[attribute]
        except TypeError:
            try:
                # If there are dots in the attribute name, traverse them
                # to the final attribute
                result = reduce_function(getattr, attribute.split('.'), obj)
                try:
                    # Try it as a method
                    return result(**kwargs)
                except (TypeError, ValueError):
                    # Try it as a property
                    return result
            except AttributeError:
                # Try as a related model field
                if LOOKUP_SEP in attribute:
                    attribute_replaced = attribute.replace(LOOKUP_SEP, '.')
                    return resolve_attribute(
                        obj=obj, attribute=attribute_replaced, kwargs=kwargs
                    )
                else:
                    raise


def return_attrib(obj, attrib, arguments=None):
    if isinstance(attrib, types.FunctionType):
        return attrib(obj)
    elif isinstance(
        obj, dict_type
    ) or isinstance(obj, dictionary_type):
        return obj[attrib]
    else:
        result = reduce_function(getattr, attrib.split('.'), obj)
        if isinstance(result, types.MethodType):
            if arguments:
                return result(**arguments)
            else:
                return result()
        else:
            return result


def return_related(instance, related_field):
    """
    This functions works in a similar method to return_attrib but is
    meant for related models. Support multiple levels of relationship
    using double underscore.
    """
    return reduce_function(getattr, related_field.split('__'), instance)
