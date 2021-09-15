from django.test import override_settings

from ..events import event_document_type_changed, event_document_viewed
from ..permissions import (
    permission_document_properties_edit, permission_document_view
)

from .base import GenericDocumentViewTestCase
from .mixins.document_mixins import DocumentViewTestMixin


class DocumentViewTestCase(
    DocumentViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_properties_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_properties_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_properties_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_properties_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_properties_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_properties_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_properties_edit_get_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_properties_edit_get_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_properties_edit_get_view_with_access(self):
        self.grant_access(
            permission=permission_document_properties_edit,
            obj=self.test_document_type
        )

        self._clear_events()

        response = self._request_test_document_properties_edit_get_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_properties_edit_get_view_with_access(self):
        self.grant_access(
            permission=permission_document_properties_edit,
            obj=self.test_document_type
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_properties_edit_get_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(DOCUMENTS_LANGUAGE='fra')
    def test_document_properties_view_setting_non_us_language_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_properties_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document.label
        )
        self.assertContains(
            response=response, status_code=200,
            text='Language:</label>\n                \n                \n                    English'
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(DOCUMENTS_LANGUAGE='fra')
    def test_document_properties_edit_get_view_setting_non_us_language_with_access(self):
        self.grant_access(
            permission=permission_document_properties_edit,
            obj=self.test_document_type
        )

        self._clear_events()

        response = self._request_test_document_properties_edit_get_view()
        self.assertContains(
            response=response, status_code=200,
            text='<option value="eng" selected>English</option>',
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_list_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['object_list'].count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_list_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_list_view()
        self.assertNotContains(
            response=response, status_code=200, text=self.test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_change_post_view_no_permission(self):
        self._create_test_document_type()

        document_type = self.test_document.document_type

        self._clear_events()

        response = self._request_test_document_type_change_post_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type, document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_change_post_view_with_access(self):
        self._create_test_document_type()

        document_type = self.test_document.document_type

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        self._clear_events()

        response = self._request_test_document_type_change_post_view()
        self.assertEqual(response.status_code, 302)

        self.test_document.refresh_from_db()
        self.assertNotEqual(
            self.test_document.document_type, document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_types[1])
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_type_changed.id)

    def test_trashed_document_document_type_change_post_view_with_access(self):
        self._create_test_document_type()

        document_type = self.test_document.document_type

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_type_change_post_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type, document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_change_view_get_no_permission(self):
        self._create_test_document_type()

        document_type = self.test_document.document_type

        self._clear_events()

        response = self._request_test_document_type_change_get_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type, document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_change_view_get_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        self._clear_events()

        response = self._request_test_document_type_change_get_view()
        self.assertEqual(response.status_code, 200)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type, self.test_document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_type_change_view_get_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        self._create_test_document_type()

        document_type = self.test_document.document_type

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_type_change_get_view()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type, document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_document_type_change_view_no_permission(self):
        self._create_test_document_type()

        document_type = self.test_document.document_type

        self._clear_events()

        response = self._request_test_document_multiple_type_change()
        self.assertEqual(response.status_code, 404)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type, document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_document_type_change_view_with_permission(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        self._create_test_document_type()

        document_type = self.test_document.document_type

        self._clear_events()

        response = self._request_test_document_multiple_type_change()
        self.assertEqual(response.status_code, 302)

        self.test_document.refresh_from_db()
        self.assertNotEqual(
            self.test_document.document_type, document_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_types[1])
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_type_changed.id)

    def test_document_preview_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_preview_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_preview_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_preview_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_viewed.id)

    def test_trashed_document_preview_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_preview_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
