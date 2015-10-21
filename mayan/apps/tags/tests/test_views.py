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
from permissions.tests.literals import TEST_ROLE_LABEL
from user_management.tests import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_GROUP,
    TEST_USER_PASSWORD, TEST_USER_USERNAME
)

from ..models import Tag
from ..permissions import permission_tag_attach, permission_tag_view

from .literals import TEST_TAG_COLOR, TEST_TAG_LABEL


class TagViewTestCase(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            email=TEST_ADMIN_EMAIL, password=TEST_ADMIN_PASSWORD,
            username=TEST_ADMIN_USERNAME
        )

        self.user = get_user_model().objects.create_user(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.group = Group.objects.create(name=TEST_GROUP)
        self.role = Role.objects.create(label=TEST_ROLE_LABEL)
        self.group.user_set.add(self.user)
        self.role.groups.add(self.group)
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

        self.tag = Tag.objects.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

    def tearDown(self):
        self.admin_user.delete()
        self.document_type
        self.group.delete()
        self.role.delete()
        self.tag.delete()
        self.user.delete()

    def test_document_tags_widget_no_permissions(self):
        logged_in = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.user.is_authenticated())

        self.tag.documents.add(self.document)
        response = self.client.get(reverse('documents:document_list'))
        self.assertNotContains(response, text=TEST_TAG_LABEL, status_code=200)

    def test_document_tags_widget_with_permissions(self):
        logged_in = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.user.is_authenticated())

        self.tag.documents.add(self.document)
        self.role.permissions.add(permission_tag_view.stored_permission)
        self.role.permissions.add(permission_document_view.stored_permission)
        response = self.client.get(reverse('documents:document_list'))

        self.assertContains(
            response, text=TEST_TAG_LABEL.replace(' ', '&nbsp;'),
            status_code=200
        )

    def test_document_attach_tag_user_view(self):
        logged_in = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.user.is_authenticated())

        self.assertEqual(
            self.document.tags.count(), 0
        )

        response = self.client.post(
            reverse(
                'tags:tag_attach',
                args=(self.document.pk,)
            ), data={
                'tag': self.tag.pk,
                'user': self.user.pk
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.document.tags.count(), 0
        )

        self.role.permissions.add(permission_tag_attach.stored_permission)
        # permission_tag_view is needed because the form filters the
        # choices
        self.role.permissions.add(permission_tag_view.stored_permission)

        response = self.client.post(
            reverse(
                'tags:tag_attach',
                args=(self.document.pk,)
            ), data={
                'tag': self.tag.pk,
                'user': self.user.pk
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            self.document.tags.all(), (repr(self.tag),)
        )

    def test_document_multiple_attach_tag_user_view(self):
        logged_in = self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.user.is_authenticated())

        self.assertEqual(
            self.document.tags.count(), 0
        )

        response = self.client.post(
            reverse(
                'tags:multiple_documents_tag_attach',
            ), data={
                'id_list': self.document.pk, 'tag': self.tag.pk,
                'user': self.user.pk
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.document.tags.count(), 0
        )

        self.role.permissions.add(permission_tag_attach.stored_permission)

        # permission_tag_view is needed because the form filters the
        # choices
        self.role.permissions.add(permission_tag_view.stored_permission)

        response = self.client.post(
            reverse(
                'tags:multiple_documents_tag_attach',
            ), data={
                'id_list': self.document.pk, 'tag': self.tag.pk,
                'user': self.user.pk
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            self.document.tags.all(), (repr(self.tag),)
        )
