from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.tests.tests.base import BaseTestCase

from .mixins import MOTDTestMixin


class MOTDCopyTestCase(MOTDTestMixin, ObjectCopyTestMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_message()
        self.test_object = self.test_message
