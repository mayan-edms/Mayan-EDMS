from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import MessageTestMixin


class MessageModelTestCase(MessageTestMixin, BaseTestCase):
    def test_method_get_absolute_url(self):
        self._create_test_message()

        self.assertTrue(self.test_message.get_absolute_url())
