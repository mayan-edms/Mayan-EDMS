from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import (
    event_metadata_type_relationship_updated, event_metadata_type_created,
    event_metadata_type_edited
)
from ..models import MetadataType
from ..permissions import (
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)

from .mixins import MetadataTypeTestMixin, MetadataTypeViewTestMixin


class DocumentTypeMetadataTypeRelationshipViewTestCase(
    MetadataTypeViewTestMixin, MetadataTypeTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()

    def test_document_type_relationship_delete_view_no_permission(self):
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self._clear_events()

        response = self._request_test_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_delete_view_with_metadata_type_access(self):
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_delete_view_with_document_type_access(self):
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_delete_view_with_full_access(self):
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(
            events[0].verb, event_metadata_type_relationship_updated.id
        )

    def test_document_type_relationship_edit_view_no_permission(self):
        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self._clear_events()

        response = self._request_test_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_edit_view_with_metadata_type_access(self):
        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_edit_view_with_document_type_access(self):
        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_relationship_edit_view_with_full_access(self):
        test_document_type_metadata_type_relationship_count = self.test_document_type.metadata.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_document_type.metadata.count(),
            test_document_type_metadata_type_relationship_count + 1
        )

        self.assertQuerysetEqual(
            qs=self.test_document_type.metadata.values(
                'metadata_type', 'required'
            ),
            values=[
                {
                    'metadata_type': self.test_metadata_type.pk,
                    'required': True,
                }
            ], transform=dict
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(
            events[0].verb, event_metadata_type_relationship_updated.id
        )


class MetadataTypeViewTestCase(
    MetadataTypeViewTestMixin, MetadataTypeTestMixin, GenericViewTestCase
):
    def test_metadata_type_create_view_no_permission(self):
        metadata_type_count = MetadataType.objects.count()

        self._clear_events()

        response = self._request_test_metadata_type_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_create_view_with_access(self):
        self.grant_permission(permission=permission_metadata_type_create)
        metadata_type_count = MetadataType.objects.count()

        self._clear_events()

        response = self._request_test_metadata_type_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_metadata_type)
        self.assertEqual(events[0].verb, event_metadata_type_created.id)

    def test_metadata_type_delete_view_no_permission(self):
        self._create_test_metadata_type()
        metadata_type_count = MetadataType.objects.count()

        self._clear_events()

        response = self._request_test_metadata_type_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_delete_view_with_access(self):
        self._create_test_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_delete
        )
        metadata_type_count = MetadataType.objects.count()

        self._clear_events()

        response = self._request_test_metadata_type_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_edit_view_no_permission(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )

        self._clear_events()

        response = self._request_test_metadata_type_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_edit_view_with_access(self):
        self._create_test_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )

        self._clear_events()

        response = self._request_test_metadata_type_edit_view()
        self.assertEqual(response.status_code, 302)

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

    def test_metadata_type_list_view_no_permission(self):
        self._create_test_metadata_type()

        self._clear_events()

        response = self._request_metadata_type_list_view()
        self.assertNotContains(
            response=response, text=self.test_metadata_type, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_list_view_with_access(self):
        self._create_test_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        self._clear_events()

        response = self._request_metadata_type_list_view()
        self.assertContains(
            response=response, text=self.test_metadata_type, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class MetadataTypeDocumentTypeRelationshipViewTestCase(
    MetadataTypeViewTestMixin, MetadataTypeTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()

    def test_metadata_type_relationship_delete_view_no_permission(self):
        self.test_metadata_type.document_types.create(
            document_type=self.test_document_type
        )

        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 404)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_relationship_delete_view_with_document_type_access(self):
        self.test_metadata_type.document_types.create(
            document_type=self.test_document_type
        )

        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 404)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_relationship_delete_view_with_metadata_type_access(self):
        self.test_metadata_type.document_types.create(
            document_type=self.test_document_type
        )

        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 302)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_relationship_delete_view_with_full_access(self):
        self.test_metadata_type.document_types.create(
            document_type=self.test_document_type
        )

        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_delete_view()
        self.assertEqual(response.status_code, 302)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(
            events[0].verb, event_metadata_type_relationship_updated.id
        )

    def test_metadata_type_document_type_relationship_view_no_permission(self):
        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_document_type_relationship_view_with_document_type_access(self):
        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_document_type_relationship_view_with_metadata_type_access(self):
        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_metadata_type, permission=permission_metadata_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_document_type_relationship_view_with_full_access(self):
        test_metadata_type_document_type_relationship_count = self.test_metadata_type.document_types.count()

        self.grant_access(
            obj=self.test_metadata_type, permission=permission_metadata_type_edit
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_metadata_type_document_type_relationship_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(
            self.test_metadata_type.document_types.count(),
            test_metadata_type_document_type_relationship_count + 1
        )

        self.assertQuerysetEqual(
            qs=self.test_document_type.metadata.values(
                'metadata_type', 'required'
            ),
            values=[
                {
                    'metadata_type': self.test_metadata_type.pk,
                    'required': True,
                }
            ], transform=dict
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_metadata_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_type)
        self.assertEqual(
            events[0].verb, event_metadata_type_relationship_updated.id
        )
