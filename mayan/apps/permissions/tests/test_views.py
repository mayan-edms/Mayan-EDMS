from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from organizations.utils import create_default_organization
from user_management.tests import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL
)

from ..models import Role

from .literals import TEST_ROLE_LABEL, TEST_ROLE_LABEL_EDITED


class PermissionsViewsTestCase(TestCase):
    def setUp(self):
        create_default_organization()
        self.admin_user = get_user_model().on_organization.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

    def test_role_creation_view(self):
        response = self.client.post(
            reverse(
                'permissions:role_create',
            ), data={
                'label': TEST_ROLE_LABEL,
            }, follow=True
        )

        self.assertContains(response, 'created', status_code=200)

        self.assertEqual(Role.on_organization.count(), 1)
        self.assertEqual(Role.on_organization.first().label, TEST_ROLE_LABEL)

    def test_role_delete_view(self):
        role = Role.on_organization.create(label=TEST_ROLE_LABEL)

        response = self.client.post(
            reverse(
                'permissions:role_delete', args=(role.pk,),
            ), follow=True
        )

        self.assertContains(response, 'deleted', status_code=200)

        self.assertEqual(Role.on_organization.count(), 0)

    def test_role_edit_view(self):
        role = Role.on_organization.create(label=TEST_ROLE_LABEL)

        response = self.client.post(
            reverse(
                'permissions:role_edit', args=(role.pk,),
            ), data={
                'label': TEST_ROLE_LABEL_EDITED,
            }, follow=True
        )

        self.assertContains(response, 'update', status_code=200)

        self.assertEqual(Role.on_organization.count(), 1)
        self.assertEqual(
            Role.on_organization.first().label, TEST_ROLE_LABEL_EDITED
        )
