from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from documents.models import DocumentType
from documents.permissions import permission_document_view
from documents.tests import TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
from permissions import Permission
from permissions.models import Role
from permissions.tests.literals import (
    TEST_GROUP, TEST_ROLE_LABEL, TEST_USER_PASSWORD, TEST_USER_USERNAME
)

from ..models import Tag
from ..permissions import permission_tag_view

from .literals import TEST_TAG_COLOR, TEST_TAG_LABEL


class TagViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.group = Group.objects.create(name=TEST_GROUP)
        self.role = Role.objects.create(label=TEST_ROLE_LABEL)
        Permission.invalidate_cache()

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

        self.client = Client()
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.user.is_authenticated())

        self.tag = Tag.objects.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

        self.tag.documents.add(self.document)

        self.group.user_set.add(self.user)
        self.role.groups.add(self.group)
        self.role.permissions.add(permission_document_view.stored_permission)

    def tearDown(self):
        self.group.delete()
        self.role.delete()
        self.tag.delete()
        self.user.delete()
        self.document_type

    def test_document_tags_widget_no_permissions(self):
        response = self.client.get(reverse('documents:document_list'))
        self.assertNotContains(response, text=TEST_TAG_LABEL, status_code=200)

    def test_document_tags_widget_with_permissions(self):
        self.role.permissions.add(permission_tag_view.stored_permission)
        response = self.client.get(reverse('documents:document_list'))
        self.assertContains(
            response, text=TEST_TAG_LABEL.replace(' ', '&nbsp;'),
            status_code=200
        )
