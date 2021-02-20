from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_cabinet_created, event_cabinet_edited, event_cabinet_document_added,
    event_cabinet_document_removed
)
from ..models import Cabinet
from ..permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_remove_document, permission_cabinet_view
)

from .mixins import (
    CabinetAPIViewTestMixin, CabinetDocumentAPIViewTestMixin,
    CabinetTestMixin, DocumentCabinetAPIViewTestMixin
)


class CabinetAPITestCase(
    CabinetAPIViewTestMixin, CabinetTestMixin, BaseAPITestCase
):
    def test_cabinet_create_api_view_no_permission(self):
        test_cabinet_count = Cabinet.objects.count()

        self._clear_events()

        response = self._request_test_cabinet_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Cabinet.objects.count(), test_cabinet_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_create_api_view_with_permission(self):
        test_cabinet_count = Cabinet.objects.count()

        self.grant_permission(permission=permission_cabinet_create)

        self._clear_events()

        response = self._request_test_cabinet_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], self.test_cabinet.pk)
        self.assertEqual(response.data['label'], self.test_cabinet.label)

        self.assertEqual(Cabinet.objects.count(), test_cabinet_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_cabinet)
        self.assertEqual(events[0].verb, event_cabinet_created.id)

    def test_cabinet_delete_api_view_no_permissions(self):
        self._create_test_cabinet()

        test_cabinet_count = Cabinet.objects.count()

        self._clear_events()

        response = self._request_test_cabinet_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Cabinet.objects.count(), test_cabinet_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_delete_api_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_delete
        )

        test_cabinet_count = Cabinet.objects.count()

        self._clear_events()

        response = self._request_test_cabinet_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Cabinet.objects.count(), test_cabinet_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_edit_api_patch_view_no_pemission(self):
        self._create_test_cabinet()

        cabinet_label = self.test_cabinet.label

        self._clear_events()

        response = self._request_test_cabinet_edit_api_patch_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(cabinet_label, self.test_cabinet.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_edit_api_patch_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )

        cabinet_label = self.test_cabinet.label

        self._clear_events()

        response = self._request_test_cabinet_edit_api_patch_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_cabinet.refresh_from_db()
        self.assertNotEqual(cabinet_label, self.test_cabinet.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_cabinet)
        self.assertEqual(events[0].verb, event_cabinet_edited.id)

    def test_cabinet_edit_api_put_view_no_pemission(self):
        self._create_test_cabinet()

        cabinet_label = self.test_cabinet.label

        self._clear_events()

        response = self._request_test_cabinet_edit_api_put_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_cabinet.refresh_from_db()
        self.assertEqual(cabinet_label, self.test_cabinet.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_edit_api_put_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )

        cabinet_label = self.test_cabinet.label

        self._clear_events()

        response = self._request_test_cabinet_edit_api_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_cabinet.refresh_from_db()
        self.assertNotEqual(cabinet_label, self.test_cabinet.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_cabinet)
        self.assertEqual(events[0].verb, event_cabinet_edited.id)

    def test_cabinet_list_api_view_no_permission(self):
        self._create_test_cabinet()

        self._clear_events()

        response = self._request_test_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_list_api_view_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        self._clear_events()

        response = self._request_test_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], self.test_cabinet.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class CabinetDocumentAPITestCase(
    CabinetDocumentAPIViewTestMixin, CabinetTestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_cabinet()

    def test_cabinet_document_add_api_view_no_permission(self):
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_add_document
        )

        test_cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_cabinet_document_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_cabinet.documents.count(), test_cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_add_api_view_with_cabinet_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_add_document
        )

        test_cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_cabinet_document_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            self.test_cabinet.documents.count(), test_cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_add_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_add_document
        )

        test_cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_cabinet_document_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_cabinet.documents.count(), test_cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_add_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_add_document
        )
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_add_document
        )

        test_cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_cabinet_document_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            self.test_cabinet.documents.count(),
            test_cabinet_document_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_cabinet)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_cabinet_document_added.id)

    def test_cabinet_trashed_document_add_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_add_document
        )
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_add_document
        )

        test_cabinet_document_count = self.test_cabinet.documents.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_cabinet_document_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            self.test_cabinet.documents.count(),
            test_cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_list_api_view_no_permission(self):
        self.test_cabinet.documents.add(self.test_document)

        self._clear_events()

        response = self._request_test_cabinet_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_list_api_view_with_cabinet_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )

        self._clear_events()

        response = self._request_test_cabinet_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_list_api_view_with_document_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_view
        )

        self._clear_events()

        response = self._request_test_cabinet_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_list_api_view_with_full_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_cabinet_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['uuid'],
            force_text(s=self.test_document.uuid)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_trashed_document_list_api_view_with_full_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_cabinet_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_remove_api_view_no_permission(self):
        self.test_cabinet.documents.add(self.test_document)

        test_cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_cabinet_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_cabinet.documents.count(), test_cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_remove_api_view_with_cabinet_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet,
            permission=permission_cabinet_remove_document
        )

        test_cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_cabinet_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            self.test_cabinet.documents.count(), test_cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_remove_api_view_with_document_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document,
            permission=permission_cabinet_remove_document
        )

        test_cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_cabinet_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_cabinet.documents.count(), test_cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_document_remove_api_view_with_full_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet,
            permission=permission_cabinet_remove_document
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_cabinet_remove_document
        )

        test_cabinet_document_count = self.test_cabinet.documents.count()

        self._clear_events()

        response = self._request_test_cabinet_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            self.test_cabinet.documents.count(),
            test_cabinet_document_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_cabinet)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_cabinet_document_removed.id)

    def test_cabinet_trashed_document_remove_api_view_with_full_access(self):
        self.test_cabinet.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_cabinet,
            permission=permission_cabinet_remove_document
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_cabinet_remove_document
        )

        test_cabinet_document_count = self.test_cabinet.documents.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_cabinet_document_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            self.test_cabinet.documents.count(), test_cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentCabinetAPITestCase(
    CabinetAPIViewTestMixin, CabinetTestMixin,
    DocumentCabinetAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_cabinet()
        self.test_cabinet.documents.add(self.test_document)

    def test_document_cabinet_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_cabinet_list_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_view,
        )

        self._clear_events()

        response = self._request_test_document_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_cabinet_list_api_view_with_cabinet_access(self):
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view,
        )

        self._clear_events()

        response = self._request_test_document_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_cabinet_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_view,
        )
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view,
        )

        self._clear_events()

        response = self._request_test_document_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['count'], Cabinet.objects.all().count()
        )
        self.assertEqual(
            response.data['results'][0]['id'], self.test_cabinet.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_cabinet_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_cabinet_view,
        )
        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_view,
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_cabinet_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
