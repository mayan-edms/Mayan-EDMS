from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.django_gpg.tests.mixins import KeyTestMixin
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import (
    TEST_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_PATH
)

from ..events import (
    event_detached_signature_created, event_detached_signature_deleted,
    event_detached_signature_uploaded
)
from ..models import DetachedSignature
from ..permissions import (
    permission_document_file_sign_detached,
    permission_document_file_signature_delete,
    permission_document_file_signature_download,
    permission_document_file_signature_upload,
    permission_document_file_signature_view
)

from .mixins import (
    DetachedSignatureViewTestMixin, DetachedSignatureTestMixin
)


class DetachedSignaturesViewTestCase(
    KeyTestMixin, DetachedSignatureTestMixin, DetachedSignatureViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_detached_signature_create_view_with_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self._clear_events()

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_detached_signature_create_view_with_document_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_detached
        )

        self._clear_events()

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_detached_signature_create_view_with_key_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        self._clear_events()

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_detached_signature_create_view_with_full_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_detached
        )
        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        self._clear_events()

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object,
            self.test_document_file.signatures.first().detachedsignature
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_detached_signature_created.id)

    def test_trashed_document_detached_signature_create_view_with_full_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_detached
        )
        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_detached_signature_delete_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature_count = DetachedSignature.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        self._clear_events()

        response = self._request_test_document_file_signature_detached_delete_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(DetachedSignature.objects.count(), signature_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_detached_signature_delete_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature_count = DetachedSignature.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_delete
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        self._clear_events()

        response = self._request_test_document_file_signature_detached_delete_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            DetachedSignature.objects.count(), signature_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_document_file)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_detached_signature_deleted.id)

    def test_trashed_document_signature_delete_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature_count = DetachedSignature.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_delete
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_signature_detached_delete_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            DetachedSignature.objects.count(), signature_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_download_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self._clear_events()

        response = self._request_test_document_file_signature_detached_download_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_download_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_download
        )

        self.expected_content_types = ('application/octet-stream',)

        self._clear_events()

        response = self._request_test_document_file_signature_detached_download_view()

        with self.test_signature.signature_file as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
            )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_signature_download_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_download
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_signature_detached_download_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_upload_view_no_permission(self):
        self.test_document_path = TEST_DOCUMENT_PATH

        signature_count = DetachedSignature.objects.count()

        self._upload_test_document()

        self._clear_events()

        response = self._request_test_document_file_signature_detached_upload_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(DetachedSignature.objects.count(), signature_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_upload_view_with_access(self):
        self.test_document_path = TEST_DOCUMENT_PATH
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_upload
        )

        signature_count = DetachedSignature.objects.count()

        self._clear_events()

        response = self._request_test_document_file_signature_detached_upload_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            DetachedSignature.objects.count(), signature_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object,
            self.test_document.file_latest.signatures.first().detachedsignature
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_detached_signature_uploaded.id)

    def test_trashed_document_signature_upload_view_with_access(self):
        self.test_document_path = TEST_DOCUMENT_PATH
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_upload
        )

        self.test_document.delete()

        signature_count = DetachedSignature.objects.count()

        self._clear_events()

        response = self._request_test_document_file_signature_detached_upload_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(DetachedSignature.objects.count(), signature_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
