from distutils import util
from functools import reduce
import logging
import types

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db.models.constants import LOOKUP_SEP

from .exceptions import ResolverError, ResolverPipelineError
from .literals import DJANGO_SQLITE_BACKEND

logger = logging.getLogger(name=__name__)


class Resolver:
    exceptions = ()

    def __init__(self, attribute, obj, kwargs, klass, resolver_extra_kwargs):
        self.attribute = attribute
        self.obj = obj
        self.kwargs = kwargs
        self.klass = klass
        self.resolver_extra_kwargs = resolver_extra_kwargs

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
                    attribute=self.attribute, obj=item, kwargs=self.kwargs,
                    resolver_extra_kwargs=self.resolver_extra_kwargs
                )
            )

        return result


class ResolverPipelineObjectAttribute:
    resolver_list = (
        ResolverDictionary, ResolverList, ResolverFunction,
        ResolverObjectAttribute, ResolverGetattr
    )

    @classmethod
    def resolve(cls, attribute, obj, resolver_extra_kwargs=None, kwargs=None):
        kwargs = kwargs or {}
        resolver_extra_kwargs = resolver_extra_kwargs or {}

        if '.' in attribute:
            attribute_list = attribute.split('.')
        else:
            attribute_list = (attribute,)

        result = obj
        for attribute in attribute_list:
            for resolver in cls.resolver_list:
                try:
                    result = resolver(
                        attribute=attribute, obj=result, kwargs=kwargs,
                        klass=cls, resolver_extra_kwargs=resolver_extra_kwargs
                    ).resolve()
                except ResolverError:
                    """Expected, try the next resolver in the list."""

            if result == obj:
                raise ResolverPipelineError(
                    'Unable to resolve attribute `{attribute}` of object `{obj}`'.format(
                        attribute=attribute, obj=obj
                    )
                )

        return result


class ResolverRelatedManager(Resolver):
    exceptions = (AttributeError, FieldDoesNotExist)

    def _resolve(self):
        model = self.resolver_extra_kwargs.get('model', {})
        exclude = self.resolver_extra_kwargs.get('exclude', {})

        field = self.obj._meta.get_field(field_name=self.attribute)

        if field.many_to_one:
            # Many to one.
            queryset = field.related_model._meta.default_manager.filter(
                **{field.remote_field.name: self.obj.pk}
            )

            if field.related_model == model:
                queryset = queryset.exclude(**exclude)

            return queryset
        elif field.many_to_many:
            # Many to many from the parent side.
            if hasattr(field, 'get_filter_kwargs_for_object'):
                queryset = getattr(self.obj, field.attname)

                if queryset.model == model:
                    queryset = queryset.exclude(**exclude)
                else:
                    queryset = queryset.all()

                return queryset

        # Many to many from the child side.
        # One to many.
        # One to one.
        queryset = field.remote_field.model._meta.default_manager.filter(
            **{field.remote_field.name: self.obj.pk}
        )

        if field.related_model == model:
            queryset = queryset.exclude(**exclude)

        return queryset


class ResolverPipelineModelAttribute(ResolverPipelineObjectAttribute):
    resolver_list = (
        ResolverDictionary, ResolverList, ResolverRelatedManager,
        ResolverFunction, ResolverObjectAttribute, ResolverGetattr
    )

    @classmethod
    def resolve(cls, attribute, obj, resolver_extra_kwargs=None, kwargs=None):
        attribute = attribute.replace(LOOKUP_SEP, '.')
        return super().resolve(
            attribute=attribute, obj=obj, kwargs=kwargs,
            resolver_extra_kwargs=resolver_extra_kwargs
        )


def any_to_bool(value):
    if not isinstance(value, bool):
        value = bool(
            util.strtobool(val=value)
        )
    return value


def check_for_sqlite():
    return settings.DATABASES['default']['ENGINE'] == DJANGO_SQLITE_BACKEND and settings.DEBUG is False


def get_class_full_name(klass):
    return '{klass.__module__}.{klass.__qualname__}'.format(klass=klass)


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
                result = reduce(getattr, attribute.split('.'), obj)
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
        result = reduce(getattr, attrib.split('.'), obj)
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
    return reduce(getattr, related_field.split(LOOKUP_SEP), instance)
