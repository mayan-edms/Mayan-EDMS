from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import search_model_document
from mayan.apps.dynamic_search.tests.mixins import SearchTestMixin

from ..permissions import permission_signature_capture_view
from ..search import search_model_signature_capture

from .mixins import SignatureCaptureTestMixin


class DocumentSignatureCaptureSearchTestCase(
    SignatureCaptureTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    auto_create_test_document_stub = True
    auto_upload_test_document = False
    auto_create_test_signature_capture = True

    def _do_test_search(self, query):
        return self.search_backend.search(
            search_model=search_model_document, query=query,
            user=self._test_case_user
        )

    def test_search_by_text_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__text': self._test_signature_capture.text
            }
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_text_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__text': self._test_signature_capture.text
            }
        )

        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_search_by_text_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__text': self._test_signature_capture.text
            }
        )

        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_first_name_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__user__first_name': self._test_signature_capture.user.first_name
            }
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_first_name_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__user__first_name': self._test_signature_capture.user.first_name
            }
        )

        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_search_by_user_first_name_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__user__first_name': self._test_signature_capture.user.first_name
            }
        )

        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_last_name_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__user__last_name': self._test_signature_capture.user.last_name
            }
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_last_name_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__user__last_name': self._test_signature_capture.user.last_name
            }
        )

        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_search_by_user_last_name_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__user__last_name': self._test_signature_capture.user.last_name
            }
        )

        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_username_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__user__username': self._test_signature_capture.user.username
            }
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_username_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__user__username': self._test_signature_capture.user.username
            }
        )

        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_search_by_user_username_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'signature_captures__user__username': self._test_signature_capture.user.username
            }
        )

        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class SignatureCaptureSearchTestCase(
    SignatureCaptureTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    auto_create_test_document_stub = True
    auto_upload_test_document = False
    auto_create_test_signature_capture = True

    def _do_test_search(self, query):
        return self.search_backend.search(
            search_model=search_model_signature_capture, query=query,
            user=self._test_case_user
        )

    def test_search_by_document_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__label': self._test_signature_capture.document.label
            }
        )
        self.assertTrue(self._test_signature_capture not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_document_label_with_access(self):
        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__label': self._test_signature_capture.document.label
            }
        )

        self.assertTrue(self._test_signature_capture in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_document_type_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__document_type__label': self._test_signature_capture.document.document_type.label
            }
        )
        self.assertTrue(self._test_signature_capture not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_document_type_label_with_access(self):
        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__document_type__label': self._test_signature_capture.document.document_type.label
            }
        )

        self.assertTrue(self._test_signature_capture in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_text_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'text': self._test_signature_capture.text}
        )
        self.assertTrue(self._test_signature_capture not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_text_with_access(self):
        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'text': self._test_signature_capture.text}
        )

        self.assertTrue(self._test_signature_capture in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_username_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'user__username': self._test_case_user.username}
        )

        self.assertTrue(self._test_signature_capture not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_username_with_access(self):
        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'user__username': self._test_case_user.username}
        )

        self.assertTrue(self._test_signature_capture in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_first_name_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'user__first_name': self._test_case_user.first_name}
        )

        self.assertTrue(self._test_signature_capture not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_first_name_with_access(self):
        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'user__first_name': self._test_case_user.first_name}
        )

        self.assertTrue(self._test_signature_capture in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_last_name_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'user__last_name': self._test_case_user.last_name}
        )

        self.assertTrue(self._test_signature_capture not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_by_user_last_name_with_access(self):
        self.grant_access(
            obj=self._test_signature_capture,
            permission=permission_signature_capture_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'user__last_name': self._test_case_user.last_name}
        )

        self.assertTrue(self._test_signature_capture in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
