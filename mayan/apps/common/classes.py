from __future__ import unicode_literals

import hashlib

from django.apps import apps
from django.conf import settings
from django.db import models
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext


@python_2_unicode_compatible
class Collection(object):
    _registry = []

    @classmethod
    def get_all(cls):
        return sorted(cls._registry, key=lambda entry: entry._order)

    def __init__(self, label, icon=None, icon_class=None, link=None, queryset=None, model=None, order=None):
        self._label = label
        self._icon = icon
        self._icon_class = icon_class
        self._link = link
        self._queryset = queryset
        self._model = model
        self._order = order or 99
        self.__class__._registry.append(self)

    def __str__(self):
        return force_text(self.label)

    def resolve(self):
        self.children = self._get_children()
        self.icon = self._icon
        self.label = self._label
        self.url = None
        if self._link:
            self.icon = getattr(self._link, 'icon', self._icon)
            self.icon_class = getattr(self._link, 'icon_class', self._icon_class)
            self.url = reverse(viewname=self._link.view, args=self._link.args)
        return ''

    def _get_children(self):
        if self._queryset:
            return self._queryset
        else:
            if self._model:
                return self._model.objects.all()


class Dashboard(object):
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.widgets = {}
        self.removed_widgets = []
        self.__class__._registry[name] = self

    def add_widget(self, widget, order=0):
        self.widgets[widget] = {'widget': widget, 'order': order}

    def get_widgets(self):
        """
        Returns a list of widgets sorted by their 'order'.
        If two or more widgets have the same 'order', sort by label.
        """
        return map(
            lambda x: x['widget'],
            filter(
                lambda x: x['widget'] not in self.removed_widgets,
                sorted(
                    self.widgets.values(),
                    key=lambda x: (x['order'], x['widget'].label)
                )
            )
        )

    def remove_widget(self, widget):
        self.removed_widgets.append(widget)

    def render(self, request):
        rendered_widgets = [widget().render(request=request) for widget in self.get_widgets()]

        return loader.render_to_string(
            template_name='dashboard/dashboard.html', context={
                'widgets': rendered_widgets
            }
        )


class BaseDashboardWidget(object):
    _registry = {}
    context = {}
    template_name = None

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return cls._registry.items()

    @classmethod
    def register(cls, klass):
        cls._registry[klass.name] = klass

    def get_context(self):
        return self.context

    def render(self, request):
        if self.template_name:
            return loader.render_to_string(
                template_name=self.template_name, context=self.get_context(),
            )


class DashboardWidgetNumeric(BaseDashboardWidget):
    count = 0
    icon_class = None
    label = None
    link = None
    template_name = 'dashboard/numeric_widget.html'

    def get_context(self):
        return {
            'count': self.count,
            'icon_class': self.icon_class,
            'label': self.label,
            'link': self.link,
        }


@python_2_unicode_compatible
class ErrorLogNamespace(object):
    def __init__(self, name, label=None):
        self.name = name
        self.label = label or name

    def __str__(self):
        return force_text(self.label)

    def create(self, obj, result):
        obj.error_logs.create(namespace=self.name, result=result)

    def all(self):
        ErrorLogEntry = apps.get_model(
            app_label='common', model_name='ErrorLogEntry'
        )

        return ErrorLogEntry.objects.filter(namespace=self.name)


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


@python_2_unicode_compatible
class ModelAttribute(object):
    _registry = {}

    @classmethod
    def get_for(cls, model):
        try:
            return cls._registry[model]
        except KeyError:
            # We were passed a model instance, try again using the model of
            # the instance

            # If we are already in the model class, exit with an error
            if model.__class__ == models.base.ModelBase:
                raise

            return cls.get_for(model=type(model))

    @classmethod
    def get_choices_for(cls, model):
        return [
            (attribute.name, attribute) for attribute in cls.get_for(model)
        ]

    @classmethod
    def get_help_text_for(cls, model, show_name=False):
        result = []
        for count, attribute in enumerate(cls.get_for(model=model), 1):
            result.append(
                '{}) {}'.format(
                    count, force_text(attribute.get_display(show_name=show_name))
                )
            )

        return ' '.join(
            [ugettext('Available attributes: \n'), '\n'.join(result)]
        )

    def __init__(self, model, name, label=None, description=None):
        self.model = model
        self.label = label
        self.name = name
        self.description = description
        self._registry.setdefault(model, [])
        self._registry[model].append(self)

    def __str__(self):
        return self.get_display()

    def get_display(self, show_name=False):
        if self.description:
            return '{} - {}'.format(
                self.name if show_name else self.label, self.description
            )
        else:
            return force_text(self.name if show_name else self.label)


class ModelField(ModelAttribute):
    """Subclass to handle model database fields"""
    _registry = {}

    @classmethod
    def get_help_text_for(cls, model, show_name=False):
        result = []
        for count, model_field in enumerate(cls.get_for(model=model), 1):
            result.append(
                '{}) {} - {}'.format(
                    count,
                    model_field.name if show_name else model_field.label,
                    model_field.description
                )
            )

        return ' '.join(
            [ugettext('Available fields: \n'), '\n'.join(result)]
        )

    def __init__(self, *args, **kwargs):
        super(ModelField, self).__init__(*args, **kwargs)
        self._final_model_verbose_name = None

        if not self.label:
            self.label = self.get_field_attribute(
                attribute='verbose_name'
            )
            if self.label != self._final_model_verbose_name:
                self.label = '{} {}'.format(
                    self._final_model_verbose_name, self.label
                )

        if not self.description:
            self.description = self.get_field_attribute(
                attribute='help_text'
            )

    def get_field_attribute(self, attribute, model=None, field_name=None):
        if not model:
            model = self.model

        if not field_name:
            field_name = self.name

        parts = field_name.split('__')
        if len(parts) > 1:
            return self.get_field_attribute(
                model=model._meta.get_field(parts[0]).related_model,
                field_name='__'.join(parts[1:]), attribute=attribute
            )
        else:
            self._final_model_verbose_name = model._meta.verbose_name
            return getattr(
                model._meta.get_field(field_name=field_name),
                attribute
            )


class ModelProperty(object):
    _registry = []

    @classmethod
    def get_for(cls, model):
        result = []

        for klass in cls._registry:
            result.extend(klass.get_for(model=model))

        return result

    @classmethod
    def get_choices_for(cls, model):
        result = []

        for klass in cls._registry:
            result.extend(klass.get_choices_for(model=model))

        return result

    @classmethod
    def get_help_text_for(cls, model, show_name=False):
        result = []

        for klass in cls._registry:
            result.append(
                klass.get_help_text_for(model=model, show_name=show_name)
            )

        return '\n'.join(result)

    @classmethod
    def register(cls, klass):
        cls._registry.append(klass)


class Package(object):
    _registry = []

    @classmethod
    def get_all(cls):
        return cls._registry

    def __init__(self, label, license_text):
        self.label = label
        self.license_text = license_text
        self.__class__._registry.append(self)


class PropertyHelper(object):
    """
    Makes adding fields using __class__.add_to_class easier.
    Each subclass must implement the `constructor` and the `get_result`
    method.
    """
    @staticmethod
    @property
    def constructor(source_object):
        return PropertyHelper(source_object)

    def __init__(self, instance):
        self.instance = instance

    def __getattr__(self, name):
        return self.get_result(name=name)

    def get_result(self, name):
        """
        The method that produces the actual result. Must be implemented
        by each subclass.
        """
        raise NotImplementedError


class Template(object):
    _registry = {}

    @classmethod
    def all(cls, rendered=False, request=None):
        if not rendered:
            return cls._registry.values()
        else:
            result = []
            for template in cls._registry.values():
                result.append(template.render(request=request))
            return result

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name, template_name):
        self.name = name
        self.template_name = template_name
        self.__class__._registry[name] = self

    def get_absolute_url(self):
        return reverse(
            kwargs={'name': self.name}, viewname='rest_api:template-detail'
        )

    def render(self, request):
        context = {
            'home_view': settings.HOME_VIEW,
        }
        result = TemplateResponse(
            request=request,
            template=self.template_name,
            context=context,
        ).render()

        # Calculate the hash of the bytes version but return the unicode
        # version
        self.html = result.rendered_content.replace('\n', '')
        self.hex_hash = hashlib.sha256(result.content).hexdigest()
        return self


ModelProperty.register(ModelAttribute)
ModelProperty.register(ModelField)
