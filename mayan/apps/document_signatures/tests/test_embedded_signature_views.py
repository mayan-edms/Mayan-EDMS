from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.django_gpg.tests.mixins import KeyTestMixin
from mayan.apps.documents.events import (
    event_document_file_created, event_document_file_edited,
    event_document_version_created, event_document_version_page_created
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH

from ..events import event_embedded_signature_created
from ..permissions import permission_document_file_sign_embedded

from .mixins import EmbeddedSignatureViewTestMixin


class EmbeddedSignaturesViewTestCase(
    KeyTestMixin, EmbeddedSignatureViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_embedded_signature_create_view_with_no_permission(self):
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

    def test_embedded_signature_create_view_with_document_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_embedded
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

    def test_embedded_signature_create_view_with_key_access(self):
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

    def test_embedded_signature_create_view_with_full_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_embedded
        )
        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        self._clear_events()

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            str(self.test_document.file_latest.pk) in response.url
        )

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 5)

        test_document_file = self.test_document.file_latest
        test_document_version = self.test_document.versions.last()

        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document_file)
        self.assertEqual(events[0].verb, event_document_file_created.id)

        self.assertEqual(events[1].action_object, self.test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_edited.id)

        self.assertEqual(events[2].action_object, self.test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_version)
        self.assertEqual(events[2].verb, event_document_version_created.id)

        self.assertEqual(events[3].action_object, test_document_version)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version.pages.first())
        self.assertEqual(
            events[3].verb, event_document_version_page_created.id
        )

        self.assertEqual(
            events[4].action_object,
            self.test_document.file_latest.signatures.first().embeddedsignature
        )
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(events[4].target, self.test_document_file)
        self.assertEqual(events[4].verb, event_embedded_signature_created.id)

    def test_trashed_document_embedded_signature_create_view_with_full_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_embedded
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
