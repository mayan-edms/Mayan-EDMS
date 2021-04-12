from mayan.apps.common.apps import MayanAppConfig


class MOTDApp(MayanAppConfig):
    has_tests = False
    has_translations = False
    name = 'mayan.apps.motd'
