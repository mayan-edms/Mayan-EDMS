from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import (
    event_cabinet_created, event_cabinet_edited,
    event_cabinet_document_added, event_cabinet_document_removed
)
from ..models import Cabinet
from ..permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_remove_document, permission_cabinet_view
)
from .literals import TEST_CABINET_LABEL, TEST_CABINET_LABEL_EDITED
from .mixins import (
    CabinetTestMixin, CabinetViewTestMixin,
    DocumentCabinetViewTestMixin
)


class CabinetViewTestCase(
    CabinetTestMixin, CabinetViewTestMixin, GenericViewTestCase
):
    def test_cabinet_create_view_no_permission(self):
        self._clear_events()

        response = self._request_test_cabinet_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Cabinet.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_create_view_with_permission(self):
        self.grant_permission(permission=permission_cabinet_create)

        self._clear_events()

        response = self._request_test_cabinet_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Cabinet.objects.count(), 1)
        self.assertEqual(Cabinet.objects.first().label, TEST_CABINET_LABEL)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_cabinet)
        self.assertEqual(events[0].verb, event_cabinet_created.id)

    def test_cabinet_create_duplicate_view_with_permission(self):
        self._create_test_cabinet()
        self.grant_permission(permission=permission_cabinet_create)

        cabinet_count = Cabinet.objects.count()
        cabinet_original = self.test_cabinet

        self._clear_events()

        response = self._request_test_cabinet_create_view()
        # HTTP 200 with error message
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Cabinet.objects.count(), cabinet_count)
        self.assertEqual(Cabinet.objects.first(), cabinet_original)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_delete_view_no_permission(self):
        self._create_test_cabinet()

        self._clear_events()

        response = self._request_test_cabinet_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Cabinet.objects.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_delete_view_with_access(self):
        self._create_test_cabinet()
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_delete
        )

        self._clear_events()

        response = self._request_test_cabinet_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Cabinet.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_edit_view_no_permission(self):
        self._create_test_cabinet()

        self._clear_events()

        response = self._request_test_cabinet_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(self.test_cabinet.label, TEST_CABINET_LABEL)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_edit_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )

        self._clear_events()

        response = self._request_test_cabinet_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(self.test_cabinet.label, TEST_CABINET_LABEL_EDITED)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_cabinet)
        self.assertEqual(events[0].verb, event_cabinet_edited.id)

    def test_cabinet_list_view_no_permission(self):
        self._create_test_cabinet()

        self._clear_events()

        response = self._request_test_cabinet_list_view()
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_list_view_with_access(self):
        self._create_test_cabinet()
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        self._clear_events()

        response = self._request_test_cabinet_list_view()
        self.assertContains(
            response, text=self.test_cabinet.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class CabinetChildViewTestCase(
    CabinetTestMixin, CabinetViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_cabinet()

    def test_cabinet_child_create_view_no_permission(self):
        cabinet_count = Cabinet.objects.count()

        self._clear_events()

        response = self._request_test_cabinet_child_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Cabinet.objects.count(), cabinet_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_child_create_view_with_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )
        cabinet_count = Cabinet.objects.count()

        self._clear_events()

        response = self._request_test_cabinet_child_create_view()
        self.assertEqual(response.status_code, 302)

        self.test_cabinets[0].refresh_from_db()
        self.assertEqual(Cabinet.objects.count(), cabinet_count + 1)
        self.assertTrue(
            self.test_cabinets[1] in self.test_cabinets[0].get_descendants()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_cabinet)
        self.assertEqual(events[0].verb, event_cabinet_created.id)

    def test_cabinet_child_delete_view_no_permission(self):
        self._create_test_cabinet_child()

        cabinet_count = Cabinet.objects.count()

        self._clear_events()

        response = self._request_test_cabinet_child_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Cabinet.objects.count(), cabinet_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_child_delete_view_with_access(self):
        self._create_test_cabinet_child()
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_delete
        )

        cabinet_count = Cabinet.objects.count()

        self._clear_events()

        response = self._request_test_cabinet_child_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Cabinet.objects.count(), cabinet_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class CabinetDocumentViewTestCase(
    CabinetTestMixin, CabinetViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_cabinet()

    def test_cabinet_add_document_view_no_permission(self):
        self.grant_permission(permission=permission_cabinet_view)

        cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_document_cabinet_add_view()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(
            self.test_cabinet.documents.count(), cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_add_document_view_with_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_add_document
        )
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_add_document
        )

        cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_document_cabinet_add_view()
        self.assertEqual(response.status_code, 302)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(
            self.test_cabinet.documents.count(), cabinet_document_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_cabinet)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_cabinet_document_added.id)

    def test_cabinet_add_trashed_document_view_with_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_add_document
        )
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_add_document
        )

        self.test_document.delete()

        cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_document_cabinet_add_view()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(
            self.test_cabinet.documents.count(), cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_add_multiple_documents_view_no_permission(self):
        self.grant_permission(permission=permission_cabinet_view)

        cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_document_multiple_cabinet_multiple_add_view_cabinet()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(
            self.test_cabinet.documents.count(), cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_add_multiple_documents_view_with_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_add_document
        )
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_add_document
        )

        cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_document_multiple_cabinet_multiple_add_view_cabinet()
        self.assertEqual(response.status_code, 302)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(
            self.test_cabinet.documents.count(), cabinet_document_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_cabinet)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_cabinet_document_added.id)

    def test_cabinet_add_multiple_trashed_documents_view_with_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_add_document
        )
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_add_document
        )

        self.test_document.delete()

        cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_document_multiple_cabinet_multiple_add_view_cabinet()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(
            self.test_cabinet.documents.count(), cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_remove_document_view_no_permission(self):
        self.test_cabinet.documents.add(self.test_document)

        cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_document_cabinet_multiple_remove_view()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(
            self.test_cabinet.documents.count(), cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_remove_document_view_with_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet,
            permission=permission_cabinet_remove_document
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_cabinet_remove_document
        )

        cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_document_cabinet_multiple_remove_view()
        self.assertEqual(response.status_code, 302)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(
            self.test_cabinet.documents.count(), cabinet_document_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_cabinet)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_cabinet_document_removed.id)

    def test_cabinet_remove_trashed_document_view_with_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet,
            permission=permission_cabinet_remove_document
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_cabinet_remove_document
        )

        self.test_document.delete()

        cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_document_cabinet_multiple_remove_view()
        self.assertEqual(response.status_code, 404)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(
            self.test_cabinet.documents.count(), cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_list_view_no_permission(self):
        self.test_cabinet.documents.add(self.test_document)

        self._clear_events()

        response = self._request_test_cabinet_document_list_view()
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=404
        )
        self.assertNotContains(
            response, text=self.test_document.label, status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_list_view_with_cabinet_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        self._clear_events()

        response = self._request_test_cabinet_document_list_view()
        self.assertContains(
            response, text=self.test_cabinet.label, status_code=200
        )
        self.assertNotContains(
            response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_list_view_with_document_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_cabinet_document_list_view()
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=404
        )
        self.assertNotContains(
            response, text=self.test_document.label, status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_list_view_with_full_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_cabinet_document_list_view()
        self.assertContains(
            response, text=self.test_cabinet.label, status_code=200
        )
        self.assertContains(
            response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_trashed_document_list_view_with_full_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_cabinet_document_list_view()
        self.assertContains(
            response, text=self.test_cabinet.label, status_code=200
        )
        self.assertNotContains(
            response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentCabinetViewTestCase(
    CabinetTestMixin, DocumentCabinetViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_cabinet()

    def test_document_cabinet_list_view_no_permission(self):
        self.test_document.cabinets.add(self.test_cabinet)

        self._clear_events()

        response = self._request_test_document_cabinet_list_view()
        self.assertNotContains(
            response, text=self.test_document.label, status_code=404
        )
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_cabinet_list_view_with_document_access(self):
        self.test_document.cabinets.add(self.test_cabinet)

        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_view
        )

        self._clear_events()

        response = self._request_test_document_cabinet_list_view()
        self.assertContains(
            response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_cabinet_list_view_with_cabinet_access(self):
        self.test_document.cabinets.add(self.test_cabinet)

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        self._clear_events()

        response = self._request_test_document_cabinet_list_view()
        self.assertNotContains(
            response, text=self.test_document.label, status_code=404
        )
        self.assertNotContains(
            response, text=self.test_cabinet.label, status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_cabinet_list_view_with_full_access(self):
        self.test_document.cabinets.add(self.test_cabinet)

        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_view
        )
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        self._clear_events()

        response = self._request_test_document_cabinet_list_view()
        self.assertContains(
            response, text=self.test_document.label, status_code=200
        )
        self.assertContains(
            response, text=self.test_cabinet.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_cabinet_list_view_with_full_access(self):
        self.test_document.cabinets.add(self.test_cabinet)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_cabinet_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
