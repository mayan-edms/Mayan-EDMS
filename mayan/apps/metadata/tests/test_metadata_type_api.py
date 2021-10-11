from rest_framework import status

from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_type_view
)
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_metadata_type_created, event_metadata_type_edited,
    event_metadata_type_relationship_updated
)
from ..models import DocumentTypeMetadataType, MetadataType
from ..permissions import (
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)

from .mixins import (
    DocumentTypeMetadataTypeAPIViewTestMixin,
    DocumentTypeMetadataTypeTestMixin, MetadataTypeAPIViewTestMixin,
    MetadataTypeTestMixin
)


class MetadataTypeAPITestCase(
    MetadataTypeAPIViewTestMixin, MetadataTypeTestMixin, BaseAPITestCase
):
    def test_metadata_type_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_metadata_type_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MetadataType.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_metadata_type_create)

        self._clear_events()

        response = self._request_test_metadata_type_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        metadata_type = MetadataType.objects.first()
        self.assertEqual(response.data['id'], metadata_type.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_metadata_type)
        self.assertEqual(events[0].verb, event_metadata_type_created.id)

    def test_metadata_type_delete_api_view_no_permission(self):
        self._create_test_metadata_type()

        self._clear_events()

        response = self._request_test_metadata_type_delete_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(MetadataType.objects.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_delete_api_view_with_access(self):
        self._create_test_metadata_type()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_delete
        )

        self._clear_events()

        response = self._request_test_metadata_type_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(MetadataType.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_detail_api_view_no_permission(self):
        self._create_test_metadata_type()

        self._clear_events()

        response = self._request_test_metadata_type_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_detail_api_view_with_access(self):
        self._create_test_metadata_type()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        self._clear_events()

        response = self._request_test_metadata_type_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['label'], self.test_metadata_type.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_patch_api_view_no_permission(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )

        self._clear_events()

        response = self._request_test_metadata_type_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_patch_api_view_with_access(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_metadata_type.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_metadata_type)
        self.assertEqual(events[0].verb, event_metadata_type_edited.id)

    def test_metadata_type_put_api_view_no_permission(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )

        self._clear_events()

        response = self._request_test_metadata_type_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_put_api_view_with_access(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_metadata_type.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_metadata_type)
        self.assertEqual(events[0].verb, event_metadata_type_edited.id)

    def test_metadata_type_list_api_view_no_permission(self):
        self._create_test_metadata_type()

        self._clear_events()

        response = self._request_test_metadata_type_list_api_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_list_api_view_with_access(self):
        self._create_test_metadata_type()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        self._clear_events()

        response = self._request_test_metadata_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_metadata_type.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentTypeMetadataTypeAPITestCase(
    DocumentTestMixin, DocumentTypeMetadataTypeAPIViewTestMixin,
    DocumentTypeMetadataTypeTestMixin, MetadataTypeTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()

    def test_document_type_metadata_type_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_document_type_metadata_type_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document_type.metadata.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_create_api_view_with_document_type_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(self.test_document_type.metadata.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_create_api_view_with_metadata_type_access(self):
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document_type.metadata.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_create_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertEqual(response.data['id'], document_type_metadata_type.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(
            events[0].verb, event_metadata_type_relationship_updated.id
        )

    def test_document_type_metadata_type_create_duplicate_api_view(self):
        self._create_test_document_type_metadata_type()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys())[0], 'non_field_errors')

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_delete_api_view_no_permission(self):
        self._create_test_document_type_metadata_type()

        self._clear_events()

        response = self._request_document_type_metadata_type_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document_type.metadata.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_delete_api_view_with_document_type_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document_type.metadata.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_delete_api_view_with_metadata_type_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.test_document_type.metadata.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_delete_api_view_with_full_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.test_document_type.metadata.all().count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(
            events[0].verb, event_metadata_type_relationship_updated.id
        )

    def test_document_type_metadata_type_list_api_view_no_permission(self):
        self._create_test_document_type_metadata_type()

        self._clear_events()

        response = self._request_document_type_metadata_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_list_api_view_document_type_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_list_api_view_metadata_type_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_list_api_view_with_full_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document_type_metadata_type.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_patch_api_view_no_permission(self):
        self._create_test_document_type_metadata_type()

        self._clear_events()

        response = self._request_document_type_metadata_type_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_patch_api_view_with_document_type_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_patch_api_view_with_metadata_type_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_patch_api_view_with_full_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertEqual(document_type_metadata_type.required, True)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(
            events[0].verb, event_metadata_type_relationship_updated.id
        )

    def test_document_type_metadata_type_put_api_view_no_permission(self):
        self._create_test_document_type_metadata_type()

        self._clear_events()

        response = self._request_document_type_metadata_type_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_put_api_view_with_document_type_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_put_api_view_with_metadata_type_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_put_api_view_with_full_access(self):
        self._create_test_document_type_metadata_type()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_document_type_metadata_type_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertEqual(document_type_metadata_type.required, True)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(
            events[0].verb, event_metadata_type_relationship_updated.id
        )
