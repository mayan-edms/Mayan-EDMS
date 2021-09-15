from mayan.apps.django_gpg.tests.mixins import KeyTestMixin
from mayan.apps.documents.models import DocumentFile
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH

from ..models import DetachedSignature, EmbeddedSignature
from ..permissions import permission_document_file_signature_verify

from .literals import (
    TEST_SIGNED_DOCUMENT_COUNT, TEST_SIGNED_DOCUMENT_PATH,
    TEST_UNSIGNED_DOCUMENT_COUNT
)
from .mixins import DetachedSignatureTestMixin, SignatureToolsViewTestMixin


class SignatureToolsViewTestCase(
    KeyTestMixin, DetachedSignatureTestMixin, SignatureToolsViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        class DetachedSignatureProxy(DetachedSignature):
            def save(self, *args, **kwargs):
                return super(DetachedSignature, self).save(*args, **kwargs)

            class Meta:
                proxy = True

        class EmbeddedSignatureProxy(EmbeddedSignature):
            def save(self, *args, **kwargs):
                return super(EmbeddedSignature, self).save(*args, **kwargs)

            class Meta:
                proxy = True

        cls.DetachedSignatureProxy = DetachedSignatureProxy
        cls.EmbeddedSignatureProxy = EmbeddedSignatureProxy

    def test_missing_signature_verify_view_no_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        old_hooks = DocumentFile._post_save_hooks
        DocumentFile._post_save_hooks = {}

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

        self._clear_events()

        response = self._request_all_test_document_file_signature_verify_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT + TEST_SIGNED_DOCUMENT_COUNT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_missing_signature_verify_view_with_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        old_hooks = DocumentFile._post_save_hooks
        DocumentFile._post_save_hooks = {}

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

        self.grant_permission(
            permission=permission_document_file_signature_verify
        )

        self._clear_events()

        response = self._request_all_test_document_file_signature_verify_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_missing_signature_verify_view_with_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        old_hooks = DocumentFile._post_save_hooks
        DocumentFile._post_save_hooks = {}

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

        self.grant_permission(
            permission=permission_document_file_signature_verify
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_all_test_document_file_signature_verify_view()

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_refresh_view_no_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature = self.DetachedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        signature = self.EmbeddedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        self._clear_events()

        response = self._request_all_test_document_file_signature_refresh_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            DetachedSignature.objects.first().date_time, None
        )
        self.assertEqual(
            EmbeddedSignature.objects.first().date_time, None
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_refresh_view_with_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature = self.DetachedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        signature = self.EmbeddedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        self.grant_permission(
            permission=permission_document_file_signature_verify
        )

        self._clear_events()

        response = self._request_all_test_document_file_signature_refresh_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            DetachedSignature.objects.first().date_time, None
        )
        self.assertNotEqual(
            EmbeddedSignature.objects.first().date_time, None
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_signature_refresh_view_with_permission(self):
        # Silence converter logging.
        self._silence_logger(name='mayan.apps.converter.backends')

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature = self.DetachedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        signature = self.EmbeddedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        self.test_documents[0].delete()
        self.test_documents[1].delete()

        self.grant_permission(
            permission=permission_document_file_signature_verify
        )

        self._clear_events()

        response = self._request_all_test_document_file_signature_refresh_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            DetachedSignature.objects.first().date_time, None
        )
        self.assertNotEqual(
            EmbeddedSignature.objects.first().date_time, None
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
