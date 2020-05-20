from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Cabinet
from ..permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_remove_document, permission_cabinet_view
)

from .mixins import (
    CabinetAPIViewTestMixin, CabinetTestMixin,
    DocumentCabinetAPIViewTestMixin
)


class CabinetAPITestCase(
    CabinetAPIViewTestMixin, CabinetTestMixin, BaseAPITestCase
):
    def test_cabinet_create_api_view_no_permission(self):
        cabinet_count = Cabinet.objects.count()

        response = self._request_test_cabinet_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(cabinet_count, Cabinet.objects.count())

    def test_cabinet_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_cabinet_create)

        response = self._request_test_cabinet_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], self.test_cabinet.pk)
        self.assertEqual(response.data['label'], self.test_cabinet.label)

        self.assertEqual(Cabinet.objects.count(), 1)

    def test_cabinet_delete_api_view_no_permssions(self):
        self._create_test_cabinet()

        cabinet_count = Cabinet.objects.count()

        response = self._request_test_cabinet_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Cabinet.objects.count(), cabinet_count)

    def test_cabinet_delete_api_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_delete
        )

        cabinet_count = Cabinet.objects.count()

        response = self._request_test_cabinet_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Cabinet.objects.count(), cabinet_count - 1)

    def test_cabinet_edit_api_patch_view_no_pemission(self):
        self._create_test_cabinet()

        cabinet_label = self.test_cabinet.label

        response = self._request_test_cabinet_edit_api_patch_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(cabinet_label, self.test_cabinet.label)

    def test_cabinet_edit_api_patch_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )

        cabinet_label = self.test_cabinet.label

        response = self._request_test_cabinet_edit_api_patch_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_cabinet.refresh_from_db()
        self.assertNotEqual(cabinet_label, self.test_cabinet.label)

    def test_cabinet_edit_api_put_view_no_pemission(self):
        self._create_test_cabinet()

        cabinet_label = self.test_cabinet.label

        response = self._request_test_cabinet_edit_api_put_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(cabinet_label, self.test_cabinet.label)

    def test_cabinet_edit_api_put_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )

        cabinet_label = self.test_cabinet.label

        response = self._request_test_cabinet_edit_api_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_cabinet.refresh_from_db()
        self.assertNotEqual(cabinet_label, self.test_cabinet.label)

    def test_cabinet_list_api_view_no_permission(self):
        self._create_test_cabinet()

        response = self._request_test_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_cabinet_list_api_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        response = self._request_test_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], self.test_cabinet.label
        )


class CabinetDocumentAPITestCase(
    CabinetAPIViewTestMixin, CabinetTestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def test_cabinet_create_with_single_document(self):
        self._upload_test_document()

        self.grant_permission(permission=permission_cabinet_create)

        response = self._request_test_cabinet_create_api_view(
            extra_data={
                'documents_pk_list': '{}'.format(
                    self.test_document.pk
                )
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['id'], self.test_cabinet.pk)
        self.assertEqual(response.data['label'], self.test_cabinet.label)

        self.assertQuerysetEqual(
            self.test_cabinet.documents.all(), (repr(self.test_document),)
        )

    def test_cabinet_create_with_multiple_documents(self):
        self._upload_test_document()
        self._upload_test_document()

        documents_pk_list = ','.join(
            [force_text(document.pk) for document in self.test_documents]
        )

        self.grant_permission(permission=permission_cabinet_create)

        response = self._request_test_cabinet_create_api_view(
            extra_data={
                'documents_pk_list': documents_pk_list
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], self.test_cabinet.pk)
        self.assertEqual(response.data['label'], self.test_cabinet.label)

        self.assertEqual(Cabinet.objects.count(), 1)

        self.assertQuerysetEqual(
            qs=self.test_cabinet.documents.all(),
            values=map(repr, self.test_documents)
        )

    def test_cabinet_document_remove_api_view(self):
        self._upload_test_document()

        self._create_test_cabinet()
        self.test_cabinet.documents.add(self.test_document)

        self.grant_permission(
            permission=permission_cabinet_remove_document
        )

        response = self._request_test_cabinet_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.test_cabinet.documents.count(), 0)

    def test_cabinet_document_detail_api_view(self):
        self._upload_test_document()

        self._create_test_cabinet()

        self.test_cabinet.documents.add(self.test_document)

        self.grant_permission(
            permission=permission_cabinet_view
        )
        self.grant_permission(
            permission=permission_document_view
        )
        response = self.get(
            viewname='rest_api:cabinet-document', kwargs={
                'pk': self.test_cabinet.pk,
                'document_pk': self.test_document.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['uuid'], force_text(self.test_document.uuid)
        )

    def test_cabinet_document_list_api_view(self):
        self._upload_test_document()

        self._create_test_cabinet()

        self.test_cabinet.documents.add(self.test_document)

        self.grant_permission(permission=permission_cabinet_view)
        self.grant_permission(permission=permission_document_view)

        response = self.get(
            viewname='rest_api:cabinet-document-list', kwargs={
                'pk': self.test_cabinet.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['uuid'],
            force_text(self.test_document.uuid)
        )

    def test_cabinet_add_document_api_view(self):
        self._upload_test_document()

        self._create_test_cabinet()

        response = self.post(
            data={
                'documents_pk_list': '{}'.format(self.test_document.pk)
            }, kwargs={
                'pk': self.test_cabinet.pk
            }, viewname='rest_api:cabinet-document-list'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertQuerysetEqual(
            self.test_cabinet.documents.all(), (repr(self.test_document),)
        )

    def test_cabinet_add_multiple_documents_api_view(self):
        self._upload_test_document()
        self._upload_test_document()

        documents_pk_list = ','.join(
            [force_text(document.pk) for document in self.test_documents]
        )

        self._create_test_cabinet()

        self.grant_permission(permission=permission_cabinet_add_document)
        response = self.post(
            data={
                'documents_pk_list': documents_pk_list
            }, kwargs={
                'pk': self.test_cabinet.pk
            }, viewname='rest_api:cabinet-document-list'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertQuerysetEqual(
            qs=self.test_cabinet.documents.all(),
            values=map(repr, self.test_documents)
        )


class DocumentCabinetAPITestCase(
    CabinetAPIViewTestMixin, CabinetTestMixin,
    DocumentCabinetAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super(DocumentCabinetAPITestCase, self).setUp()
        self._upload_test_document()
        self._create_test_cabinet()
        self.test_cabinet.documents.add(self.test_document)

    def test_document_cabinet_list_view_no_permission(self):
        response = self._request_test_document_cabinet_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('count' not in response.data)

    def test_document_cabinet_list_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view,
        )

        response = self._request_test_document_cabinet_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_document_cabinet_list_view_with_cabinet_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view,
        )

        response = self._request_test_document_cabinet_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('count' not in response.data)

    def test_document_cabinet_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view,
        )
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view,
        )

        response = self._request_test_document_cabinet_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['count'], Cabinet.objects.all().count()
        )
        self.assertEqual(
            response.data['results'][0]['id'], self.test_cabinet.pk
        )
