from __future__ import unicode_literals

import hashlib
import time

from mayan.apps.django_gpg.models import Key
from mayan.apps.django_gpg.tests.literals import (
    TEST_KEY_DATA, TEST_KEY_PASSPHRASE
)
from mayan.apps.documents.models import DocumentVersion
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import TEST_DOCUMENT_PATH

from ..models import DetachedSignature, EmbeddedSignature
from ..tasks import task_verify_missing_embedded_signature

from .literals import TEST_SIGNED_DOCUMENT_PATH, TEST_KEY_ID, TEST_SIGNATURE_ID
from .mixins import SignaturesTestMixin


class DocumentSignaturesTestCase(SignaturesTestMixin, GenericDocumentTestCase):
    auto_upload_document = False

    def test_embedded_signature_no_key(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self.upload_document()

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()
        self.assertEqual(
            signature.document_version, self.test_document.latest_version
        )
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.signature_id, None)

    def test_embedded_signature_post_key_verify(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self.upload_document()

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()
        self.assertEqual(
            signature.document_version, self.test_document.latest_version
        )
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.signature_id, None)

        self._create_test_key()

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(signature.signature_id, TEST_SIGNATURE_ID)

    def test_embedded_signature_post_no_key_verify(self):
        self._create_test_key()
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self.upload_document()

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(
            signature.document_version, self.test_document.latest_version
        )
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(signature.signature_id, TEST_SIGNATURE_ID)

        self.test_key.delete()

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(signature.signature_id, None)

    def test_embedded_signature_with_key(self):
        self._create_test_key()
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self.upload_document()

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(
            signature.document_version,
            self.test_document.latest_version
        )
        self.assertEqual(signature.key_id, TEST_KEY_ID)
        self.assertEqual(
            signature.public_key_fingerprint, self.test_key.fingerprint
        )
        self.assertEqual(signature.signature_id, TEST_SIGNATURE_ID)

    def test_detached_signature_no_key(self):
        self.test_document_path = TEST_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        self.assertEqual(DetachedSignature.objects.count(), 1)

        self.assertEqual(
            self.test_signature.document_version, self.test_document.latest_version
        )
        self.assertEqual(self.test_signature.key_id, TEST_KEY_ID)
        self.assertEqual(self.test_signature.public_key_fingerprint, None)

    def test_detached_signature_with_key(self):
        self._create_test_key()
        self.test_document_path = TEST_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        self.assertEqual(DetachedSignature.objects.count(), 1)

        self.assertEqual(
            self.test_signature.document_version, self.test_document.latest_version
        )
        self.assertEqual(self.test_signature.key_id, TEST_KEY_ID)
        self.assertEqual(
            self.test_signature.public_key_fingerprint,
            self.test_key.fingerprint
        )

    def test_detached_signature_post_key_verify(self):
        self.test_document_path = TEST_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        self.assertEqual(DetachedSignature.objects.count(), 1)

        self.assertEqual(
            self.test_signature.document_version,
            self.test_document.latest_version
        )
        self.assertEqual(self.test_signature.key_id, TEST_KEY_ID)
        self.assertEqual(self.test_signature.public_key_fingerprint, None)

        self._create_test_key()

        signature = DetachedSignature.objects.first()

        self.assertEqual(
            signature.public_key_fingerprint, self.test_key.fingerprint
        )

    def test_detached_signature_post_no_key_verify(self):
        self._create_test_key()
        self.test_document_path = TEST_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        self.assertEqual(DetachedSignature.objects.count(), 1)

        self.assertEqual(
            self.test_signature.document_version,
            self.test_document.latest_version
        )
        self.assertEqual(self.test_signature.key_id, TEST_KEY_ID)
        self.assertEqual(
            self.test_signature.public_key_fingerprint,
            self.test_key.fingerprint
        )

        self.test_key.delete()

        signature = DetachedSignature.objects.first()

        self.assertEqual(signature.public_key_fingerprint, None)

    def test_document_no_signature(self):
        self.test_document_path = TEST_DOCUMENT_PATH
        self.upload_document()

        self.assertEqual(EmbeddedSignature.objects.count(), 0)

    def test_new_signed_version(self):
        self.test_document_path = TEST_DOCUMENT_PATH
        self.upload_document()

        with open(TEST_SIGNED_DOCUMENT_PATH, mode='rb') as file_object:
            signed_version = self.test_document.new_version(
                file_object=file_object, comment=''
            )

        # Artifical delay since MySQL doesn't store microsecond data in
        # timestamps. Version timestamp is used to determine which version
        # is the latest.
        time.sleep(1)

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(signature.document_version, signed_version)
        self.assertEqual(signature.key_id, TEST_KEY_ID)


class EmbeddedSignaturesTestCase(GenericDocumentTestCase):
    auto_upload_document = False

    def test_unsigned_document_version_method(self):
        TEST_UNSIGNED_DOCUMENT_COUNT = 2
        TEST_SIGNED_DOCUMENT_COUNT = 2

        self.test_document_path = TEST_DOCUMENT_PATH
        for count in range(TEST_UNSIGNED_DOCUMENT_COUNT):
            self.upload_document()

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        for count in range(TEST_SIGNED_DOCUMENT_COUNT):
            self.upload_document()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_versions().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT
        )

    def test_task_verify_missing_embedded_signature(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        old_hooks = DocumentVersion._post_save_hooks

        DocumentVersion._post_save_hooks = {}

        TEST_UNSIGNED_DOCUMENT_COUNT = 2
        TEST_SIGNED_DOCUMENT_COUNT = 2

        self.test_document_path = TEST_DOCUMENT_PATH
        for count in range(TEST_UNSIGNED_DOCUMENT_COUNT):
            self.upload_document()

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        for count in range(TEST_SIGNED_DOCUMENT_COUNT):
            self.upload_document()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_versions().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT + TEST_SIGNED_DOCUMENT_COUNT
        )

        DocumentVersion._post_save_hooks = old_hooks

        task_verify_missing_embedded_signature.delay()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_versions().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT
        )

    def test_signing(self):
        self.test_key = Key.objects.create(key_data=TEST_KEY_DATA)

        self.test_document_path = TEST_DOCUMENT_PATH
        self.upload_document()

        with self.test_document.latest_version.open() as file_object:
            file_object.seek(0, 2)
            original_size = file_object.tell()
            file_object.seek(0)
            original_hash = hashlib.sha256(file_object.read()).hexdigest()

        new_version = EmbeddedSignature.objects.sign_document_version(
            document_version=self.test_document.latest_version,
            key=self.test_key,
            passphrase=TEST_KEY_PASSPHRASE
        )

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        with new_version.open() as file_object:
            file_object.seek(0, 2)
            new_size = file_object.tell()
            file_object.seek(0)
            new_hash = hashlib.sha256(file_object.read()).hexdigest()

        self.assertEqual(original_size, new_size)
        self.assertEqual(original_hash, new_hash)
