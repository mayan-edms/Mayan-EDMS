from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig

from .classes import DefinedStorage
from .tasks import task_delete_stale_uploads  # NOQA - Force task registration


class StorageApp(MayanAppConfig):
    has_tests = True
    name = 'mayan.apps.storage'
    verbose_name = _('Storage')

    def ready(self):
        super(StorageApp, self).ready()
        DefinedStorage.initialize()
