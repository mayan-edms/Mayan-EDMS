from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from documents.models import DocumentType
from documents.tests import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL,
    TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)

from ..models import Folder

from .literals import TEST_FOLDER_LABEL, TEST_FOLDER_EDITED_LABEL


class FolderViewTestCase(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

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
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

    def tearDown(self):
        self.admin_user.delete()
        self.document_type

    def test_folder_create_view(self):
        response = self.client.post(
            reverse('folders:folder_create'), data={
                'label': TEST_FOLDER_LABEL
            }, follow=True
        )

        self.assertContains(response, text='created', status_code=200)
        self.assertEqual(Folder.objects.count(), 1)
        self.assertEqual(Folder.objects.first().label, TEST_FOLDER_LABEL)
        self.assertEqual(Folder.objects.first().user, self.admin_user)

    def test_folder_delete_view(self):
        folder = Folder.objects.create(
            label=TEST_FOLDER_LABEL, user=self.admin_user
        )

        response = self.client.post(
            reverse('folders:folder_delete', args=(folder.pk,)), follow=True
        )

        self.assertContains(response, text='deleted', status_code=200)
        self.assertEqual(Folder.objects.count(), 0)

    def test_folder_edit_view(self):
        folder = Folder.objects.create(
            label=TEST_FOLDER_LABEL, user=self.admin_user
        )

        response = self.client.post(
            reverse('folders:folder_edit', args=(folder.pk,)), data = {
                'label': TEST_FOLDER_EDITED_LABEL
            }, follow=True
        )

        folder = Folder.objects.get(pk=folder.pk)
        self.assertContains(response, text='saved', status_code=200)
        self.assertEqual(folder.label, TEST_FOLDER_EDITED_LABEL)
        self.assertEqual(folder.user, self.admin_user)

    def test_folder_add_document_view(self):
        folder = Folder.objects.create(
            label=TEST_FOLDER_LABEL, user=self.admin_user
        )

        response = self.client.post(
            reverse('folders:folder_add_document', args=(self.document.pk,)),
            data={
                'folder': folder.pk,
            }, follow=True
        )

        folder = Folder.objects.get(pk=folder.pk)
        self.assertContains(response, text='added', status_code=200)
        self.assertEqual(folder.documents.count(), 1)
        self.assertQuerysetEqual(
            folder.documents.all(), (repr(self.document),)
        )

    def test_folder_add_multiple_documents_view(self):
        folder = Folder.objects.create(
            label=TEST_FOLDER_LABEL, user=self.admin_user
        )

        response = self.client.post(
            reverse('folders:folder_add_multiple_documents'), data={
                'id_list': (self.document.pk,),
                'folder': folder.pk
            }, follow=True
        )

        folder = Folder.objects.get(pk=folder.pk)
        self.assertContains(response, text='added', status_code=200)
        self.assertEqual(folder.documents.count(), 1)
        self.assertQuerysetEqual(
            folder.documents.all(), (repr(self.document),)
        )

    def test_folder_remove_document_view(self):
        folder = Folder.objects.create(
            label=TEST_FOLDER_LABEL, user=self.admin_user,
        )

        folder.documents.add(self.document)

        self.assertEqual(folder.documents.count(), 1)

        response = self.client.post(
            reverse(
                'folders:folder_document_multiple_remove', args=(folder.pk,)
            ), data={
                'id_list': (self.document.pk,),
            }, follow=True
        )

        folder = Folder.objects.get(pk=folder.pk)
        self.assertContains(response, text='removed', status_code=200)
        self.assertEqual(folder.documents.count(), 0)
