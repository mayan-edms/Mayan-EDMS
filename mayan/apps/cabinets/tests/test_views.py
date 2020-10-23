from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..models import Cabinet
from ..permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_remove_document, permission_cabinet_view
)
from .literals import TEST_CABINET_LABEL, TEST_CABINET_LABEL_EDITED
from .mixins import (
    CabinetTestMixin, CabinetViewTestMixin,
    DocumentCabinetViewTestMixin
)


class CabinetViewTestCase(
    CabinetTestMixin, CabinetViewTestMixin, GenericViewTestCase
):
    def test_cabinet_create_view_no_permission(self):
        response = self._request_test_cabinet_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Cabinet.objects.count(), 0)

    def test_cabinet_create_view_with_permission(self):
        self.grant_permission(permission=permission_cabinet_create)

        response = self._request_test_cabinet_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Cabinet.objects.count(), 1)
        self.assertEqual(Cabinet.objects.first().label, TEST_CABINET_LABEL)

    def test_cabinet_create_duplicate_view_with_permission(self):
        self._create_test_cabinet()
        self.grant_permission(permission=permission_cabinet_create)

        cabinet_count = Cabinet.objects.count()
        cabinet_original = self.test_cabinet

        response = self._request_test_cabinet_create_view()
        # HTTP 200 with error message
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Cabinet.objects.count(), cabinet_count)
        self.assertEqual(Cabinet.objects.first(), cabinet_original)

    def test_cabinet_delete_view_no_permission(self):
        self._create_test_cabinet()

        response = self._request_test_cabinet_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Cabinet.objects.count(), 1)

    def test_cabinet_delete_view_with_access(self):
        self._create_test_cabinet()
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_delete
        )

        response = self._request_test_cabinet_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Cabinet.objects.count(), 0)

    def test_cabinet_edit_view_no_permission(self):
        self._create_test_cabinet()

        response = self._request_test_cabinet_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(self.test_cabinet.label, TEST_CABINET_LABEL)

    def test_cabinet_edit_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )

        response = self._request_test_cabinet_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(self.test_cabinet.label, TEST_CABINET_LABEL_EDITED)

    def test_cabinet_list_view_no_permission(self):
        self._create_test_cabinet()

        response = self._request_test_cabinet_list_view()
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=200
        )

    def test_cabinet_list_view_with_access(self):
        self._create_test_cabinet()
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        response = self._request_test_cabinet_list_view()
        self.assertContains(
            response, text=self.test_cabinet.label, status_code=200
        )


class CabinetChildViewTestCase(
    CabinetTestMixin, CabinetViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super(CabinetChildViewTestCase, self).setUp()
        self._create_test_cabinet()

    def test_cabinet_child_create_view_no_permission(self):
        cabinet_count = Cabinet.objects.count()

        response = self._request_test_cabinet_child_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Cabinet.objects.count(), cabinet_count)

    def test_cabinet_child_create_view_with_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )
        cabinet_count = Cabinet.objects.count()

        response = self._request_test_cabinet_child_create_view()
        self.assertEqual(response.status_code, 302)

        self.test_cabinets[0].refresh_from_db()
        self.assertEqual(Cabinet.objects.count(), cabinet_count + 1)
        self.assertTrue(
            self.test_cabinets[1] in self.test_cabinets[0].get_descendants()
        )

    def test_cabinet_child_delete_view_no_permission(self):
        self._create_test_cabinet_child()

        cabinet_count = Cabinet.objects.count()

        response = self._request_test_cabinet_child_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Cabinet.objects.count(), cabinet_count)

    def test_cabinet_child_delete_view_with_access(self):
        self._create_test_cabinet_child()
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_delete
        )

        cabinet_count = Cabinet.objects.count()

        response = self._request_test_cabinet_child_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Cabinet.objects.count(), cabinet_count - 1)


class CabinetDocumentViewTestCase(
    CabinetTestMixin, CabinetViewTestMixin, GenericDocumentViewTestCase
):
    def test_cabinet_add_document_view_no_permission(self):
        self._create_test_cabinet()

        self.grant_permission(permission=permission_cabinet_view)

        response = self._request_test_document_cabinet_add_view()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(self.test_cabinet.documents.count(), 0)

    def test_cabinet_add_document_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_add_document
        )
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_add_document
        )

        response = self._request_test_document_cabinet_add_view()
        self.assertEqual(response.status_code, 302)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(self.test_cabinet.documents.count(), 1)
        self.assertQuerysetEqual(
            self.test_cabinet.documents.all(), (repr(self.test_document),)
        )

    def test_cabinet_add_multiple_documents_view_no_permission(self):
        self._create_test_cabinet()

        self.grant_permission(permission=permission_cabinet_view)

        response = self._request_test_document_multiple_cabinet_multiple_add_view_cabinet()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(self.test_cabinet.documents.count(), 0)

    def test_cabinet_add_multiple_documents_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_add_document
        )
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_add_document
        )

        response = self._request_test_document_multiple_cabinet_multiple_add_view_cabinet()
        self.assertEqual(response.status_code, 302)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(self.test_cabinet.documents.count(), 1)
        self.assertQuerysetEqual(
            self.test_cabinet.documents.all(), (repr(self.test_document),)
        )

    def test_cabinet_remove_document_view_no_permission(self):
        self._create_test_cabinet()

        self.test_cabinet.documents.add(self.test_document)

        response = self._request_test_document_cabinet_multiple_remove_view()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(self.test_cabinet.documents.count(), 1)

    def test_cabinet_remove_document_view_with_access(self):
        self._create_test_cabinet()

        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet,
            permission=permission_cabinet_remove_document
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_cabinet_remove_document
        )

        response = self._request_test_document_cabinet_multiple_remove_view()
        self.assertEqual(response.status_code, 302)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(self.test_cabinet.documents.count(), 0)

    def test_cabinet_document_list_view_no_permission(self):
        self._create_test_cabinet()
        self.test_cabinet.documents.add(self.test_document)

        response = self._request_test_cabinet_document_list_view()
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=404
        )
        self.assertNotContains(
            response, text=self.test_document.label, status_code=404
        )

    def test_cabinet_document_list_view_with_cabinet_access(self):
        self._create_test_cabinet()
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        response = self._request_test_cabinet_document_list_view()
        self.assertContains(
            response, text=self.test_cabinet.label, status_code=200
        )
        self.assertNotContains(
            response, text=self.test_document.label, status_code=200
        )

    def test_cabinet_document_list_view_with_document_access(self):
        self._create_test_cabinet()
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_cabinet_document_list_view()
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=404
        )
        self.assertNotContains(
            response, text=self.test_document.label, status_code=404
        )

    def test_cabinet_document_list_view_with_full_access(self):
        self._create_test_cabinet()
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_cabinet_document_list_view()
        self.assertContains(
            response, text=self.test_cabinet.label, status_code=200
        )
        self.assertContains(
            response, text=self.test_document.label, status_code=200
        )


class DocumentCabinetViewTestCase(
    CabinetTestMixin, DocumentCabinetViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_cabinet_list_view_no_permission(self):
        self._create_test_cabinet()
        self.test_document.cabinets.add(self.test_cabinet)

        response = self._request_test_document_cabinet_list_view()
        self.assertNotContains(
            response, text=self.test_document.label, status_code=404
        )
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=404
        )

    def test_document_cabinet_list_view_with_document_access(self):
        self._create_test_cabinet()
        self.test_document.cabinets.add(self.test_cabinet)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_cabinet_list_view()
        self.assertContains(
            response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=200
        )

    def test_document_cabinet_list_view_with_cabinet_access(self):
        self._create_test_cabinet()
        self.test_document.cabinets.add(self.test_cabinet)

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        response = self._request_test_document_cabinet_list_view()
        self.assertNotContains(
            response, text=self.test_document.label, status_code=404
        )
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=404
        )

    def test_document_cabinet_list_view_with_full_access(self):
        self._create_test_cabinet()
        self.test_document.cabinets.add(self.test_cabinet)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        response = self._request_test_document_cabinet_list_view()
        self.assertContains(
            response, text=self.test_document.label, status_code=200
        )
        self.assertContains(
            response, text=self.test_cabinet.label, status_code=200
        )
