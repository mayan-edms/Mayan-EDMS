from mayan.apps.common.apps import MayanAppConfig

from .patches import patch_Migration


class DatabasesApp(MayanAppConfig):
    has_tests = False
    name = 'mayan.apps.databases'

    def ready(self):
        super().ready()

        patch_Migration()
