from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core import management
from django.test import TestCase

from mayan.apps.common.tests.utils import mute_stdout

from ..models import AutoAdminSingleton


class AutoAdminManagementCommandTestCase(TestCase):
    def setUp(self):
        with mute_stdout():
            management.call_command('createautoadmin')

    def tearDown(self):
        AutoAdminSingleton.objects.all().delete()

    def test_autoadmin_creation(self):
        autoadmin = AutoAdminSingleton.objects.get()
        user = get_user_model().objects.first()

        self.assertEqual(AutoAdminSingleton.objects.count(), 1)

        self.assertEqual(autoadmin.account, user)
        self.assertEqual(autoadmin.account.email, user.email)
        self.assertEqual(autoadmin.password_hash, user.password)
