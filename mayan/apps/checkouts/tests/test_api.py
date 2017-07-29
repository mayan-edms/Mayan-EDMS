from __future__ import unicode_literals

import datetime

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import override_settings
from django.utils.encoding import force_text
from django.utils.timezone import now

from rest_framework.test import APITestCase

from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_PATH
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from ..models import DocumentCheckout


@override_settings(OCR_AUTO_OCR=False)
class CheckoutAPITestCase(APITestCase):
    def setUp(self):
        super(CheckoutAPITestCase, self).setUp()

        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object,
            )

    def tearDown(self):
        self.document_type.delete()
        super(CheckoutAPITestCase, self).tearDown()

    def test_document_checkout_get_view(self):
        expiration_datetime = now() + datetime.timedelta(days=1)

        DocumentCheckout.objects.checkout_document(
            document=self.document, expiration_datetime=expiration_datetime,
            user=self.admin_user, block_new_version=True
        )

        response = self.client.get(reverse('rest_api:checkout-document-list'))

        self.assertEqual(
            response.data['results'][0]['document']['uuid'],
            force_text(self.document.uuid)
        )

    def test_document_checkout_post_view(self):
        response = self.client.post(
            reverse('rest_api:checkout-document-list'), data={
                'document_pk': self.document.pk,
                'expiration_datetime': '2099-01-01T12:00'
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            DocumentCheckout.objects.first().document, self.document
        )
