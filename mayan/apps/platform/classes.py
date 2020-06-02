import os

from django.template import loader
from django.template.base import Template
from django.template.context import Context
from django.utils.encoding import force_text
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_dump, yaml_load
from mayan.apps.task_manager.classes import Worker
from mayan.apps.task_manager.settings import (
    setting_celery_broker_url, setting_celery_result_backend
)


class Variable:
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


class PlatformTemplate:
    _registry = {}
    context = {}
    context_defaults = {}
    label = None
    name = None
    settings = None
    template_name = None
    template_string = None
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

        if self.template_string:
            template = Template(template_string=self.template_string)
            return template.render(context=Context(dict_=context))
        else:
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
            name='CELERY_BROKER_URL',
            default='redis://:mayanredispassword@127.0.0.1:6379/0',
            environment_name='MAYAN_CELERY_BROKER_URL'
        ),
        YAMLVariable(
            name='CELERY_RESULT_BACKEND',
            default='redis://:mayanredispassword@127.0.0.1:6379/1',
            environment_name='MAYAN_CELERY_RESULT_BACKEND'
        ),
        YAMLVariable(
            name='DATABASES',
            default={
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'mayan', 'PASSWORD': 'mayanuserpass',
                    'USER': 'mayan', 'HOST': '127.0.0.1'
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
        return {'workers': Worker.all()}


class PlatformTemplateSupervisordDocker(PlatformTemplate):
    label = _('Template for Supervisord inside a Docker image.')
    name = 'supervisord_docker'

    def get_context(self):
        return {'workers': Worker.all()}


class PlatformTemplateWorkerQueues(PlatformTemplate):
    label = _('Template showing the queues of a worker.')
    name = 'worker_queues'

    variables = (
        Variable(
            name='WORKER_NAME', default=None,
            environment_name='MAYAN_WORKER_NAME'
        ),
    )

    def get_context(self):
        worker_name = self.get_variables_context().get('WORKER_NAME')
        queues = Worker.get(name=worker_name).queues

        return {
            'queues': queues, 'queue_names': sorted(
                map(lambda x: x.name, queues)
            )
        }


PlatformTemplate.register(klass=PlatformTemplateSupervisord)
PlatformTemplate.register(klass=PlatformTemplateSupervisordDocker)
PlatformTemplate.register(klass=PlatformTemplateWorkerQueues)
