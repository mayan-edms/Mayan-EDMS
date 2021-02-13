from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import AnnouncementTestMixin


class AnnouncementCopyTestCase(
    AnnouncementTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_announcement()
        self.test_object = self.test_announcement
