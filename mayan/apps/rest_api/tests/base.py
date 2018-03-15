from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase

from common.tests.mixins import UserMixin
from permissions.classes import Permission
from smart_settings.classes import Namespace
from user_management.tests import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_USER_USERNAME,
    TEST_USER_PASSWORD
)


class BaseAPITestCase(UserMixin, APITestCase):
    """
    API test case class that invalidates permissions and smart settings
    """
    def setUp(self):
        super(BaseAPITestCase, self).setUp()
        Namespace.invalidate_cache_all()
        Permission.invalidate_cache()

    def tearDown(self):
        self.client.logout()
        super(BaseAPITestCase, self).tearDown()

    def delete(self, viewname=None, path=None, *args, **kwargs):
        data = kwargs.pop('data', {})
        follow = kwargs.pop('follow', False)

        if viewname:
            path = reverse(viewname=viewname, *args, **kwargs)

        return self.client.delete(
            path=path, data=data, follow=follow
        )

    def get(self, viewname=None, path=None, *args, **kwargs):
        data = kwargs.pop('data', {})
        follow = kwargs.pop('follow', False)

        if viewname:
            path = reverse(viewname=viewname, *args, **kwargs)

        return self.client.get(
            path=path, data=data, follow=follow
        )

    def login(self, username, password):
        logged_in = self.client.login(username=username, password=password)

        user = get_user_model().objects.get(username=username)

        self.assertTrue(logged_in)
        self.assertTrue(user.is_authenticated)
        return user.is_authenticated

    def login_user(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

    def login_admin_user(self):
        self.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)

    def logout(self):
        self.client.logout()

    def patch(self, viewname=None, path=None, *args, **kwargs):
        data = kwargs.pop('data', {})
        follow = kwargs.pop('follow', False)

        if viewname:
            path = reverse(viewname=viewname, *args, **kwargs)

        return self.client.patch(
            path=path, data=data, follow=follow
        )

    def post(self, viewname=None, path=None, *args, **kwargs):
        data = kwargs.pop('data', {})
        follow = kwargs.pop('follow', False)

        if viewname:
            path = reverse(viewname=viewname, *args, **kwargs)

        return self.client.post(
            path=path, data=data, follow=follow
        )

    def put(self, viewname=None, path=None, *args, **kwargs):
        data = kwargs.pop('data', {})
        follow = kwargs.pop('follow', False)

        if viewname:
            path = reverse(viewname=viewname, *args, **kwargs)

        return self.client.put(
            path=path, data=data, follow=follow
        )
