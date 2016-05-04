from __future__ import unicode_literals

from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils.translation import ugettext

from permissions import Permission


class ModelAttribute(object):
    __registry = {}

    @classmethod
    def get_for(cls, model, type_names=None):
        result = []

        try:
            for type_name, attributes in cls.__registry[model].iteritems():
                if not type_names or type_name in type_names:
                    result.extend(attributes)

            return result
        except IndexError:
            # We were passed a model instance, try again using the model of
            # the instance

            # If we are already in the model class, exit with an error
            if model.__class__ == models.base.ModelBase:
                raise

            return cls.get_for[type(model)]

    @classmethod
    def get_choices_for(cls, model, type_names=None):
        return [
            (
                attribute.name, attribute
            ) for attribute in cls.get_for(model, type_names)
        ]

    @classmethod
    def help_text_for(cls, model, type_names=None):
        result = []
        for count, attribute in enumerate(cls.get_for(model, type_names), 1):
            result.append(
                '{}) {}'.format(
                    count, unicode(attribute.get_display(show_name=True))
                )
            )

        return ' '.join(
            [ugettext('Available attributes: '), ', '.join(result)]
        )

    def get_display(self, show_name=False):
        if self.description:
            return '{} - {}'.format(
                self.name if show_name else self.label, self.description
            )
        else:
            return unicode(self.name if show_name else self.label)

    def __unicode__(self):
        return self.get_display()

    def __init__(self, model, name, label=None, description=None, type_name=None):
        self.model = model
        self.label = label
        self.name = name
        self.description = description

        for field in model._meta.fields:
            if field.name == name:
                self.label = field.verbose_name
                self.description = field.help_text

        self.__registry.setdefault(model, {})

        if isinstance(type_name, list):
            for single_type in type_name:
                self.__registry[model].setdefault(single_type, [])
                self.__registry[model][single_type].append(self)
        else:
            self.__registry[model].setdefault(type_name, [])
            self.__registry[model][type_name].append(self)


class MissingItem(object):
    _registry = []

    @classmethod
    def get_all(cls):
        return cls._registry

    def __init__(self, label, condition, description, view):
        self.label = label
        self.condition = condition
        self.description = description
        self.view = view
        self.__class__._registry.append(self)


class Filter(object):
    _registry = {}

    @classmethod
    def get(cls, slug):
        return cls._registry[slug]

    @classmethod
    def all(cls):
        return cls._registry

    def __init__(self, label, slug, filter_kwargs, model, object_permission=None, hide_links=False):
        self.label = label
        self.slug = slug
        self.filter_kwargs = filter_kwargs
        self.model = model
        self.object_permission = object_permission
        self.hide_links = hide_links

        self.__class__._registry[self.slug] = self

    def __unicode__(self):
        return unicode(self.label)

    def get_queryset(self, user):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        queryset = self.model.objects.all()
        for kwargs in self.filter_kwargs:
            queryset = queryset.filter(**kwargs)

        queryset = queryset.distinct()

        if self.object_permission:
            try:
                # Check to see if the user has the permissions globally
                Permission.check_permissions(
                    user, (self.object_permission,)
                )
            except PermissionDenied:
                # No global permission, filter ther queryset per object +
                # permission
                return AccessControlList.objects.filter_by_access(
                    self.object_permission, user, queryset
                )
            else:
                # Has the permission globally, return all results
                return queryset
        else:
            return queryset


class Package(object):
    _registry = []

    @classmethod
    def get_all(cls):
        return cls._registry

    def __init__(self, label, license_text):
        self.label = label
        self.license_text = license_text
        self.__class__._registry.append(self)
