from __future__ import unicode_literals

import datetime
import time

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.utils.timezone import now

from documents.exceptions import NewDocumentVersionNotAllowed
from documents.models import DocumentType
from documents.tests.literals import (
    TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)
from organizations.tests.base import OrganizationTestCase
from user_management.tests.literals import (
    TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD
)

from ..exceptions import DocumentAlreadyCheckedOut, DocumentNotCheckedOut
from ..models import DocumentCheckout


@override_settings(OCR_AUTO_OCR=False)
class DocumentCheckoutTestCase(OrganizationTestCase):
    def setUp(self):
        super(DocumentCheckoutTestCase, self).setUp()
        self.admin_user = get_user_model().on_organization.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def tearDown(self):
        self.document_type.delete()
        super(DocumentCheckoutTestCase, self).tearDown()

    def test_document_checkout(self):
        expiration_datetime = now() + datetime.timedelta(days=1)

        DocumentCheckout.on_organization.checkout_document(
            document=self.document, expiration_datetime=expiration_datetime,
            user=self.admin_user, block_new_version=True
        )

        self.assertTrue(self.document.is_checked_out())
        self.assertTrue(
            DocumentCheckout.on_organization.is_document_checked_out(
                document=self.document
            )
        )

    def test_version_creation_blocking(self):
        expiration_datetime = now() + datetime.timedelta(days=1)

        DocumentCheckout.on_organization.checkout_document(
            document=self.document, expiration_datetime=expiration_datetime,
            user=self.admin_user, block_new_version=True
        )

        with self.assertRaises(NewDocumentVersionNotAllowed):
            with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
                self.document.new_version(file_object=file_object)

    def test_checkin_in(self):
        expiration_datetime = now() + datetime.timedelta(days=1)

        DocumentCheckout.on_organization.checkout_document(
            document=self.document, expiration_datetime=expiration_datetime,
            user=self.admin_user, block_new_version=True
        )

        self.document.check_in()

        self.assertFalse(self.document.is_checked_out())
        self.assertFalse(
            DocumentCheckout.on_organization.is_document_checked_out(
                document=self.document
            )
        )

    def test_double_checkout(self):
        expiration_datetime = now() + datetime.timedelta(days=1)

        DocumentCheckout.on_organization.checkout_document(
            document=self.document, expiration_datetime=expiration_datetime,
            user=self.admin_user, block_new_version=True
        )

        with self.assertRaises(DocumentAlreadyCheckedOut):
            DocumentCheckout.on_organization.checkout_document(
                document=self.document,
                expiration_datetime=expiration_datetime, user=self.admin_user,
                block_new_version=True
            )

    def test_checkin_without_checkout(self):
        with self.assertRaises(DocumentNotCheckedOut):
            self.document.check_in()

    def test_auto_checkin(self):
        expiration_datetime = now() + datetime.timedelta(seconds=1)

        DocumentCheckout.on_organization.checkout_document(
            document=self.document, expiration_datetime=expiration_datetime,
            user=self.admin_user, block_new_version=True
        )

        time.sleep(2)

        DocumentCheckout.on_organization.check_in_expired_check_outs()

        self.assertFalse(self.document.is_checked_out())
