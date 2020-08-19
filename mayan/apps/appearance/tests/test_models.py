from mayan.apps.events.tests.mixins import EventTestCaseMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..events import event_theme_created, event_theme_edited

from .mixins import ThemeTestMixin


class ThemeTestCase(EventTestCaseMixin, ThemeTestMixin, BaseTestCase):
    _test_event_object_name = 'test_theme'

    def test_theme_create(self):
        self._create_test_theme()

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_theme_created.id)

    def test_document_remove(self):
        self._create_test_theme()
        self._edit_test_theme()

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_theme_edited.id)

    def test_method_get_absolute_url(self):
        self._create_test_theme()

        self.assertTrue(self.test_theme.get_absolute_url())
