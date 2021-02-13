from datetime import timedelta

from django.utils import timezone

from mayan.apps.testing.tests.base import BaseTestCase

from ..models import Announcement

from .mixins import AnnouncementTestMixin


class AnnouncementModelTestCase(AnnouncementTestMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_announcement()

    def test_basic(self):
        queryset = Announcement.objects.get_for_now()

        self.assertEqual(queryset.exists(), True)

    def test_start_datetime(self):
        self.test_announcement.start_datetime = timezone.now() - timedelta(days=1)
        self.test_announcement.save()

        queryset = Announcement.objects.get_for_now()

        self.assertEqual(queryset.first(), self.test_announcement)

    def test_end_datetime(self):
        self.test_announcement.start_datetime = timezone.now() - timedelta(days=2)
        self.test_announcement.end_datetime = timezone.now() - timedelta(days=1)
        self.test_announcement.save()

        queryset = Announcement.objects.get_for_now()

        self.assertEqual(queryset.exists(), False)

    def test_enable(self):
        self.test_announcement.enabled = False
        self.test_announcement.save()

        queryset = Announcement.objects.get_for_now()

        self.assertEqual(queryset.exists(), False)
