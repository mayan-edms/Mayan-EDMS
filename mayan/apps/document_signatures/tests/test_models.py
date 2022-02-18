import hashlib

from mayan.apps.django_gpg.events import event_key_created
from mayan.apps.django_gpg.tests.literals import (
    TEST_KEY_PRIVATE_PASSPHRASE, TEST_KEY_PUBLIC_ID
)
from mayan.apps.django_gpg.tests.mixins import KeyTestMixin
from mayan.apps.documents.models import DocumentFile
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import (
    TEST_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_PATH
)

from ..events import (
    event_detached_signature_created, event_detached_signature_deleted,
    event_detached_signature_uploaded
)
from ..models import DetachedSignature, EmbeddedSignature
from ..tasks import task_verify_missing_embedded_signature

from .literals import TEST_SIGNED_DOCUMENT_PATH, TEST_SIGNATURE_ID
from .mixins import DetachedSignatureTestMixin


class DetachedSignaturesTestCase(
    KeyTestMixin, DetachedSignatureTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def test_detached_signature_create(self):
        self._create_test_key_private()

        self._upload_test_document()

        self._clear_events()

        test_detached_signature = DetachedSignature.objects.sign_document_file(
            document_file=self.test_document.file_latest,
            key=self.test_key_private,
            passphrase=TEST_KEY_PRIVATE_PASSPHRASE
        )

        self.assertEqual(DetachedSignature.objects.count(), 1)
        self.assertTrue(test_detached_signature.signature_file.file is not None)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, test_detached_signature)
        self.assertEqual(events[0].actor, self.test_document_file)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_detached_signature_created.id)

    def test_detached_signature_delete(self):
        self._create_test_key_private()

        self._upload_test_document()
        self._upload_test_detached_signature()

        self._clear_events()

        self.test_signature.delete()

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_document_file)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_detached_signature_deleted.id)

    def test_detached_signature_upload_no_key(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._clear_events()

        self._upload_test_detached_signature()

        self.assertEqual(DetachedSignature.objects.count(), 1)

        self.assertEqual(
            self.test_signature.document_file,
            self.test_document.file_latest
        )
        self.assertEqual(self.test_signature.key_id, TEST_KEY_PUBLIC_ID)
        self.assertEqual(self.test_signature.public_key_fingerprint, None)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_signature)
        self.assertEqual(events[0].actor, self.test_document_file)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_detached_signature_uploaded.id)

    def test_detached_signature_upload_with_key(self):
        self._create_test_key_public()
        self.test_document_path = TEST_DOCUMENT_PATH
        self._upload_test_document()

        self._clear_events()

        self._upload_test_detached_signature()

        self.assertEqual(DetachedSignature.objects.count(), 1)

        self.assertEqual(
            self.test_signature.document_file,
            self.test_document.file_latest
        )
        self.assertEqual(self.test_signature.key_id, TEST_KEY_PUBLIC_ID)
        self.assertEqual(
            self.test_signature.public_key_fingerprint,
            self.test_key_public.fingerprint
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_signature)
        self.assertEqual(events[0].actor, self.test_document_file)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_detached_signature_uploaded.id)

    def test_detached_signature_upload_post_key_verify(self):
        self.test_document_path = TEST_DOCUMENT_PATH
        self._upload_test_document()

        self._clear_events()

        self._upload_test_detached_signature()

        self.assertEqual(DetachedSignature.objects.count(), 1)

        self.assertEqual(
            self.test_signature.document_file,
            self.test_document.file_latest
        )
        self.assertEqual(self.test_signature.key_id, TEST_KEY_PUBLIC_ID)
        self.assertEqual(self.test_signature.public_key_fingerprint, None)

        self._create_test_key_public()

        signature = DetachedSignature.objects.first()

        self.assertEqual(
            signature.public_key_fingerprint, self.test_key_public.fingerprint
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, self.test_signature)
        self.assertEqual(events[0].actor, self.test_document_file)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_detached_signature_uploaded.id)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self.test_key_public)
        self.assertEqual(events[1].target, self.test_key_public)
        self.assertEqual(events[1].verb, event_key_created.id)

    def test_detached_signature_upload_post_no_key_verify(self):
        self._create_test_key_public()
        self.test_document_path = TEST_DOCUMENT_PATH
        self._upload_test_document()

        self._clear_events()

        self._upload_test_detached_signature()

        self.assertEqual(DetachedSignature.objects.count(), 1)

        self.assertEqual(
            self.test_signature.document_file,
            self.test_document.file_latest
        )
        self.assertEqual(self.test_signature.key_id, TEST_KEY_PUBLIC_ID)
        self.assertEqual(
            self.test_signature.public_key_fingerprint,
            self.test_key_public.fingerprint
        )

        self.test_key_public.delete()

        signature = DetachedSignature.objects.first()

        self.assertEqual(signature.public_key_fingerprint, None)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_signature)
        self.assertEqual(events[0].actor, self.test_document_file)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_detached_signature_uploaded.id)


class DocumentSignaturesTestCase(
    DetachedSignatureTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def test_unsigned_document_file_method(self):
        TEST_UNSIGNED_DOCUMENT_COUNT = 2
        TEST_SIGNED_DOCUMENT_COUNT = 2

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        for count in range(TEST_UNSIGNED_DOCUMENT_COUNT):
            self._upload_test_document()

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        for count in range(TEST_SIGNED_DOCUMENT_COUNT):
            self._upload_test_document()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT
        )

    def test_method_get_absolute_url(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        EmbeddedSignature.objects.first().get_absolute_url()


class EmbeddedSignaturesTestCase(
    KeyTestMixin, DetachedSignatureTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def test_embedded_signature_no_key(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()
        self.assertEqual(
            signature.document_file, self.test_document.file_latest
        )
        self.assertEqual(signature.key_id, TEST_KEY_PUBLIC_ID)
        self.assertEqual(signature.signature_id, None)

    def test_embedded_signature_post_key_verify(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()
        self.assertEqual(
            signature.document_file, self.test_document.file_latest
        )
        self.assertEqual(signature.key_id, TEST_KEY_PUBLIC_ID)
        self.assertEqual(signature.signature_id, None)

        self._create_test_key_public()

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(signature.signature_id, TEST_SIGNATURE_ID)

    def test_embedded_signature_post_no_key_verify(self):
        self._create_test_key_public()
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(
            signature.document_file, self.test_document.file_latest
        )
        self.assertEqual(signature.key_id, TEST_KEY_PUBLIC_ID)
        self.assertEqual(signature.signature_id, TEST_SIGNATURE_ID)

        self.test_key_public.delete()

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(signature.signature_id, None)

    def test_embedded_signature_with_key(self):
        self._create_test_key_public()
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(
            signature.document_file,
            self.test_document.file_latest
        )
        self.assertEqual(signature.key_id, TEST_KEY_PUBLIC_ID)
        self.assertEqual(
            signature.public_key_fingerprint, self.test_key_public.fingerprint
        )
        self.assertEqual(signature.signature_id, TEST_SIGNATURE_ID)

    def test_task_verify_missing_embedded_signature(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        old_hooks = DocumentFile._post_save_hooks

        DocumentFile._post_save_hooks = {}

        TEST_UNSIGNED_DOCUMENT_COUNT = 2
        TEST_SIGNED_DOCUMENT_COUNT = 2

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        for count in range(TEST_UNSIGNED_DOCUMENT_COUNT):
            self._upload_test_document()

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        for count in range(TEST_SIGNED_DOCUMENT_COUNT):
            self._upload_test_document()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT + TEST_SIGNED_DOCUMENT_COUNT
        )

        DocumentFile._post_save_hooks = old_hooks

        task_verify_missing_embedded_signature.delay()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT
        )

    def test_embedded_signing(self):
        self._create_test_key_private()

        self.test_document_path = TEST_DOCUMENT_PATH
        self._upload_test_document()
        test_document_file_count = self.test_document.files.count()

        with self.test_document.file_latest.open() as file_object:
            file_object.seek(0, 2)
            original_size = file_object.tell()
            file_object.seek(0)
            original_hash = hashlib.sha256(file_object.read()).hexdigest()

        signature = EmbeddedSignature.objects.sign_document_file(
            document_file=self.test_document.file_latest,
            key=self.test_key_private,
            passphrase=TEST_KEY_PRIVATE_PASSPHRASE
        )

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        with signature.document_file.open() as file_object:
            file_object.seek(0, 2)
            new_size = file_object.tell()
            file_object.seek(0)
            new_hash = hashlib.sha256(file_object.read()).hexdigest()

        self.assertEqual(original_size, new_size)
        self.assertEqual(original_hash, new_hash)
        self.assertEqual(
            self.test_document.files.count(), test_document_file_count + 1
        )

        test_document_file_signed = self.test_document.files.last()
        self.assertNotEqual(
            self.test_document_file.checksum,
            test_document_file_signed.checksum
        )
        self.assertEqual(
            self.test_document_file.mimetype,
            test_document_file_signed.mimetype
        )
        self.assertEqual(
            self.test_document_file.pages.count(),
            test_document_file_signed.pages.count()
        )
        self.assertNotEqual(
            self.test_document_file.size,
            test_document_file_signed.size
        )

        with test_document_file_signed.get_download_file_object() as file_object:
            test_document_file_signed_download_file_checksum = hashlib.sha256(
                file_object.read()
            ).hexdigest()

        self.assertEqual(
            test_document_file_signed.checksum,
            test_document_file_signed_download_file_checksum
        )

    def test_document_no_signature(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self.assertEqual(EmbeddedSignature.objects.count(), 0)

    def test_new_signed_file(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        with open(file=TEST_SIGNED_DOCUMENT_PATH, mode='rb') as file_object:
            signed_file = self.test_document.file_new(
                file_object=file_object, comment=''
            )

        self.assertEqual(EmbeddedSignature.objects.count(), 1)

        signature = EmbeddedSignature.objects.first()

        self.assertEqual(signature.document_file, signed_file)
        self.assertEqual(signature.key_id, TEST_KEY_PUBLIC_ID)
