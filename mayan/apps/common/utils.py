import logging
import types

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db.models.constants import LOOKUP_SEP
from django.utils.six.moves import reduce as reduce_function

from .exceptions import ResolverError, ResolverPipelineError
from .literals import DJANGO_SQLITE_BACKEND

logger = logging.getLogger(name=__name__)


class Resolver:
    exceptions = ()

    def __init__(self, attribute, obj, kwargs, klass):
        self.attribute = attribute
        self.obj = obj
        self.kwargs = kwargs
        self.klass = klass

    def resolve(self):
        try:
            return self._resolve()
        except self.exceptions:
            raise ResolverError

    def _resolve(self):
        raise NotImplementedError


class ResolverObjectAttribute(Resolver):
    exceptions = (TypeError,)

    def _resolve(self):
        return self.attribute(self.obj, **self.kwargs)


class ResolverGetattr(Resolver):
    exceptions = (AttributeError, TypeError,)

    def _resolve(self):
        return getattr(self.obj, self.attribute)


class ResolverFunction(Resolver):
    exceptions = (AttributeError, TypeError,)

    def _resolve(self):
        return getattr(self.obj, self.attribute)(**self.kwargs)


class ResolverDictionary(Resolver):
    exceptions = (TypeError,)

    def _resolve(self):
        return self.obj[self.attribute]


class ResolverList(Resolver):
    exceptions = (TypeError,)

    def _resolve(self):
        result = []
        for item in self.obj:
            result.append(
                self.klass.resolve(
                    attribute=self.attribute, obj=item, kwargs=self.kwargs
                )
            )

        return result


class ResolverPipelineObjectAttribute:
    resolver_list = (
        ResolverDictionary, ResolverList, ResolverFunction,
        ResolverObjectAttribute, ResolverGetattr
    )

    @classmethod
    def resolve(cls, attribute, obj, kwargs=None):
        if not kwargs:
            kwargs = {}

        if '.' in attribute:
            attribute_list = attribute.split('.')
        else:
            attribute_list = (attribute,)

        result = obj
        for attribute in attribute_list:
            for resolver in cls.resolver_list:
                try:
                    result = resolver(
                        attribute=attribute, obj=result, kwargs=kwargs, klass=cls
                    ).resolve()
                except ResolverError:
                    """Expected, try the next resolver in the list."""

            if result == obj:
                raise ResolverPipelineError(
                    'Unable to resolve attribute "{attribute}" of object "{obj}"'.format(
                        attribute=attribute, obj=obj
                    )
                )

        return result


class ResolverRelatedManager(Resolver):
    exceptions = (AttributeError,)

    def _resolve(self):
        return getattr(self.obj, self.attribute).all()


class ResolverPipelineModelAttribute(ResolverPipelineObjectAttribute):
    resolver_list = (
        ResolverDictionary, ResolverList, ResolverRelatedManager,
        ResolverFunction, ResolverObjectAttribute, ResolverGetattr
    )

    @classmethod
    def resolve(cls, attribute, obj, kwargs=None):
        attribute = attribute.replace(LOOKUP_SEP, '.')
        return super().resolve(attribute=attribute, obj=obj, kwargs=kwargs)


def check_for_sqlite():
    return settings.DATABASES['default']['ENGINE'] == DJANGO_SQLITE_BACKEND and settings.DEBUG is False


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
        obj, dict
    ) or isinstance(obj, dict):
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
