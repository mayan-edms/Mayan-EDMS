from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import MessageTestMixin


class MessageCopyTestCase(MessageTestMixin, ObjectCopyTestMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_message()
        self.test_object = self.test_message
