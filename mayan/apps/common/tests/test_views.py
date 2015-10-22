from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from permissions import Permission
from permissions.models import Role
from permissions.tests.literals import TEST_ROLE_LABEL
from user_management.tests import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL, TEST_GROUP,
    TEST_USER_EMAIL, TEST_USER_USERNAME, TEST_USER_PASSWORD
)


class GenericViewTestCase(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.user = get_user_model().objects.create_user(
            username=TEST_USER_USERNAME, email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD
        )

        self.group = Group.objects.create(name=TEST_GROUP)
        self.role = Role.objects.create(label=TEST_ROLE_LABEL)
        self.group.user_set.add(self.user)
        self.role.groups.add(self.group)
        Permission.invalidate_cache()

    def tearDown(self):
        self.admin_user.delete()
        self.client.logout()
        self.group.delete()
        self.role.delete()
        self.user.delete()

    def get(self, viewname, *args, **kwargs):
        data = kwargs.pop('data', {})
        follow = kwargs.pop('follow', False)

        return self.client.get(
            reverse(viewname=viewname, *args, **kwargs),
            data=data, follow=follow
        )

    def login(self, username, password):
        logged_in = self.client.login(username=username, password=password)

        user = get_user_model().objects.get(username=username)

        self.assertTrue(logged_in)
        self.assertTrue(user.is_authenticated())

    def post(self, viewname, *args, **kwargs):
        data = kwargs.pop('data', {})
        follow = kwargs.pop('follow', False)

        return self.client.post(
            reverse(viewname=viewname, *args, **kwargs),
            data=data, follow=follow
        )


class CommonViewTestCase(GenericViewTestCase):
    def test_about_view(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.get('common:about_view')
        self.assertContains(response, text='About', status_code=200)
