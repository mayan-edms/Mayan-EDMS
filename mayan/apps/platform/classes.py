import os
from pathlib import Path

from django.conf import settings
from django.template import loader
from django.template.base import Template
from django.template.context import Context
from django.utils.encoding import force_text
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_dump, yaml_load
from mayan.apps.task_manager.classes import Worker
from mayan.settings.literals import (
    DEFAULT_DATABASE_NAME, DEFAULT_DATABASE_PASSWORD, DEFAULT_DATABASE_USER,
    DEFAULT_DIRECTORY_INSTALLATION, DEFAULT_USER_SETTINGS_FOLDER,
    DOCKER_DIND_IMAGE_VERSION, DOCKER_LINUX_IMAGE_VERSION,
    DOCKER_MYSQL_IMAGE_VERSION, DOCKER_POSTGRES_IMAGE_VERSION,
    GUNICORN_JITTER, GUNICORN_LIMIT_REQUEST_LINE, GUNICORN_MAX_REQUESTS,
    GUNICORN_TIMEOUT, GUNICORN_WORKER_CLASS, GUNICORN_WORKERS
)

from .utils import load_env_file


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
        return force_text(s=self.get_label())

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


class PlatformTemplateDockerEntrypoint(PlatformTemplate):
    label = _('Template for entrypoint.sh file inside a Docker image.')
    name = 'docker_entrypoint'

    def get_context(self):
        context = load_env_file()
        context.update({'workers': Worker.all()})
        return context


class PlatformTemplateDockerfile(PlatformTemplate):
    label = _('Template that generates a Dockerfile file.')
    name = 'dockerfile'

    def __init__(self):
        self.variables = (
            Variable(
                name='DOCKER_LINUX_IMAGE_VERSION',
                default=DOCKER_LINUX_IMAGE_VERSION,
                environment_name='MAYAN_DOCKER_LINUX_IMAGE_VERSION'
            ),
        )


class PlatformTemplateDockerSupervisord(PlatformTemplate):
    label = _('Template for Supervisord inside a Docker image.')
    name = 'docker_supervisord'

    def get_context(self):
        return {
            'autorestart': 'false',
            'shell_path': '/bin/sh',
            'stderr_logfile': '/dev/fd/2',
            'stderr_logfile_maxbytes': '0',
            'stdout_logfile': '/dev/fd/1',
            'stdout_logfile_maxbytes': '0',
            'workers': Worker.all()
        }


class PlatformTemplateGitLabCI(PlatformTemplate):
    label = _('Template that generates a GitLab CI config file.')
    name = 'gitlab-ci'

    def __init__(self):
        self.variables = (
            Variable(
                name='DEFAULT_DATABASE_NAME',
                default=DEFAULT_DATABASE_NAME,
                environment_name='MAYAN_DEFAULT_DATABASE_NAME'
            ),
            Variable(
                name='DEFAULT_DATABASE_PASSWORD',
                default=DEFAULT_DATABASE_PASSWORD,
                environment_name='MAYAN_DEFAULT_DATABASE_PASSWORD'
            ),
            Variable(
                name='DEFAULT_DATABASE_USER',
                default=DEFAULT_DATABASE_USER,
                environment_name='MAYAN_DEFAULT_DATABASE_USER'
            ),
            Variable(
                name='DOCKER_DIND_IMAGE_VERSION',
                default=DOCKER_DIND_IMAGE_VERSION,
                environment_name='MAYAN_DOCKER_DIND_IMAGE_VERSION'
            ),
            Variable(
                name='DOCKER_LINUX_IMAGE_VERSION',
                default=DOCKER_LINUX_IMAGE_VERSION,
                environment_name='MAYAN_DOCKER_LINUX_IMAGE_VERSION'
            ),
            Variable(
                name='DOCKER_MYSQL_IMAGE_VERSION',
                default=DOCKER_MYSQL_IMAGE_VERSION,
                environment_name='MAYAN_DOCKER_MYSQL_IMAGE_VERSION'
            ),
            Variable(
                name='DOCKER_POSTGRES_IMAGE_VERSION',
                default=DOCKER_POSTGRES_IMAGE_VERSION,
                environment_name='MAYAN_DOCKER_POSTGRES_IMAGE_VERSION'
            ),
        )


class PlatformTemplateSupervisord(PlatformTemplate):
    label = _('Template for Supervisord.')
    name = 'supervisord'

    def __init__(self):
        self.variables = (
            Variable(
                name='GUNICORN_JITTER',
                default=GUNICORN_JITTER,
                environment_name='MAYAN_GUNICORN_JITTER'
            ),
            Variable(
                name='GUNICORN_LIMIT_REQUEST_LINE',
                default=GUNICORN_LIMIT_REQUEST_LINE,
                environment_name='MAYAN_GUNICORN_GUNICORN_LIMIT_REQUEST_LINE'
            ),
            Variable(
                name='GUNICORN_MAX_REQUESTS',
                default=GUNICORN_MAX_REQUESTS,
                environment_name='MAYAN_GUNICORN_MAX_REQUESTS'
            ),
            Variable(
                name='GUNICORN_TIMEOUT',
                default=GUNICORN_TIMEOUT,
                environment_name='MAYAN_GUNICORN_TIMEOUT'
            ),
            Variable(
                name='GUNICORN_WORKER_CLASS',
                default=GUNICORN_WORKER_CLASS,
                environment_name='MAYAN_GUNICORN_WORKER_CLASS'
            ),
            Variable(
                name='GUNICORN_WORKERS',
                default=GUNICORN_WORKERS,
                environment_name='MAYAN_GUNICORN_WORKERS'
            ),
            Variable(
                name='GUNICORN_TIMEOUT',
                default=GUNICORN_TIMEOUT,
                environment_name='MAYAN_GUNICORN_TIMEOUT'
            ),
            Variable(
                name='INSTALLATION_PATH', default=DEFAULT_DIRECTORY_INSTALLATION,
                environment_name='MAYAN_INSTALLATION_PATH'
            ),
            Variable(
                name='USER_SETTINGS_FOLDER',
                default=DEFAULT_USER_SETTINGS_FOLDER,
                environment_name='MAYAN_USER_SETTINGS_FOLDER'
            ),
            YAMLVariable(
                name='MEDIA_ROOT', default=settings.MEDIA_ROOT,
                environment_name='MAYAN_MEDIA_ROOT'
            ),
        )

    def get_context(self):
        *_, user_settings_folder, media_root = self.variables

        return {
            'autorestart': 'true',
            'shell_path': '/bin/sh',
            'user_settings_folder': Path(
                media_root.get_value()
            ) / user_settings_folder.get_value(),
            'workers': Worker.all(),
        }


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
        try:
            queues = Worker.get(name=worker_name).queues
        except KeyError:
            raise KeyError('Worker name "{}" not found.'.format(worker_name))

        return {
            'queues': queues, 'queue_names': sorted(
                map(lambda x: x.name, queues)
            )
        }


PlatformTemplate.register(klass=PlatformTemplateDockerEntrypoint)
PlatformTemplate.register(klass=PlatformTemplateDockerfile)
PlatformTemplate.register(klass=PlatformTemplateDockerSupervisord)
PlatformTemplate.register(klass=PlatformTemplateGitLabCI)
PlatformTemplate.register(klass=PlatformTemplateSupervisord)
PlatformTemplate.register(klass=PlatformTemplateWorkerQueues)
