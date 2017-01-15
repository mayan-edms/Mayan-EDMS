from __future__ import absolute_import, unicode_literals

from documents.permissions import permission_document_view
from documents.tests.test_views import GenericDocumentViewTestCase

from ..models import Folder
from ..permissions import (
    permission_folder_add_document, permission_folder_create,
    permission_folder_delete, permission_folder_edit,
    permission_folder_remove_document, permission_folder_view
)
from .literals import TEST_FOLDER_LABEL, TEST_FOLDER_EDITED_LABEL


class FolderViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(FolderViewTestCase, self).setUp()
        self.login_user()

    def _create_folder(self, label):
        return self.post(
            'folders:folder_create', data={
                'label': TEST_FOLDER_LABEL
            }
        )

    def test_folder_create_view_no_permission(self):
        response = self._create_folder(label=TEST_FOLDER_LABEL)

        self.assertEquals(response.status_code, 403)
        self.assertEqual(Folder.objects.count(), 0)

    def test_folder_create_view_with_permission(self):
        self.grant(permission=permission_folder_create)

        response = self._create_folder(label=TEST_FOLDER_LABEL)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Folder.objects.count(), 1)
        self.assertEqual(Folder.objects.first().label, TEST_FOLDER_LABEL)

    def test_folder_create_duplicate_view_with_permission(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        self.grant(permission=permission_folder_create)

        response = self._create_folder(label=TEST_FOLDER_LABEL)

        self.assertContains(response, text='exists', status_code=200)
        self.assertEqual(Folder.objects.count(), 1)
        self.assertEqual(Folder.objects.first().pk, folder.pk)

    def _delete_folder(self, folder):
        return self.post('folders:folder_delete', args=(folder.pk,))

    def test_folder_delete_view_no_permission(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        response = self._delete_folder(folder=folder)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Folder.objects.count(), 1)

    def test_folder_delete_view_with_permission(self):
        self.grant(permission=permission_folder_delete)

        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        response = self._delete_folder(folder=folder)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Folder.objects.count(), 0)

    def _edit_folder(self, folder, label):
        return self.post(
            'folders:folder_edit', args=(folder.pk,), data={
                'label': label
            }
        )

    def test_folder_edit_view_no_permission(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        response = self._edit_folder(
            folder=folder, label=TEST_FOLDER_EDITED_LABEL
        )
        self.assertEqual(response.status_code, 403)
        folder.refresh_from_db()
        self.assertEqual(folder.label, TEST_FOLDER_LABEL)

    def test_folder_edit_view_with_permission(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        self.grant(permission=permission_folder_edit)

        response = self._edit_folder(
            folder=folder, label=TEST_FOLDER_EDITED_LABEL
        )

        self.assertEqual(response.status_code, 302)
        folder.refresh_from_db()
        self.assertEqual(folder.label, TEST_FOLDER_EDITED_LABEL)

    def _add_document_to_folder(self, folder):
        return self.post(
            'folders:folder_add_document', args=(self.document.pk,), data={
                'folders': folder.pk
            }
        )

    def test_folder_add_document_view_no_permission(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        self.grant(permission=permission_folder_view)

        response = self._add_document_to_folder(folder=folder)

        self.assertContains(
            response, text='Select a valid choice.', status_code=200
        )
        folder.refresh_from_db()
        self.assertEqual(folder.documents.count(), 0)

    def test_folder_add_document_view_with_permission(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        self.grant(permission=permission_folder_view)
        self.grant(permission=permission_folder_add_document)
        self.grant(permission=permission_document_view)

        response = self._add_document_to_folder(folder=folder)

        folder.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(folder.documents.count(), 1)
        self.assertQuerysetEqual(
            folder.documents.all(), (repr(self.document),)
        )

    def _add_multiple_documents_to_folder(self, folder):
        return self.post(
            'folders:folder_add_multiple_documents', data={
                'id_list': (self.document.pk,), 'folders': folder.pk
            }
        )

    def test_folder_add_multiple_documents_view_no_permission(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        self.grant(permission=permission_folder_view)

        response = self._add_multiple_documents_to_folder(folder=folder)

        self.assertContains(
            response, text='Select a valid choice', status_code=200
        )
        folder.refresh_from_db()
        self.assertEqual(folder.documents.count(), 0)

    def test_folder_add_multiple_documents_view_with_permission(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        self.grant(permission=permission_folder_view)
        self.grant(permission=permission_folder_add_document)

        response = self._add_multiple_documents_to_folder(folder=folder)

        self.assertEqual(response.status_code, 302)
        folder.refresh_from_db()
        self.assertEqual(folder.documents.count(), 1)
        self.assertQuerysetEqual(
            folder.documents.all(), (repr(self.document),)
        )

    def _remove_document_from_folder(self, folder):
        return self.post(
            'folders:document_folder_remove', args=(self.document.pk,),
            data={
                'folders': (folder.pk,),
            }
        )

    def test_folder_remove_document_view_no_permission(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        folder.documents.add(self.document)

        response = self._remove_document_from_folder(folder=folder)

        self.assertContains(
            response, text='Select a valid choice', status_code=200
        )

        folder.refresh_from_db()
        self.assertEqual(folder.documents.count(), 1)

    def test_folder_remove_document_view_with_permission(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        folder.documents.add(self.document)

        self.grant(permission=permission_folder_remove_document)

        response = self._remove_document_from_folder(folder=folder)

        self.assertEqual(response.status_code, 302)
        folder.refresh_from_db()
        self.assertEqual(folder.documents.count(), 0)
