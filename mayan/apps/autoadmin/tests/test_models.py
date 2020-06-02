import logging

from mayan.apps.tests.tests.base import BaseTestCase
from mayan.apps.tests.tests.utils import mute_stdout

from ..models import AutoAdminSingleton
from ..settings import setting_username

from .literals import TEST_ADMIN_USER_PASSWORD


class AutoAdminHandlerTestCase(BaseTestCase):
    def test_post_admin_creation(self):
        logging.disable(logging.INFO)

        with mute_stdout():
            AutoAdminSingleton.objects.create_autoadmin()

        self.assertEqual(
            AutoAdminSingleton.objects.get().account.username,
            setting_username.value
        )

        user = AutoAdminSingleton.objects.get().account

        user.set_password(TEST_ADMIN_USER_PASSWORD)
        user.save(update_fields=['password'])

        self.assertEqual(AutoAdminSingleton.objects.get().account, None)

    def test_double_creation(self):
        with mute_stdout():
            AutoAdminSingleton.objects.create_autoadmin()

        self.assertEqual(AutoAdminSingleton.objects.count(), 1)

        logging.disable(logging.ERROR)

        AutoAdminSingleton.objects.create_autoadmin()
        self.assertEqual(AutoAdminSingleton.objects.count(), 1)
