from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from .literals import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_USER_PASSWORD,
    TEST_USER_USERNAME, TEST_USER_2_EMAIL, TEST_USER_2_PASSWORD,
    TEST_USER_2_USERNAME
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


class UserTestCaseMixin(object):
    def tearDown(self):
        self.client.logout()
        super(UserTestCaseMixin, self).tearDown()

    def login(self, username, password):
        logged_in = self.client.login(username=username, password=password)
        return logged_in

    def login_user(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

    def login_admin_user(self):
        self.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)

    def logout(self):
        self.client.logout()
