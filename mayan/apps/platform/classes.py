from __future__ import absolute_import, unicode_literals

import os

from django.template import loader
from django.utils.html import mark_safe
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_dump, yaml_load
from mayan.apps.common.settings import (
    setting_celery_broker_url, setting_celery_result_backend
)
from mayan.apps.task_manager.classes import Worker


class Variable(object):
    def __init__(self, name, default, environment_name):
        self.name = name
        self.default = default
        self.environment_name = environment_name

    def _get_value(self):
        return os.environ.get(self.environment_name, self.default)

    def get_value(self):
        return mark_safe(self._get_value())


class YAMLVariable(Variable):
    def _get_value(self):
        value = os.environ.get(self.environment_name)
        if value:
            value = yaml_load(stream=value)
        else:
            value = self.default

        return yaml_dump(
            data=value, allow_unicode=True, default_flow_style=True, width=999
        ).replace('...\n', '').replace('\n', '')


@python_2_unicode_compatible
class PlatformTemplate(object):
    _registry = {}
    context = {}
    context_defaults = {}
    label = None
    settings = None
    template_name = None
    variables = None

    @classmethod
    def all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def register(cls, klass):
        cls._registry[klass.name] = klass

    def __str__(self):
        return force_text(self.get_label())

    def get_context(self):
        return self.context

    def get_context_defaults(self):
        return self.context_defaults

    def get_label(self):
        return self.label or self.name

    def get_settings_context(self):
        result = {}
        for setting in self.settings or ():
            if setting.value:
                result[setting.global_name] = setting.value

        return result

    def get_template_name(self):
        return self.template_name or 'platform/{}.tmpl'.format(self.name)

    def get_variables_context(self):
        result = {}
        for variable in self.variables or ():
            result[variable.name] = variable.get_value()

        return result

    def render(self, context_string=None):
        """
        context_string allows the management command to pass context to this
        method as a JSON string
        """
        context = {}

        context.update(self.get_context_defaults())
        context.update(self.get_settings_context())
        context.update(self.get_variables_context())
        # get_context goes last to server as the override
        context.update(self.get_context())

        if context_string:
            context.update(
                yaml_load(stream=context_string)
            )
        return loader.render_to_string(
            template_name=self.get_template_name(),
            context=context
        )


class PlatformTemplateSupervisord(PlatformTemplate):
    label = _('Template for Supervisord.')
    name = 'supervisord'
    settings = (
        setting_celery_broker_url, setting_celery_result_backend
    )
    variables = (
        Variable(
            name='GUNICORN_WORKERS', default=2,
            environment_name='MAYAN_GUNICORN_WORKERS'
        ),
        Variable(
            name='GUNICORN_TIMEOUT', default=120,
            environment_name='MAYAN_GUNICORN_TIMEOUT'
        ),
        Variable(
            name='INSTALLATION_PATH', default='/opt/mayan-edms',
            environment_name='MAYAN_INSTALLATION_PATH'
        ),
        YAMLVariable(
            name='ALLOWED_HOSTS',
            default=['*'],
            environment_name='MAYAN_ALLOWED_HOSTS'
        ),
        YAMLVariable(
            name='BROKER_URL',
            default='redis://127.0.0.1:6379/0',
            environment_name='MAYAN_BROKER_URL'
        ),
        YAMLVariable(
            name='CELERY_RESULT_BACKEND',
            default='redis://127.0.0.1:6379/0',
            environment_name='MAYAN_CELERY_RESULT_BACKEND'
        ),
        YAMLVariable(
            name='DATABASES',
            default={
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'mayan', 'PASSWORD':'mayanuserpass',
                    'USER': 'mayan', 'HOST':'127.0.0.1'
                }
            },
            environment_name='MAYAN_DATABASES'
        ),
        YAMLVariable
        (
            name='MEDIA_ROOT', default='/opt/mayan-edms/media',
            environment_name='MAYAN_MEDIA_ROOT'
        ),
    )

    def get_context(self):
        return {
            'workers': Worker.all()
        }


class PlatformTemplateSupervisordDocker(PlatformTemplate):
    label = _('Template for Supervisord inside a Docker image.')
    name = 'supervisord_docker'

    def get_context(self):
        return {'workers': Worker.all()}


PlatformTemplate.register(klass=PlatformTemplateSupervisord)
PlatformTemplate.register(klass=PlatformTemplateSupervisordDocker)
