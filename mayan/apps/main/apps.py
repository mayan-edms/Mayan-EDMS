from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _


class MainApp(apps.AppConfig):
    name = 'main'
    verbose_name = _('Main')
