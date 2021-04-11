from rest_framework import status

from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_type_view
)
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_document_metadata_added, event_document_metadata_edited,
    event_document_metadata_removed, event_metadata_type_created,
    event_metadata_type_edited, event_metadata_type_relationship_updated
)
from ..models import DocumentTypeMetadataType, MetadataType
from ..permissions import (
    permission_document_metadata_add, permission_document_metadata_edit,
    permission_document_metadata_remove, permission_document_metadata_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)

from .literals import (
    TEST_METADATA_TYPE_DEFAULT_VALUE, TEST_METADATA_VALUE,
    TEST_METADATA_VALUE_EDITED
)
from .mixins import (
    DocumentMetadataAPIViewTestMixin, DocumentTypeMetadataTypeAPIViewTestMixin,
    MetadataTypeAPIViewTestMixin, MetadataTypeTestMixin
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
            obj=self.test_metadata_type, permission=permission_metadata_type_delete
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
            obj=self.test_metadata_type, permission=permission_metadata_type_view
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
            obj=self.test_metadata_type, permission=permission_metadata_type_edit
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
    MetadataTypeTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()

    def _create_test_document_type_metadata_type(self):
        self.test_document_type_metadata_type = self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type, required=False
        )

    def test_document_type_metadata_type_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_document_type_metadata_type_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.test_document_type.metadata.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
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
        self.assertEqual(events[0].verb, event_metadata_type_relationship_updated.id)

    def test_document_type_metadata_type_create_dupicate_api_view(self):
        self._create_test_document_type_metadata_type()
        self.grant_permission(permission=permission_document_type_edit)

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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(self.test_document_type.metadata.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_delete_api_view_with_access(self):
        self._create_test_document_type_metadata_type()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
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
        self.assertEqual(events[0].verb, event_metadata_type_relationship_updated.id)

    def test_document_type_metadata_type_list_api_view_no_permission(self):
        self._create_test_document_type_metadata_type()

        self._clear_events()

        response = self._request_document_type_metadata_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_list_api_view_with_access(self):
        self._create_test_document_type_metadata_type()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_patch_api_view_with_access(self):
        self._create_test_document_type_metadata_type()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
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
        self.assertEqual(events[0].verb, event_metadata_type_relationship_updated.id)

    def test_document_type_metadata_type_put_api_view_no_permission(self):
        self._create_test_document_type_metadata_type()

        self._clear_events()

        response = self._request_document_type_metadata_type_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_metadata_type_put_api_view_with_access(self):
        self._create_test_document_type_metadata_type()
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
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
        self.assertEqual(events[0].verb, event_metadata_type_relationship_updated.id)


class DocumentMetadataAPIViewTestCase(
    DocumentTestMixin, DocumentMetadataAPIViewTestMixin, MetadataTypeTestMixin,
    BaseAPITestCase
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

    def _create_document_metadata(self):
        self.test_document_metadata = self.test_document.metadata.create(
            metadata_type=self.test_metadata_type, value=TEST_METADATA_VALUE
        )

    def test_document_metadata_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_document_metadata_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_create_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_metadata_add
        )

        self._clear_events()

        response = self._request_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.test_document.metadata.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_create_api_view_with_metadata_type_access(self):
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        self._clear_events()

        response = self._request_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.count(), 0)

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

        self._clear_events()

        response = self._request_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        document_metadata = self.test_document.metadata.first()
        self.assertEqual(response.data['id'], document_metadata.pk)
        self.assertEqual(document_metadata.metadata_type, self.test_metadata_type)
        self.assertEqual(document_metadata.value, TEST_METADATA_VALUE)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_added.id)

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
        self._create_document_metadata()
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
        self._create_document_metadata()

        self._clear_events()

        response = self._request_document_metadata_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.all().count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_delete_api_view_with_document_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )

        self._clear_events()

        response = self._request_document_metadata_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.all().count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_delete_api_view_with_metadata_type_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        self._clear_events()

        response = self._request_document_metadata_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.all().count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_delete_api_view_with_full_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        self._clear_events()

        response = self._request_document_metadata_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.test_document.metadata.all().count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_removed.id)

    def test_document_metadata_list_api_view_no_permission(self):
        self._create_document_metadata()

        self._clear_events()

        response = self._request_document_metadata_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_list_api_view_with_document_access(self):
        self._create_document_metadata()

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
        self._create_document_metadata()

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
        self._create_document_metadata()
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
            response.data['results'][0]['document']['id'], self.test_document.pk
        )
        self.assertEqual(
            response.data['results'][0]['metadata_type']['id'],
            self.test_metadata_type.pk
        )
        self.assertEqual(
            response.data['results'][0]['value'], TEST_METADATA_VALUE
        )
        self.assertEqual(
            response.data['results'][0]['id'], self.test_document_metadata.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_patch_api_view_no_permission(self):
        self._create_document_metadata()

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_patch_api_view_document_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_patch_api_view_metadata_type_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_patch_api_view_with_full_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            response.data['value'], TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE_EDITED
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_edited.id)

    def test_document_metadata_patch_default_value_api_view_with_full_access(self):
        self._create_document_metadata()
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
            self.test_document_metadata.value, TEST_METADATA_TYPE_DEFAULT_VALUE
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_edited.id)

    def test_document_metadata_put_api_view_no_permission(self):
        self._create_document_metadata()

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_put_api_view_document_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_put_api_view_metadata_type_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_metadata_put_api_view_with_full_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        self._clear_events()

        response = self._request_document_metadata_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            response.data['value'], TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE_EDITED
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_edited.id)

    def test_document_metadata_put_default_value_api_view_with_full_access(self):
        self._create_document_metadata()
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
            self.test_document_metadata.value, TEST_METADATA_TYPE_DEFAULT_VALUE
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_metadata_edited.id)
