from django.utils.encoding import force_text

from mayan.apps.documents.models import DocumentFile
from mayan.apps.documents.permissions import (
    permission_document_file_new, permission_document_file_view,
    permission_document_view
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..events import (
    event_document_checked_in, event_document_checked_out,
    event_document_forcefully_checked_in
)
from ..exceptions import DocumentAlreadyCheckedOut, DocumentNotCheckedOut
from ..literals import STATE_CHECKED_OUT, STATE_LABELS
from ..permissions import (
    permission_document_check_in, permission_document_check_in_override,
    permission_document_check_out, permission_document_check_out_detail_view
)

from .mixins import DocumentCheckoutTestMixin, DocumentCheckoutViewTestMixin


class DocumentCheckoutViewTestCase(
    DocumentCheckoutTestMixin, DocumentCheckoutViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_check_in_get_view_no_permission(self):
        self._check_out_test_document()

        self._clear_events()

        response = self._request_test_document_check_in_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_in_get_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_check_in
        )

        self._clear_events()

        response = self._request_test_document_check_in_get_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_check_in_get_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_check_in
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_in_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_in_post_view_no_permission(self):
        self._check_out_test_document()

        self._clear_events()

        response = self._request_test_document_check_in_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_in_post_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_check_in
        )

        self._clear_events()

        response = self._request_test_document_check_in_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_checked_in.id)

    def test_trashed_document_check_in_post_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_check_in
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_in_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_check_in_post_view_no_permission(self):
        # Upload second document.
        self._upload_test_document()

        self._check_out_test_document(document=self.test_documents[0])
        self._check_out_test_document(document=self.test_documents[1])

        self._clear_events()

        response = self._request_test_document_multiple_check_in_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_documents[0].is_checked_out())
        self.assertTrue(self.test_documents[1].is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_check_in_post_view_with_document_0_access(self):
        # Upload second document.
        self._upload_test_document()

        self._check_out_test_document(document=self.test_documents[0])
        self._check_out_test_document(document=self.test_documents[1])

        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_check_in
        )

        self._clear_events()

        response = self._request_test_document_multiple_check_in_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(self.test_documents[0].is_checked_out())
        self.assertTrue(self.test_documents[1].is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_documents[0])
        self.assertEqual(events[0].verb, event_document_checked_in.id)

    def test_document_multiple_check_in_post_view_with_access(self):
        # Upload second document.
        self._upload_test_document()

        self._check_out_test_document(document=self.test_documents[0])
        self._check_out_test_document(document=self.test_documents[1])

        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_check_in
        )
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_check_in
        )

        self._clear_events()

        response = self._request_test_document_multiple_check_in_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(self.test_documents[0].is_checked_out())
        self.assertFalse(self.test_documents[1].is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_documents[0])
        self.assertEqual(events[0].verb, event_document_checked_in.id)

        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].target, self.test_documents[1])
        self.assertEqual(events[1].verb, event_document_checked_in.id)

    def test_document_check_out_get_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_check_out_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_out
        )

        self._clear_events()

        response = self._request_test_document_check_out_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_check_out_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_out
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_out_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_post_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_check_out_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_post_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_out
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self._clear_events()

        response = self._request_test_document_check_out_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_checked_out.id)

    def test_trashed_document_check_out_post_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_out
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_out_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_check_out_post_view_no_permission(self):
        # Upload second document.
        self._upload_test_document()

        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_check_out_detail_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_check_out_detail_view
        )

        self._clear_events()

        response = self._request_test_document_multiple_check_out_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertFalse(self.test_documents[0].is_checked_out())
        self.assertFalse(self.test_documents[1].is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_check_out_post_view_with_document_access(self):
        # Upload second document.
        self._upload_test_document()

        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_check_out
        )
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_check_out_detail_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_check_out_detail_view
        )

        self._clear_events()

        response = self._request_test_document_multiple_check_out_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.test_documents[0].is_checked_out())
        self.assertFalse(self.test_documents[1].is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_documents[0])
        self.assertEqual(events[0].verb, event_document_checked_out.id)

    def test_document_multiple_check_out_post_view_with_access(self):
        # Upload second document.
        self._upload_test_document()

        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_check_out
        )
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_check_out
        )
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_check_out_detail_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_check_out_detail_view
        )

        self._clear_events()

        response = self._request_test_document_multiple_check_out_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.test_documents[0].is_checked_out())
        self.assertTrue(self.test_documents[1].is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_documents[0])
        self.assertEqual(events[0].verb, event_document_checked_out.id)

        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].target, self.test_documents[1])
        self.assertEqual(events[1].verb, event_document_checked_out.id)

    def test_document_check_out_detail_view_no_permission(self):
        self._check_out_test_document()

        self._clear_events()

        response = self._request_test_document_check_out_detail_view()

        self.assertNotContains(
            response, text=STATE_LABELS[STATE_CHECKED_OUT], status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_detail_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self._clear_events()

        response = self._request_test_document_check_out_detail_view()
        self.assertContains(
            response, text=STATE_LABELS[STATE_CHECKED_OUT], status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_check_out_detail_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_out_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_list_view_no_permission(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_check_out_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_out_list_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_check_out_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_check_out_list_view_with_access(self):
        self._check_out_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_out_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_in_forcefull_view_no_permission(self):
        # Gitlab issue #237
        # Forcefully checking in a document by a user without adequate
        # permissions throws out an error.
        self._create_test_user()
        # Check out document as test_user.
        self._check_out_test_document(user=self.test_user)

        self.grant_access(
            obj=self.test_document, permission=permission_document_check_in
        )

        self._clear_events()

        response = self._request_test_document_check_in_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_check_in_forcefull_view_with_access(self):
        self._create_test_user()
        # Check out document as test_user.
        self._check_out_test_document(user=self.test_user)

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_in_override
        )

        self._clear_events()

        # Check in document as test_case_user.
        response = self._request_test_document_check_in_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(
            events[0].verb, event_document_forcefully_checked_in.id
        )

    def test_trashed_document_check_in_forcefull_view_with_access(self):
        self._create_test_user()
        # Check out document as test_user
        self._check_out_test_document(user=self.test_user)

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_in_override
        )

        self.test_document.delete()

        self._clear_events()

        # Check in document as test_case_user
        response = self._request_test_document_check_in_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_document.is_checked_out())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_check_in_of_non_checked_out_document_view(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_in
        )

        self._clear_events()

        response = self._request_test_document_check_in_post_view(follow=True)
        self.assertContains(
            response=response, status_code=200,
            text=force_text(s=DocumentNotCheckedOut())
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_check_in_of_non_checked_out_trashed_document_view(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_in
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_in_post_view(follow=True)
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_check_out_of_checked_out_document_view(self):
        self._create_test_user()
        self._check_out_test_document(user=self.test_user)
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_out
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self._clear_events()

        response = self._request_test_document_check_out_post_view(follow=True)
        self.assertContains(
            response=response, status_code=200,
            text=force_text(s=DocumentAlreadyCheckedOut())
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_check_out_of_checked_out_trashed_document(self):
        self._create_test_user()
        self._check_out_test_document(user=self.test_user)
        self.grant_access(
            obj=self.test_document, permission=permission_document_check_out
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_check_out_detail_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_check_out_post_view(follow=True)
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentCheckoutOptionsViewTestCase(
    DocumentCheckoutTestMixin, DocumentCheckoutViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_check_out_block_new_file_view(self):
        self._silence_logger(name='mayan.apps.sources.links')

        self._create_test_user()
        self._check_out_test_document(user=self.test_user)
        file_count = DocumentFile.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_new
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_view
        )

        self._clear_events()

        response = self.post(
            viewname='sources:document_file_upload', kwargs={
                'document_id': self.test_document.pk
            }, follow=True
        )
        self.assertContains(
            response=response, status_code=200,
            text='Unable to upload new files'
        )

        self.assertEqual(DocumentFile.objects.count(), file_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_check_out_block_new_version(self):
        self._check_out_test_document()
        file_count = DocumentFile.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_new
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self.post(
            viewname='sources:document_file_upload', kwargs={
                'document_id': self.test_document.pk
            }, follow=True
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(DocumentFile.objects.count(), file_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
