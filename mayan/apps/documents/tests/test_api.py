# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time

from django.core.urlresolvers import reverse
from django.test import override_settings
from django.utils.six import BytesIO

from rest_framework import status

from rest_api.tests import GenericAPITestCase
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from .literals import (
    TEST_DOCUMENT_FILENAME, TEST_DOCUMENT_PATH, TEST_DOCUMENT_TYPE,
    TEST_DOCUMENT_TYPE_EDITED_LABEL, TEST_SMALL_DOCUMENT_CHECKSUM,
    TEST_SMALL_DOCUMENT_PATH,
)
from ..models import Document, DocumentType, HASH_FUNCTION


class DocumentTypeAPITestCase(GenericAPITestCase):
    """
    Test the document type API endpoints
    """

    def test_document_type_create(self):
        self.assertEqual(DocumentType.on_organization.all().count(), 0)

        self.client.post(
            reverse('rest_api:documenttype-list'), data={
                'label': TEST_DOCUMENT_TYPE
            }
        )

        self.assertEqual(DocumentType.on_organization.all().count(), 1)
        self.assertEqual(
            DocumentType.on_organization.all().first().label,
            TEST_DOCUMENT_TYPE
        )

    def test_document_type_edit_via_put(self):
        document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        response = self.client.put(
            reverse('rest_api:documenttype-detail', args=(document_type.pk,)),
            {'label': TEST_DOCUMENT_TYPE_EDITED_LABEL}
        )

        self.assertEqual(response.status_code, 200)

        document_type = DocumentType.on_organization.get(pk=document_type.pk)
        self.assertEqual(document_type.label, TEST_DOCUMENT_TYPE_EDITED_LABEL)

    def test_document_type_edit_via_patch(self):
        document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        response = self.client.patch(
            reverse('rest_api:documenttype-detail', args=(document_type.pk,)),
            {'label': TEST_DOCUMENT_TYPE_EDITED_LABEL}
        )
        self.assertEqual(response.status_code, 200)

        document_type = DocumentType.on_organization.get(pk=document_type.pk)
        self.assertEqual(document_type.label, TEST_DOCUMENT_TYPE_EDITED_LABEL)
        document_type.delete()

    def test_document_type_delete(self):
        document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        self.client.delete(
            reverse('rest_api:documenttype-detail', args=(document_type.pk,))
        )

        self.assertEqual(DocumentType.on_organization.all().count(), 0)


@override_settings(OCR_AUTO_OCR=False)
class DocumentAPITestCase(GenericAPITestCase):
    """
    Test document API endpoints
    """

    def setUp(self):
        super(DocumentAPITestCase, self).setUp()
        self.document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

    def tearDown(self):
        self.document_type.delete()
        super(DocumentAPITestCase, self).tearDown()

    def test_document_upload(self):
        with open(TEST_DOCUMENT_PATH) as file_descriptor:
            response = self.client.post(
                reverse('rest_api:document-list'), {
                    'document_type': self.document_type.pk,
                    'file': file_descriptor
                }
            )

        document_data = response.data

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(Document.on_organization.count(), 1)

        document = Document.on_organization.first()

        self.assertEqual(document.pk, document_data['id'])

        self.assertEqual(document.versions.count(), 1)

        self.assertEqual(document.exists(), True)
        self.assertEqual(document.size, 272213)

        self.assertEqual(document.file_mimetype, 'application/pdf')
        self.assertEqual(document.file_mime_encoding, 'binary')
        self.assertEqual(document.label, TEST_DOCUMENT_FILENAME)
        self.assertEqual(
            document.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(document.page_count, 47)

    def test_document_move_to_trash(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object,
            )

        self.client.delete(
            reverse('rest_api:document-detail', args=(document.pk,))
        )

        self.assertEqual(Document.on_organization.count(), 0)
        self.assertEqual(Document.trash.count(), 1)

    def test_document_new_version_upload(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object,
            )

        # Artifical delay since MySQL doesn't store microsecond data in
        # timestamps. Version timestamp is used to determine which version
        # is the latest.
        time.sleep(1)
        with open(TEST_DOCUMENT_PATH) as file_descriptor:
            response = self.client.post(
                reverse(
                    'rest_api:document-version-list', args=(document.pk,)
                ), {
                    'comment': '',
                    'file': file_descriptor,
                }
            )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(document.versions.count(), 2)
        self.assertEqual(document.exists(), True)
        self.assertEqual(document.size, 272213)
        self.assertEqual(document.file_mimetype, 'application/pdf')
        self.assertEqual(document.file_mime_encoding, 'binary')
        self.assertEqual(
            document.checksum,
            'c637ffab6b8bb026ed3784afdb07663fddc60099853fae2be93890852a69ecf3'
        )
        self.assertEqual(document.page_count, 47)

    def test_document_version_revert(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object,
            )

        # Needed by MySQL as milliseconds value is not store in timestamp field
        time.sleep(1)

        with open(TEST_DOCUMENT_PATH) as file_object:
            document.new_version(file_object=file_object)

        self.assertEqual(document.versions.count(), 2)

        document_version = document.versions.first()

        self.client.post(
            reverse(
                'rest_api:documentversion-revert', args=(document_version.pk,)
            )
        )

        self.assertEqual(document.versions.count(), 1)

        self.assertEqual(document_version, document.latest_version)

    def test_document_download(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object,
            )

        response = self.client.get(
            reverse(
                'rest_api:document-download', args=(document.pk,)
            )
        )
        buf = BytesIO()
        buf.write(response.content)

        self.assertEqual(
            HASH_FUNCTION(buf.getvalue()), TEST_SMALL_DOCUMENT_CHECKSUM
        )

        del(buf)

    def test_document_version_download(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object,
            )

        response = self.client.get(
            reverse(
                'rest_api:documentversion-download',
                args=(document.latest_version.pk,)
            )
        )
        buf = BytesIO()
        buf.write(response.content)

        self.assertEqual(
            HASH_FUNCTION(buf.getvalue()), TEST_SMALL_DOCUMENT_CHECKSUM
        )

        del(buf)

    def test_trashed_document_delete_from_trash(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object,
            )

        document.delete()

        self.assertEqual(Document.on_organization.count(), 0)
        self.assertEqual(Document.trash.count(), 1)

        self.client.delete(
            reverse('rest_api:trasheddocument-detail', args=(document.pk,))
        )

        self.assertEqual(Document.trash.count(), 0)

    def test_trashed_document_restore(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object,
            )

        document.delete()

        self.client.post(
            reverse('rest_api:trasheddocument-restore', args=(document.pk,))
        )

        self.assertEqual(Document.trash.count(), 0)
        self.assertEqual(Document.on_organization.count(), 1)
