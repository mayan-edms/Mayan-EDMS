from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from .literals import (
    TEST_USER_2_EMAIL, TEST_USER_2_PASSWORD, TEST_USER_2_USERNAME
)


class UserTestMixin(object):
    def _create_user(self):
        return get_user_model().objects.create_user(
            username=TEST_USER_2_USERNAME, email=TEST_USER_2_EMAIL,
            password=TEST_USER_2_PASSWORD
        )

    def _create_test_user_2(self):
        self.user_2 = get_user_model().objects.create(
            username=TEST_USER_2_USERNAME
        )
