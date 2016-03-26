from __future__ import unicode_literals

import os
import time

from django.conf import settings
from django.core.files import File
from django.test import TestCase, override_settings

from django_gpg.models import Key
from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_PATH, TEST_DOCUMENT_TYPE

from ..models import DetachedSignature, EmbeddedSignature

TEST_SIGNED_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf.gpg'
)
TEST_SIGNATURE_FILE_PATH = os.path.join(
    settings.BASE_DIR, 'contrib', 'sample_documents', 'mayan_11_1.pdf.sig'
)
TEST_KEY_FILE = os.path.join(
    settings.BASE_DIR, 'contrib', 'sample_documents',
    'key0x5F3F7F75D210724D.asc'
)
TEST_KEY_ID = '5F3F7F75D210724D'
TEST_SIGNATURE_ID = 'XVkoGKw35yU1iq11dZPiv7uAY7k'


@override_settings(OCR_AUTO_OCR=False)
class DocumentSignaturesTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

    def tearDown(self):
        self.document_type.delete()

    def test_embedded_signature_no_key(self):
        with open(TEST_SIGNED_DOCUMENT_PATH) as file_object:
            signed_document = self.document_type.new_document(
                file_object=file_object
            )

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(
            signature.document_version, signed_document.latest_version
        )
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.signature_id, None)

    def test_embedded_signature_post_key_verify(self):
        with open(TEST_SIGNED_DOCUMENT_PATH) as file_object:
            signed_document = self.document_type.new_document(
                file_object=file_object
            )

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(
            signature.document_version, signed_document.latest_version
        )
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.signature_id, None)

        with open(TEST_KEY_FILE) as file_object:
            key = Key.objects.create(key_data=file_object.read())

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(signature.signature_id, TEST_SIGNATURE_ID)

    def test_embedded_signature_post_no_key_verify(self):
        with open(TEST_KEY_FILE) as file_object:
            key = Key.objects.create(key_data=file_object.read())

        with open(TEST_SIGNED_DOCUMENT_PATH) as file_object:
            signed_document = self.document_type.new_document(
                file_object=file_object
            )

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(
            signature.document_version, signed_document.latest_version
        )
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.signature_id, TEST_SIGNATURE_ID)

        key.delete()

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(signature.signature_id, None)

    def test_embedded_signature_with_key(self):
        with open(TEST_KEY_FILE) as file_object:
            key = Key.objects.create(key_data=file_object.read())

        with open(TEST_SIGNED_DOCUMENT_PATH) as file_object:
            self.signed_document = self.document_type.new_document(
                file_object=file_object
            )

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(
            signature.document_version,
            self.signed_document.latest_version
        )
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.public_key_fingerprint, key.fingerprint)
        self.assertEqual(signature.signature_id, TEST_SIGNATURE_ID)

    def test_detached_signature_no_key(self):
        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.assertEqual(DetachedSignature.objects.count(), 1)

        signature = DetachedSignature.objects.first()

        self.assertEqual(signature.document_version, document.latest_version)
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.public_key_fingerprint, None)

    def test_detached_signature_with_key(self):
        with open(TEST_KEY_FILE) as file_object:
            key = Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.assertEqual(DetachedSignature.objects.count(), 1)

        signature = DetachedSignature.objects.first()

        self.assertEqual(signature.document_version, document.latest_version)
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.public_key_fingerprint, key.fingerprint)

    def test_detached_signature_post_key_verify(self):
        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.assertEqual(DetachedSignature.objects.count(), 1)

        signature = DetachedSignature.objects.first()

        self.assertEqual(signature.document_version, document.latest_version)
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.public_key_fingerprint, None)

        with open(TEST_KEY_FILE) as file_object:
            key = Key.objects.create(key_data=file_object.read())

        signature = DetachedSignature.objects.first()

        self.assertEqual(signature.public_key_fingerprint, key.fingerprint)

    def test_detached_signature_post_no_key_verify(self):
        with open(TEST_KEY_FILE) as file_object:
            key = Key.objects.create(key_data=file_object.read())

        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH) as file_object:
            DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.assertEqual(DetachedSignature.objects.count(), 1)

        signature = DetachedSignature.objects.first()

        self.assertEqual(signature.document_version, document.latest_version)
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.public_key_fingerprint, key.fingerprint)

        key.delete()

        signature = DetachedSignature.objects.first()

        self.assertEqual(signature.public_key_fingerprint, None)

    def test_document_no_signature(self):
        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        self.assertEqual(EmbeddedSignature.objects.count(), 0)

    def test_new_signed_version(self):
        with open(TEST_DOCUMENT_PATH) as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNED_DOCUMENT_PATH) as file_object:
            signed_version = document.new_version(
                file_object=file_object, comment='test comment 1'
            )

        # Artifical delay since MySQL doesn't store microsecond data in
        # timestamps. Version timestamp is used to determine which version
        # is the latest.
        time.sleep(2)

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(signature.document_version, signed_version)
        self.assertEqual(signature.key_id, TEST_KEY_ID)
