from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _


class StorageApp(apps.AppConfig):
    name = 'mayan.apps.storage'
    verbose_name = _('Storage')
