from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _


class NavigationApp(apps.AppConfig):
    name = 'navigation'
    verbose_name = _('Navigation')
