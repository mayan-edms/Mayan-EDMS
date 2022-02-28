from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import AnnouncementTestMixin


class AnnouncementCopyTestCase(
    AnnouncementTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_announcement()
        self._test_object = self._test_announcement
