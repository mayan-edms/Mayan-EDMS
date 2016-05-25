from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from permissions.classes import Permission
from permissions.models import Role
from permissions.tests import TEST_ROLE
from user_management.models import MayanGroup

from ..permissions import permission_settings_view

TEST_EMAIL = 'test_user@example.com'
TEST_GROUP = 'test group'
TEST_PASSWORD = 'testuserpassword'
TEST_USERNAME = 'test_user'


class SmartSettingViewPermissionsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().on_organization.create_user(
            username=TEST_USERNAME, email=TEST_EMAIL,
            password=TEST_PASSWORD
        )
        self.group = MayanGroup.on_organization.create(name=TEST_GROUP)
        self.role = Role.on_organization.create(label=TEST_ROLE)

        self.group.users.add(self.user)
        self.role.groups.add(self.group)

        Permission.invalidate_cache()

        self.client = Client()
        self.client.login(
            username=TEST_USERNAME, password=TEST_PASSWORD
        )

    def tearDown(self):
        self.group.delete()
        self.role.delete()
        self.user.delete()

    def test_view_access_denied(self):
        response = self.client.get(reverse('settings:namespace_list'))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(
            reverse('settings:namespace_detail', args=('common',),)
        )
        self.assertEqual(response.status_code, 403)

    def test_view_access_permitted(self):
        self.role.permissions.add(permission_settings_view.stored_permission)

        response = self.client.get(reverse('settings:namespace_list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse('settings:namespace_detail', args=('common',),)
        )
        self.assertEqual(response.status_code, 200)
