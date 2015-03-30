from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from project_setup.api import register_setup

from .links import check_settings


class SmartSettingsApp(apps.AppConfig):
    name = 'smart_settings'
    verbose_name = _('Smart settings')

    def ready(self):
        register_setup(check_settings)
