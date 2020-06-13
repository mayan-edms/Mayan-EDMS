from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig

from .classes import DefinedStorage


class StorageApp(MayanAppConfig):
    has_tests = True
    name = 'mayan.apps.storage'
    verbose_name = _('Storage')

    def ready(self):
        super(StorageApp, self).ready()
        DefinedStorage.load_modules()
