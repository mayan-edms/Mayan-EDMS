from django import apps
from django.utils.translation import ugettext_lazy as _

from .classes import DefinedStorage


class StorageApp(apps.AppConfig):
    has_tests = True
    name = 'mayan.apps.storage'
    verbose_name = _('Storage')

    def ready(self):
        super(StorageApp, self).ready()
        DefinedStorage.initialize()
