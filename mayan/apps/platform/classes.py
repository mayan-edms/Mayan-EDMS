from __future__ import absolute_import, unicode_literals

import os

import yaml
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from django.template import loader
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.settings import (
    setting_celery_broker_url, setting_celery_result_backend
)
from mayan.apps.task_manager.classes import Worker


class Variable(object):
    def __init__(self, name, default, environment_name):
        self.name = name
        self.default = default
        self.environment_name = environment_name

    def get_value(self):
        return os.environ.get(self.environment_name, self.default)


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
                yaml.load(
                    stream=context_string, Loader=SafeLoader
                )
            )
        return loader.render_to_string(
            template_name=self.get_template_name(),
            context=context
        )


class PlatformTemplateSupervisord(PlatformTemplate):
    context_defaults = {
        'BROKER_URL': 'redis://127.0.0.1:6379/0',
        'CELERY_RESULT_BACKEND': 'redis://127.0.0.1:6379/0',
    }
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
            name='DATABASE_CONN_MAX_AGE', default=0,
            environment_name='MAYAN_DATABASE_CONN_MAX_AGE'
        ),
        Variable(
            name='DATABASE_ENGINE', default='django.db.backends.postgresql',
            environment_name='MAYAN_DATABASE_ENGINE'
        ),
        Variable(
            name='DATABASE_HOST', default='127.0.0.1',
            environment_name='MAYAN_DATABASE_HOST'
        ),
        Variable(
            name='DATABASE_NAME', default='mayan',
            environment_name='MAYAN_DATABASE_NAME'
        ),
        Variable(
            name='DATABASE_PASSWORD', default='mayanuserpass',
            environment_name='MAYAN_DATABASE_PASSWORD'
        ),
        Variable(
            name='DATABASE_USER', default='mayan',
            environment_name='MAYAN_DATABASE_USER'
        ),
        Variable(
            name='INSTALLATION_PATH', default='/opt/mayan-edms',
            environment_name='MAYAN_INSTALLATION_PATH'
        ),
        Variable(
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
