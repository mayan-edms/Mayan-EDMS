from django.apps import apps

from mayan.apps.testing.tests.base import BaseTestCase

from ..finders import MayanAppDirectoriesFinder


class MayanAppDirectoriesFinderTestCase(BaseTestCase):
    def test_app_detection(self):
        app_list = []

        for app_config in apps.get_app_configs():
            if getattr(app_config, 'has_static_media', False):
                if app_config.name not in app_list:
                    app_list.append(app_config.name)

        test_finder = MayanAppDirectoriesFinder()

        for finder_app in test_finder.apps:
            if finder_app.startswith('mayan'):
                self.assertTrue(
                    finder_app in app_list, msg='"{}" is missing'.format(finder_app)
                )

        self.assertEqual(
            len(test_finder.apps), len(test_finder.storages)
        )
