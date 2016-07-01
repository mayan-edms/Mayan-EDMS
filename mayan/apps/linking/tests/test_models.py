# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test import override_settings

from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_PATH, TEST_DOCUMENT_TYPE
from organizations.tests import OrganizationTestCase
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from ..models import SmartLink

from .literals import TEST_SMART_LINK_LABEL, TEST_SMART_LINK_DYNAMIC_LABEL


@override_settings(OCR_AUTO_OCR=False)
class SmartLinkTestCase(OrganizationTestCase):
    def setUp(self):
        super(SmartLinkTestCase, self).setUp()

        self.document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

        self.user = get_user_model().on_organization.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

    def tearDown(self):
        self.document_type.delete()
        super(SmartLinkTestCase, self).tearDown()

    def test_dynamic_label(self):
        smart_link = SmartLink.on_organization.create(
            label=TEST_SMART_LINK_LABEL,
            dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
        )
        smart_link.document_types.add(self.document_type)

        self.assertEqual(
            smart_link.get_dynamic_label(document=self.document),
            self.document.label
        )
