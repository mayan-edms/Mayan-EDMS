from __future__ import unicode_literals

import datetime

from django.utils.timezone import now

from common.literals import TIME_DELTA_UNIT_DAYS
from documents.models import DocumentType
from documents.tests.literals import (
    TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)
from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import DocumentCheckout


class OrganizationDocumentCheckoutTestCase(OrganizationViewTestCase):
    def create_document(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.document_type = DocumentType.on_organization.create(
                label=TEST_DOCUMENT_TYPE
            )

            with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
                self.document = self.document_type.new_document(
                    file_object=file_object
                )

    def check_out_document(self):
        self.create_document()
        expiration_datetime = now() + datetime.timedelta(days=1)

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):

            DocumentCheckout.on_organization.checkout_document(
                document=self.document,
                expiration_datetime=expiration_datetime, user=self.user,
                block_new_version=True
            )

    def test_checkout_info(self):
        self.check_out_document()

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.get(
                'checkouts:checkout_info', args=(self.document.pk,),
                follow=True
            )

            self.assertEquals(response.status_code, 200)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.get(
                'checkouts:checkout_info', args=(self.document.pk,),
                follow=True
            )

            self.assertEquals(response.status_code, 404)

    def test_check_in(self):
        self.check_out_document()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.get(
                'checkouts:checkin_document', args=(self.document.pk,),
                follow=True
            )

            self.assertEquals(response.status_code, 404)
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.assertTrue(self.document.is_checked_out())

    def test_check_out(self):
        self.create_document()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'checkouts:checkout_document', args=(self.document.pk,), data={
                    'expiration_datetime_0': 2,
                    'expiration_datetime_1': TIME_DELTA_UNIT_DAYS,
                    'block_new_version': True
                }, follow=True
            )

            self.assertEquals(response.status_code, 404)
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.assertFalse(self.document.is_checked_out())

    def test_checkout_list(self):
        self.check_out_document()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.get('checkouts:checkout_list')

            self.assertNotContains(
                response, text=self.document.label, status_code=200
            )
