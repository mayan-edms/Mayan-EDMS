from __future__ import unicode_literals

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from organizations.models import Organization
from organizations.utils import create_default_organization

from ..models import Message

from .literals import TEST_MESSAGE_LABEL, TEST_MESSAGE_TEXT


class MOTDTestCase(TestCase):
    def setUp(self):
        create_default_organization()
        self.motd = Message.on_organization.create(
            label=TEST_MESSAGE_LABEL, message=TEST_MESSAGE_TEXT
        )

    def tearDown(self):
        Organization.objects.all().delete()
        Organization.objects.clear_cache()

    def test_basic(self):
        queryset = Message.on_organization.get_for_now()

        self.assertEqual(queryset.exists(), True)

    def test_start_datetime(self):
        self.motd.start_datetime = timezone.now() - timedelta(days=1)
        self.motd.save()

        queryset = Message.on_organization.get_for_now()

        self.assertEqual(queryset.first(), self.motd)

    def test_end_datetime(self):
        self.motd.start_datetime = timezone.now() - timedelta(days=2)
        self.motd.end_datetime = timezone.now() - timedelta(days=1)
        self.motd.save()

        queryset = Message.on_organization.get_for_now()

        self.assertEqual(queryset.exists(), False)

    def test_enable(self):
        self.motd.enabled = False
        self.motd.save()

        queryset = Message.on_organization.get_for_now()

        self.assertEqual(queryset.exists(), False)
