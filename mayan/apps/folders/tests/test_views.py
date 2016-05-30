from __future__ import absolute_import, unicode_literals

from documents.permissions import permission_document_view
from documents.tests.test_views import GenericDocumentViewTestCase
from user_management.tests import (
    TEST_USER_USERNAME, TEST_USER_PASSWORD
)

from ..models import Folder
from ..permissions import (
    permission_folder_add_document, permission_folder_create,
    permission_folder_delete, permission_folder_edit,
    permission_folder_remove_document, permission_folder_view
)
from .literals import TEST_FOLDER_LABEL, TEST_FOLDER_EDITED_LABEL


class FolderViewTestCase(GenericDocumentViewTestCase):
    def test_folder_create_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.post(
            'folders:folder_create', data={
                'label': TEST_FOLDER_LABEL
            }
        )

        self.assertEquals(response.status_code, 403)
        self.assertEqual(Folder.on_organization.count(), 0)

    def test_folder_create_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_folder_create.stored_permission
        )

        response = self.post(
            'folders:folder_create', data={
                'label': TEST_FOLDER_LABEL
            }, follow=True
        )
        self.assertContains(response, text='created', status_code=200)
        self.assertEqual(Folder.on_organization.count(), 1)
        self.assertEqual(
            Folder.on_organization.first().label, TEST_FOLDER_LABEL
        )

    def test_folder_create_duplicate_view_with_permission(self):
        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_folder_create.stored_permission
        )

        response = self.post(
            'folders:folder_create', data={
                'label': TEST_FOLDER_LABEL
            }
        )

        self.assertContains(response, text='exists', status_code=200)
        self.assertEqual(Folder.on_organization.count(), 1)
        self.assertEqual(Folder.on_organization.first().pk, folder.pk)

    def test_folder_delete_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        response = self.post('folders:folder_delete', args=(folder.pk,))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Folder.on_organization.count(), 1)

    def test_folder_delete_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_folder_delete.stored_permission
        )

        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        response = self.post(
            'folders:folder_delete', args=(folder.pk,), follow=True
        )

        self.assertContains(response, text='deleted', status_code=200)
        self.assertEqual(Folder.on_organization.count(), 0)

    def test_folder_edit_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        response = self.post(
            'folders:folder_edit', args=(folder.pk,), data={
                'label': TEST_FOLDER_EDITED_LABEL
            }
        )
        self.assertEqual(response.status_code, 403)
        folder = Folder.on_organization.get(pk=folder.pk)
        self.assertEqual(folder.label, TEST_FOLDER_LABEL)

    def test_folder_edit_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_folder_edit.stored_permission
        )

        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        response = self.post(
            'folders:folder_edit', args=(folder.pk,), data={
                'label': TEST_FOLDER_EDITED_LABEL
            }, follow=True
        )

        folder = Folder.on_organization.get(pk=folder.pk)
        self.assertContains(response, text='update', status_code=200)
        self.assertEqual(folder.label, TEST_FOLDER_EDITED_LABEL)

    def test_folder_add_document_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_folder_view.stored_permission)

        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        response = self.post(
            'folders:folder_add_document', args=(self.document.pk,), data={
                'folder': folder.pk,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(folder.documents.count(), 0)

    def test_folder_add_document_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_folder_view.stored_permission)

        self.role.permissions.add(
            permission_folder_add_document.stored_permission
        )

        self.role.permissions.add(
            permission_document_view.stored_permission
        )

        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        response = self.post(
            'folders:folder_add_document', args=(self.document.pk,), data={
                'folder': folder.pk,
            }, follow=True
        )

        folder = Folder.on_organization.get(pk=folder.pk)
        self.assertContains(response, text='added', status_code=200)
        self.assertEqual(folder.documents.count(), 1)
        self.assertQuerysetEqual(
            folder.documents.all(), (repr(self.document),)
        )

    def test_folder_add_multiple_documents_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_folder_view.stored_permission)

        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        response = self.post(
            'folders:folder_add_multiple_documents', data={
                'id_list': (self.document.pk,), 'folder': folder.pk
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(folder.documents.count(), 0)

    def test_folder_add_multiple_documents_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_folder_view.stored_permission)

        self.role.permissions.add(
            permission_folder_add_document.stored_permission
        )

        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        response = self.post(
            'folders:folder_add_multiple_documents', data={
                'id_list': (self.document.pk,), 'folder': folder.pk
            }, follow=True
        )

        folder = Folder.on_organization.get(pk=folder.pk)
        self.assertContains(response, text='added', status_code=200)
        self.assertEqual(folder.documents.count(), 1)
        self.assertQuerysetEqual(
            folder.documents.all(), (repr(self.document),)
        )

    def test_folder_remove_document_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        folder.documents.add(self.document)

        self.assertEqual(folder.documents.count(), 1)

        response = self.post(
            'folders:folder_document_multiple_remove', args=(folder.pk,),
            data={
                'id_list': (self.document.pk,),
            }
        )

        self.assertEqual(response.status_code, 302)

        folder = Folder.on_organization.get(pk=folder.pk)
        self.assertEqual(folder.documents.count(), 1)

    def test_folder_remove_document_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_folder_remove_document.stored_permission
        )

        folder = Folder.on_organization.create(label=TEST_FOLDER_LABEL)

        folder.documents.add(self.document)
        self.assertEqual(folder.documents.count(), 1)

        response = self.post(
            'folders:folder_document_multiple_remove', args=(folder.pk,),
            data={
                'id_list': (self.document.pk,),
            }, follow=True
        )

        folder = Folder.on_organization.get(pk=folder.pk)
        self.assertContains(response, text='removed', status_code=200)
        self.assertEqual(folder.documents.count(), 0)
