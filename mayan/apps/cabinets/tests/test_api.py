from __future__ import unicode_literals

from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests import DocumentTestMixin
from mayan.apps.rest_api.tests import BaseAPITestCase

from ..models import Cabinet
from ..permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_remove_document, permission_cabinet_view
)

from .literals import TEST_CABINET_EDITED_LABEL, TEST_CABINET_LABEL
from .mixins import CabinetTestMixin


class CabinetAPITestCase(CabinetTestMixin, BaseAPITestCase):
    def _request_cabinet_create_api_view(self):
        return self.post(
            viewname='rest_api:cabinet-list', data={
                'label': TEST_CABINET_LABEL
            }
        )

    def test_cabinet_create_api_view_no_permission(self):
        cabinet_count = Cabinet.objects.count()

        response = self._request_cabinet_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(cabinet_count, Cabinet.objects.count())

    def test_cabinet_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_cabinet_create)

        response = self._request_cabinet_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cabinet = Cabinet.objects.first()

        self.assertEqual(response.data['id'], cabinet.pk)
        self.assertEqual(response.data['label'], TEST_CABINET_LABEL)

        self.assertEqual(Cabinet.objects.count(), 1)
        self.assertEqual(cabinet.label, TEST_CABINET_LABEL)

    def _request_cabinet_delete_api_view(self):
        return self.delete(
            viewname='rest_api:cabinet-detail', kwargs={
                'pk': self.test_cabinet.pk
            }
        )

    def test_cabinet_delete_api_view_no_permssions(self):
        self._create_test_cabinet()

        cabinet_count = Cabinet.objects.count()

        response = self._request_cabinet_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Cabinet.objects.count(), cabinet_count)

    def test_cabinet_delete_api_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_delete
        )

        cabinet_count = Cabinet.objects.count()

        response = self._request_cabinet_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Cabinet.objects.count(), cabinet_count - 1)

    def _request_cabinet_edit_api_patch_view(self):
        return self.patch(
            data={'label': TEST_CABINET_EDITED_LABEL}, kwargs={
                'pk': self.test_cabinet.pk
            }, viewname='rest_api:cabinet-detail'
        )

    def test_cabinet_edit_api_patch_view_no_pemission(self):
        self._create_test_cabinet()

        cabinet_label = self.test_cabinet.label

        response = self._request_cabinet_edit_api_patch_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(cabinet_label, self.test_cabinet.label)

    def test_cabinet_edit_api_patch_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )

        cabinet_label = self.test_cabinet.label

        response = self._request_cabinet_edit_api_patch_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_cabinet.refresh_from_db()
        self.assertNotEqual(cabinet_label, self.test_cabinet.label)

    def _request_cabinet_edit_api_put_view(self):
        return self.put(
            data={'label': TEST_CABINET_EDITED_LABEL}, kwargs={
                'pk': self.test_cabinet.pk
            }, viewname='rest_api:cabinet-detail'
        )

    def test_cabinet_edit_api_put_view_no_pemission(self):
        self._create_test_cabinet()

        cabinet_label = self.test_cabinet.label

        response = self._request_cabinet_edit_api_put_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(cabinet_label, self.test_cabinet.label)

    def test_cabinet_edit_api_put_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )

        cabinet_label = self.test_cabinet.label

        response = self._request_cabinet_edit_api_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_cabinet.refresh_from_db()
        self.assertNotEqual(cabinet_label, self.test_cabinet.label)

    def _request_cabinet_list_api_view(self):
        return self.get(viewname='rest_api:cabinet-list')

    def test_cabinet_list_api_view_no_permission(self):
        self._create_test_cabinet()

        response = self._request_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_cabinet_list_api_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        response = self._request_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], self.test_cabinet.label
        )


class CabinetDocumentAPITestCase(CabinetTestMixin, DocumentTestMixin, BaseAPITestCase):
    auto_upload_document = False

    def _request_test_cabinet_create_api_view(self, extra_data=None):
        data = {'label': TEST_CABINET_LABEL}

        if extra_data:
            data.update(extra_data)

        return self.post(viewname='rest_api:cabinet-list', data=data)

    def test_cabinet_create_with_single_document(self):
        self.upload_document()

        self.grant_permission(permission=permission_cabinet_create)

        response = self._request_test_cabinet_create_api_view(
            extra_data={
                'documents_pk_list': '{}'.format(
                    self.test_document.pk
                )
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cabinet = Cabinet.objects.first()

        self.assertEqual(response.data['id'], cabinet.pk)
        self.assertEqual(response.data['label'], TEST_CABINET_LABEL)

        self.assertQuerysetEqual(
            cabinet.documents.all(), (repr(self.test_document),)
        )
        self.assertEqual(cabinet.label, TEST_CABINET_LABEL)

    def test_cabinet_create_with_multiple_documents(self):
        self.upload_document()
        self.test_document_2 = self.upload_document()

        self.grant_permission(permission=permission_cabinet_create)

        response = self._request_test_cabinet_create_api_view(
            extra_data={
                'documents_pk_list': '{},{}'.format(
                    self.test_document.pk, self.test_document_2.pk
                )
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cabinet = Cabinet.objects.first()

        self.assertEqual(response.data['id'], cabinet.pk)
        self.assertEqual(response.data['label'], TEST_CABINET_LABEL)

        self.assertEqual(Cabinet.objects.count(), 1)

        self.assertEqual(cabinet.label, TEST_CABINET_LABEL)

        self.assertQuerysetEqual(
            cabinet.documents.all(), map(
                repr, (self.test_document, self.test_document_2)
            )
        )

    def _request_test_cabinet_document_remove_api_view(self):
        return self.delete(
            viewname='rest_api:cabinet-document', kwargs={
                'pk': self.test_cabinet.pk, 'document_pk': self.test_document.pk
            }
        )

    def test_cabinet_document_remove_api_view(self):
        self.upload_document()

        self._create_test_cabinet()
        self.test_cabinet.documents.add(self.test_document)

        self.grant_permission(
            permission=permission_cabinet_remove_document
        )

        response = self._request_test_cabinet_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.test_cabinet.documents.count(), 0)

    def test_cabinet_document_detail_api_view(self):
        self.upload_document()

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
                'pk': self.test_cabinet.pk, 'document_pk': self.test_document.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['uuid'], force_text(self.test_document.uuid)
        )

    def test_cabinet_document_list_api_view(self):
        self.upload_document()

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
            response.data['results'][0]['uuid'], force_text(self.test_document.uuid)
        )

    def test_cabinet_add_document_api_view(self):
        self.upload_document()

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
        self.upload_document()
        self.test_document_2 = self.upload_document()

        self._create_test_cabinet()

        self.grant_permission(permission=permission_cabinet_add_document)
        response = self.post(
            data={
                'documents_pk_list': '{},{}'.format(
                    self.test_document.pk, self.test_document_2.pk
                ),
            }, kwargs={
                'pk': self.test_cabinet.pk
            }, viewname='rest_api:cabinet-document-list'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertQuerysetEqual(
            self.test_cabinet.documents.all(), map(
                repr, (self.test_document, self.test_document_2)
            )
        )
