from __future__ import unicode_literals

import datetime
import time

from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase
from django.utils.timezone import now

from common.literals import TIME_DELTA_UNIT_DAYS
from documents.models import DocumentType
from documents.tests.literals import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL,
    TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)

from ..models import DocumentCheckout


class DocumentCheckoutViewTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

    def tearDown(self):
        self.document_type.delete()
        self.admin_user.delete()

    def test_checkout_view(self):
        response = self.client.post(
            reverse(
                'checkouts:checkout_document', args=(self.document.pk,),
            ), data={
                'expiration_datetime_0': 2,
                'expiration_datetime_1': TIME_DELTA_UNIT_DAYS,
                'block_new_version': True
            }, follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertTrue(self.document.is_checked_out())

        self.assertTrue(
            DocumentCheckout.objects.is_document_checked_out(
                document=self.document
            )
        )

    def test_checkin_view(self):
        expiration_datetime = now() + datetime.timedelta(days=1)

        DocumentCheckout.objects.checkout_document(
            document=self.document, expiration_datetime=expiration_datetime,
            user=self.admin_user, block_new_version=True
        )

        self.assertTrue(self.document.is_checked_out())

        response = self.client.post(
            reverse(
                'checkouts:checkin_document', args=(self.document.pk,),
            ), follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertFalse(self.document.is_checked_out())

        self.assertFalse(
            DocumentCheckout.objects.is_document_checked_out(
                document=self.document
            )
        )
