from __future__ import unicode_literals

from mayan.apps.common.serialization import yaml_load
from mayan.apps.smart_settings.classes import NamespaceMigration


class OCRSettingMigration(NamespaceMigration):
    """
    From version 0001 to 0002 backend arguments are no longer quoted
    but YAML valid too. Changed in version 3.3.
    """
    def ocr_backend_arguments_0001(self, value):
        return yaml_load(
            stream=value or '{}',
        )
