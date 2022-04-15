import warnings

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig

from .literals import MESSAGE_SQLITE_WARNING
from .patches import patch_Migration
from .utils import check_for_sqlite
from .warnings import DatabaseWarning


class DatabasesApp(MayanAppConfig):
    has_tests = True
    name = 'mayan.apps.databases'
    verbose_name = _('Databases')

    def ready(self):
        super().ready()

        if check_for_sqlite():
            warnings.warn(
                category=DatabaseWarning,
                message=str(MESSAGE_SQLITE_WARNING)
            )

        patch_Migration()
