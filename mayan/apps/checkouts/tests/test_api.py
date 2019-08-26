from __future__ import unicode_literals

from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.documents.tests import DocumentTestMixin
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.rest_api.tests import BaseAPITestCase

from ..models import DocumentCheckout
from ..permissions import (
    permission_document_check_out, permission_document_check_out_detail_view
)

from .mixins import (
    DocumentCheckoutsAPIViewTestMixin, DocumentCheckoutTestMixin
)


class CheckoutsAPITestCase(
    DocumentCheckoutsAPIViewTestMixin, DocumentCheckoutTestMixin,
    DocumentTestMixin, BaseAPITestCase
):
    def test_checkedout_document_view_no_access(self):
        self._check_out_test_document()

        response = self._request_checkedout_document_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_checkedout_document_view_with_checkout_access(self):
        self._check_out_test_document()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        response = self._request_checkedout_document_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_checkedout_document_view_with_document_access(self):
        self._check_out_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_checkedout_document_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_checkedout_document_view_with_access(self):
        self._check_out_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        response = self._request_checkedout_document_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['document']['uuid'],
            force_text(self.test_document.uuid)
        )

    def test_document_checkout_no_access(self):
        response = self._request_test_document_check_out_view()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DocumentCheckout.objects.count(), 0)

    def test_document_checkout_with_access(self):
        self.grant_access(permission=permission_document_check_out, obj=self.test_document)

        response = self._request_test_document_check_out_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            DocumentCheckout.objects.first().document, self.test_document
        )

    def test_checkout_list_view_no_access(self):
        self._check_out_test_document()

        response = self._request_checkout_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response=response, text=self.test_document.uuid)

    def test_checkout_list_view_with_document_access(self):
        self._check_out_test_document()
        self.grant_access(
            permission=permission_document_view, obj=self.test_document
        )

        response = self._request_checkout_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response=response, text=self.test_document.uuid)

    def test_checkout_list_view_with_checkout_access(self):
        self._check_out_test_document()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        response = self._request_checkout_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response=response, text=self.test_document.uuid)

    def test_checkout_list_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            permission=permission_document_view, obj=self.test_document
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        response = self._request_checkout_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response=response, text=self.test_document.uuid)
