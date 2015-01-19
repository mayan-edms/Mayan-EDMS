from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext


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
            # We were passed a model instance, try again using the model of the
            # instance

            # If we are already in the model class, exit with an error
            if model.__class__ == models.base.ModelBase:
                raise

            return cls.get_for[type(model)]

    @classmethod
    def get_choices_for(cls, model, type_names=None):
        return [(attribute.name, attribute) for attribute in cls.get_for(model, type_names)]

    @classmethod
    def help_text_for(cls, model, type_names=None):
        result = []
        for count, attribute in enumerate(cls.get_for(model, type_names), 1):
            result.append('{}) {}'.format(count, unicode(attribute.get_display(show_name=True))))

        return ' '.join([ugettext('Available attributes: '), ', '.join(result)])

    def get_display(self, show_name=False):
        if self.description:
            return '{} - {}'.format(self.name if show_name else self.label, self.description)
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
