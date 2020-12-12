from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import ThemeTestMixin


class ThemeTestCase(ThemeTestMixin, BaseTestCase):
    def test_method_get_absolute_url(self):
        self._create_test_theme()

        self.assertTrue(self.test_theme.get_absolute_url())
