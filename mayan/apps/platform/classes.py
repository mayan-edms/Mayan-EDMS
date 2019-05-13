from __future__ import absolute_import, unicode_literals

import yaml
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from django.template import loader
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import Worker


@python_2_unicode_compatible
class PlatformTemplate(object):
    _registry = {}
    context = {}
    label = None
    template_name = None

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

    def get_label(self):
        return self.label or self.name

    def get_template_name(self):
        return self.template_name or 'platform/{}.tmpl'.format(self.name)

    def render(self, context_string=None):
        context = self.get_context()

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
    label = _('Template for Supervisord.')
    name = 'supervisord'

    def get_context(self):
        return {
            'gunicorn_workers': 2,
            'result_backend': 'redis://127.0.0.1:6379/0',
            'broker_url': 'redis://127.0.0.1:6379/0',
            'database_conn_max_age': 60,
            'database_engine': 'django.db.backends.postgresql',
            'database_host': '127.0.0.1',
            'database_name': 'mayan',
            'database_password': 'mayanuserpass',
            'database_user': 'mayan',
            'installation_path': '/opt/mayan-edms',
            'media_root': '/opt/mayan-edms/media',
            'workers': Worker.all()
        }


class PlatformTemplateSupervisordDocker(PlatformTemplate):
    label = _('Template for Supervisord inside a Docker image.')
    name = 'supervisord_docker'

    def get_context(self):
        return {'workers': Worker.all()}


PlatformTemplate.register(klass=PlatformTemplateSupervisord)
PlatformTemplate.register(klass=PlatformTemplateSupervisordDocker)
