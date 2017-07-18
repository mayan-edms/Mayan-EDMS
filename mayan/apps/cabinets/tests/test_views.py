from __future__ import absolute_import, unicode_literals

from documents.permissions import permission_document_view
from documents.tests.test_views import GenericDocumentViewTestCase

from ..models import Cabinet
from ..permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_remove_document, permission_cabinet_view
)
from .literals import TEST_CABINET_LABEL, TEST_CABINET_EDITED_LABEL


class CabinetViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(CabinetViewTestCase, self).setUp()
        self.login_user()

    def _request_create_cabinet(self, label):
        return self.post(
            'cabinets:cabinet_create', data={
                'label': TEST_CABINET_LABEL
            }
        )

    def test_cabinet_create_view_no_permission(self):
        response = self._request_create_cabinet(label=TEST_CABINET_LABEL)

        self.assertEquals(response.status_code, 403)
        self.assertEqual(Cabinet.objects.count(), 0)

    def test_cabinet_create_view_with_permission(self):
        self.grant_permission(permission=permission_cabinet_create)

        response = self._request_create_cabinet(label=TEST_CABINET_LABEL)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cabinet.objects.count(), 1)
        self.assertEqual(Cabinet.objects.first().label, TEST_CABINET_LABEL)

    def test_cabinet_create_duplicate_view_with_permission(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)
        self.grant_permission(permission=permission_cabinet_create)
        response = self._request_create_cabinet(label=TEST_CABINET_LABEL)

        # HTTP 200 with error message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cabinet.objects.count(), 1)
        self.assertEqual(Cabinet.objects.first().pk, cabinet.pk)

    def _delete_cabinet(self, cabinet):
        return self.post('cabinets:cabinet_delete', args=(cabinet.pk,))

    def test_cabinet_delete_view_no_permission(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        response = self._delete_cabinet(cabinet=cabinet)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Cabinet.objects.count(), 1)

    def test_cabinet_delete_view_with_permission(self):
        self.grant_permission(permission=permission_cabinet_delete)

        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        response = self._delete_cabinet(cabinet=cabinet)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cabinet.objects.count(), 0)

    def _edit_cabinet(self, cabinet, label):
        return self.post(
            'cabinets:cabinet_edit', args=(cabinet.pk,), data={
                'label': label
            }
        )

    def test_cabinet_edit_view_no_permission(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        response = self._edit_cabinet(
            cabinet=cabinet, label=TEST_CABINET_EDITED_LABEL
        )
        self.assertEqual(response.status_code, 403)
        cabinet.refresh_from_db()
        self.assertEqual(cabinet.label, TEST_CABINET_LABEL)

    def test_cabinet_edit_view_with_permission(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        self.grant_permission(permission=permission_cabinet_edit)

        response = self._edit_cabinet(
            cabinet=cabinet, label=TEST_CABINET_EDITED_LABEL
        )

        self.assertEqual(response.status_code, 302)
        cabinet.refresh_from_db()
        self.assertEqual(cabinet.label, TEST_CABINET_EDITED_LABEL)

    def _add_document_to_cabinet(self, cabinet):
        return self.post(
            'cabinets:cabinet_add_document', args=(self.document.pk,), data={
                'cabinets': cabinet.pk
            }
        )

    def test_cabinet_add_document_view_no_permission(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        self.grant_permission(permission=permission_cabinet_view)

        response = self._add_document_to_cabinet(cabinet=cabinet)

        self.assertContains(
            response, text='Select a valid choice.', status_code=200
        )
        cabinet.refresh_from_db()
        self.assertEqual(cabinet.documents.count(), 0)

    def test_cabinet_add_document_view_with_permission(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        self.grant_permission(permission=permission_cabinet_view)
        self.grant_permission(permission=permission_cabinet_add_document)
        self.grant_permission(permission=permission_document_view)

        response = self._add_document_to_cabinet(cabinet=cabinet)

        cabinet.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(cabinet.documents.count(), 1)
        self.assertQuerysetEqual(
            cabinet.documents.all(), (repr(self.document),)
        )

    def _add_multiple_documents_to_cabinet(self, cabinet):
        return self.post(
            'cabinets:cabinet_add_multiple_documents', data={
                'id_list': (self.document.pk,), 'cabinets': cabinet.pk
            }
        )

    def test_cabinet_add_multiple_documents_view_no_permission(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        self.grant_permission(permission=permission_cabinet_view)

        response = self._add_multiple_documents_to_cabinet(cabinet=cabinet)

        self.assertContains(
            response, text='Select a valid choice', status_code=200
        )
        cabinet.refresh_from_db()
        self.assertEqual(cabinet.documents.count(), 0)

    def test_cabinet_add_multiple_documents_view_with_permission(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        self.grant_permission(permission=permission_cabinet_view)
        self.grant_permission(permission=permission_cabinet_add_document)

        response = self._add_multiple_documents_to_cabinet(cabinet=cabinet)

        self.assertEqual(response.status_code, 302)
        cabinet.refresh_from_db()
        self.assertEqual(cabinet.documents.count(), 1)
        self.assertQuerysetEqual(
            cabinet.documents.all(), (repr(self.document),)
        )

    def _remove_document_from_cabinet(self, cabinet):
        return self.post(
            'cabinets:document_cabinet_remove', args=(self.document.pk,),
            data={
                'cabinets': (cabinet.pk,),
            }
        )

    def test_cabinet_remove_document_view_no_permission(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        cabinet.documents.add(self.document)

        response = self._remove_document_from_cabinet(cabinet=cabinet)

        self.assertContains(
            response, text='Select a valid choice', status_code=200
        )

        cabinet.refresh_from_db()
        self.assertEqual(cabinet.documents.count(), 1)

    def test_cabinet_remove_document_view_with_permission(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        cabinet.documents.add(self.document)

        self.grant_permission(permission=permission_cabinet_remove_document)

        response = self._remove_document_from_cabinet(cabinet=cabinet)

        self.assertEqual(response.status_code, 302)
        cabinet.refresh_from_db()
        self.assertEqual(cabinet.documents.count(), 0)

    def _create_cabinet(self):
        self.cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

    def _request_cabinet_list(self):
        return self.get('cabinets:cabinet_list')

    def test_cabinet_list_view_no_permission(self):
        self._create_cabinet()
        response = self._request_cabinet_list()
        self.assertNotContains(
            response, text=self.cabinet.label, status_code=200
        )

    def test_cabinet_list_view_with_permission(self):
        self._create_cabinet()
        self.grant_permission(permission=permission_cabinet_view)
        response = self._request_cabinet_list()

        self.assertContains(
            response, text=self.cabinet.label, status_code=200
        )
