from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_document_metadata_added, event_document_metadata_edited,
    event_document_metadata_removed
)
from ..permissions import (
    permission_document_metadata_add, permission_document_metadata_edit,
    permission_document_metadata_remove, permission_document_metadata_view
)

from .literals import TEST_METADATA_TYPE_DEFAULT_VALUE
from .mixins import (
    DocumentMetadataAPIViewTestMixin, DocumentMetadataMixin,
    MetadataTypeTestMixin
)


class DocumentMetadataAPIViewTestCase(
    DocumentMetadataAPIViewTestMixin, DocumentMetadataMixin,
    DocumentTestMixin, MetadataTypeTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_metadata_type()
        self.test_metadata_type.default = TEST_METADATA_TYPE_DEFAULT_VALUE
        self.test_metadata_type.save()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type, required=False
        )

    def test_document_metadata_create_api_view_no_permission(self):
        document_metadata_count = self.test_document.metadata.count()

        self._clear_events()

        response = self._request_document_metadata_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_create_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )

        document_metadata_count = self.test_document.metadata.count()

        self._clear_events()

        response = self._request_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_create_api_view_with_metadata_type_access(self):
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        document_metadata_count = self.test_document.metadata.count()

        self._clear_events()

        response = self._request_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_create_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        document_metadata_count = self.test_document.metadata.count()

        self._clear_events()

        response = self._request_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_added.id)

    def test_trashed_document_metadata_create_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        document_metadata_count = self.test_document.metadata.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_create_default_value_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        self._clear_events()

        response = self._request_document_metadata_create_api_view(
            extra_data={'value': ''}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        document_metadata = self.test_document.metadata.first()
        self.assertEqual(response.data['id'], document_metadata.pk)
        self.assertEqual(
            document_metadata.metadata_type, self.test_metadata_type
        )
        self.assertEqual(
            document_metadata.value, TEST_METADATA_TYPE_DEFAULT_VALUE
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_added.id)

    def test_document_metadata_create_duplicate_api_view(self):
        self._create_test_document_metadata()
        self.grant_permission(permission=permission_document_metadata_add)

        self._clear_events()

        response = self._request_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys())[0], 'non_field_errors')

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_create_invalid_lookup_value_api_view(self):
        self.test_metadata_type.lookup = 'invalid,lookup,values,on,purpose'
        self.test_metadata_type.save()
        self.grant_permission(permission=permission_document_metadata_add)

        self._clear_events()

        response = self._request_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys())[0], 'non_field_errors')

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_delete_api_view_no_permission(self):
        self._create_test_document_metadata()

        document_metadata_count = self.test_document.metadata.count()

        self._clear_events()

        response = self._request_document_metadata_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_delete_api_view_with_document_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )

        document_metadata_count = self.test_document.metadata.count()

        self._clear_events()

        response = self._request_document_metadata_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_delete_api_view_with_metadata_type_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        document_metadata_count = self.test_document.metadata.count()

        self._clear_events()

        response = self._request_document_metadata_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_delete_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        document_metadata_count = self.test_document.metadata.count()

        self._clear_events()

        response = self._request_document_metadata_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_removed.id)

    def test_trashed_document_metadata_delete_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        document_metadata_count = self.test_document.metadata.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_metadata_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.metadata.count(), document_metadata_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_list_api_view_no_permission(self):
        self._create_test_document_metadata()

        self._clear_events()

        response = self._request_document_metadata_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_list_api_view_with_document_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )

        self._clear_events()

        response = self._request_document_metadata_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_list_api_view_with_metadata_type_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        self._clear_events()

        response = self._request_document_metadata_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_list_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        self._clear_events()

        response = self._request_document_metadata_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['document']['id'],
            self.test_document.pk
        )
        self.assertEqual(
            response.data['results'][0]['metadata_type']['id'],
            self.test_metadata_type.pk
        )
        self.assertEqual(
            response.data['results'][0]['value'],
            self.test_document_metadata.value
        )
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document_metadata.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_metadata_list_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_metadata_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_patch_api_view_no_permission(self):
        self._create_test_document_metadata()

        document_metadata_value = self.test_document_metadata.value

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, document_metadata_value
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_patch_api_view_document_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )

        document_metadata_value = self.test_document_metadata.value

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, document_metadata_value
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_patch_api_view_metadata_type_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        document_metadata_value = self.test_document_metadata.value

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, document_metadata_value
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_patch_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        document_metadata_value = self.test_document_metadata.value

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_metadata.refresh_from_db()
        self.assertNotEqual(
            self.test_document_metadata.value, document_metadata_value
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_edited.id)

    def test_trashed_document_metadata_patch_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        document_metadata_value = self.test_document_metadata.value

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, document_metadata_value
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_patch_default_value_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_patch(
            extra_data={'value': ''}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            response.data['value'], TEST_METADATA_TYPE_DEFAULT_VALUE
        )
        self.assertEqual(
            self.test_document_metadata.value,
            TEST_METADATA_TYPE_DEFAULT_VALUE
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_edited.id)

    def test_document_metadata_put_api_view_no_permission(self):
        self._create_test_document_metadata()

        document_metadata_value = self.test_document_metadata.value

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, document_metadata_value
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_put_api_view_document_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )

        document_metadata_value = self.test_document_metadata.value

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, document_metadata_value
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_put_api_view_metadata_type_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        document_metadata_value = self.test_document_metadata.value

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, document_metadata_value
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_put_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        document_metadata_value = self.test_document_metadata.value

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_metadata.refresh_from_db()
        self.assertNotEqual(
            self.test_document_metadata.value, document_metadata_value
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_edited.id)

    def test_trashed_document_metadata_put_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        document_metadata_value = self.test_document_metadata.value

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, document_metadata_value
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_put_default_value_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_put(
            extra_data={'value': ''}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            response.data['value'], TEST_METADATA_TYPE_DEFAULT_VALUE
        )
        self.assertEqual(
            self.test_document_metadata.value,
            TEST_METADATA_TYPE_DEFAULT_VALUE
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_edited.id)
