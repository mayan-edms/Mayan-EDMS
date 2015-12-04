from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _


class LockManagerApp(apps.AppConfig):
    name = 'lock_manager'
    test = True
    verbose_name = _('Lock manager')
