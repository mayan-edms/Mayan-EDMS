from __future__ import unicode_literals

import datetime

from django.test import override_settings
from django.utils.encoding import force_text
from django.utils.timezone import now

from rest_framework import status

from documents.tests import DocumentTestMixin
from documents.permissions import permission_document_view
from rest_api.tests import BaseAPITestCase

from ..models import DocumentCheckout
from ..permissions import (
    permission_document_checkout, permission_document_checkout_detail_view
)


@override_settings(OCR_AUTO_OCR=False)
class CheckoutsAPITestCase(DocumentTestMixin, BaseAPITestCase):
    def setUp(self):
        super(CheckoutsAPITestCase, self).setUp()
        self.login_user()

    def _request_checkedout_document_view(self):
        return self.get(
            viewname='rest_api:checkedout-document-view',
            args=(self.checkout.pk,)
        )

    def _checkout_document(self):
        expiration_datetime = now() + datetime.timedelta(days=1)

        self.checkout = DocumentCheckout.objects.checkout_document(
            document=self.document, expiration_datetime=expiration_datetime,
            user=self.admin_user, block_new_version=True
        )

    def test_checkedout_document_view_no_access(self):
        self._checkout_document()
        response = self._request_checkedout_document_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_checkedout_document_view_with_checkout_access(self):
        self._checkout_document()
        self.grant_access(
            permission=permission_document_checkout_detail_view, obj=self.document
        )
        response = self._request_checkedout_document_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_checkedout_document_view_with_document_access(self):
        self._checkout_document()
        self.grant_access(
            permission=permission_document_view, obj=self.document
        )
        response = self._request_checkedout_document_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_checkedout_document_view_with_access(self):
        self._checkout_document()
        self.grant_access(
            permission=permission_document_view, obj=self.document
        )
        self.grant_access(
            permission=permission_document_checkout_detail_view, obj=self.document
        )
        response = self._request_checkedout_document_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['document']['uuid'], force_text(self.document.uuid))

    def _request_document_checkout_view(self):
        return self.post(
            viewname='rest_api:checkout-document-list', data={
                'document_pk': self.document.pk,
                'expiration_datetime': '2099-01-01T12:00'
            }
        )

    def test_document_checkout_no_access(self):
        response = self._request_document_checkout_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DocumentCheckout.objects.count(), 0)

    def test_document_checkout_with_access(self):
        self.grant_access(permission=permission_document_checkout, obj=self.document)
        response = self._request_document_checkout_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            DocumentCheckout.objects.first().document, self.document
        )

    def _request_checkout_list_view(self):
        return self.get(viewname='rest_api:checkout-document-list')

    def test_checkout_list_view_no_access(self):
        self._checkout_document()
        response = self._request_checkout_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response=response, text=self.document.uuid)

    def test_checkout_list_view_with_document_access(self):
        self._checkout_document()
        self.grant_access(
            permission=permission_document_view, obj=self.document
        )
        response = self._request_checkout_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response=response, text=self.document.uuid)

    def test_checkout_list_view_with_checkout_access(self):
        self._checkout_document()
        self.grant_access(
            permission=permission_document_checkout_detail_view, obj=self.document
        )
        response = self._request_checkout_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response=response, text=self.document.uuid)

    def test_checkout_list_view_with_access(self):
        self._checkout_document()
        self.grant_access(
            permission=permission_document_view, obj=self.document
        )
        self.grant_access(
            permission=permission_document_checkout_detail_view, obj=self.document
        )
        response = self._request_checkout_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response=response, text=self.document.uuid)
