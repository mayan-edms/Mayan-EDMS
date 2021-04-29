from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_type_view,
    permission_document_view
)
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_index_template_created, event_index_template_edited
from ..models import IndexInstanceNode, IndexTemplate, IndexTemplateNode
from ..permissions import (
    permission_index_template_create, permission_index_template_delete,
    permission_index_template_edit,
    permission_index_instance_view,
    permission_index_template_rebuild, permission_index_template_view
)

from .literals import TEST_INDEX_TEMPLATE_LABEL
from .mixins import (
    DocumentIndexAPIViewTestMixin, IndexInstanceAPIViewTestMixin,
    IndexInstanceNodeAPIViewTestMixin, IndexTemplateTestMixin,
    IndexTemplateActionAPIViewTestMixin, IndexTemplateAPIViewTestMixin,
    IndexTemplateDocumentTypeAPIViewTestMixin,
    IndexTemplateNodeAPITestMixin
)


class DocumentIndexAPIViewTestCase(
    DocumentIndexAPIViewTestMixin, DocumentTestMixin, IndexTemplateTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_index_template(add_test_document_type=True)
        self._create_test_index_template_node(rebuild=True)

    def test_document_index_instance_instance_list_api_view_no_permission(self):
        response = self._request_test_document_index_instance_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_index_instance_instance_list_api_view_with_index_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        response = self._request_test_document_index_instance_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_index_instance_instance_list_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_index_instance_view
        )

        response = self._request_test_document_index_instance_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_document_index_instance_instance_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        response = self._request_test_document_index_instance_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'], self.test_index_instance_node.pk
        )


class IndexInstanceAPIViewTestCase(
    IndexTemplateTestMixin, IndexInstanceAPIViewTestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_index_template()

    def test_index_instance_detail_api_view_no_permission(self):
        response = self._request_test_index_instance_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('id' not in response.data)

    def test_index_instance_detail_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_instance_view
        )

        response = self._request_test_index_instance_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_index_template.pk
        )

    def test_index_instance_list_api_view_no_permission(self):
        response = self._request_test_index_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_index_instance_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_instance_view
        )

        response = self._request_test_index_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'], self.test_index_template.pk
        )


class IndexInstanceNodeAPIViewTestCase(
    IndexTemplateTestMixin, IndexInstanceNodeAPIViewTestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_index_template(add_test_document_type=True)
        self._create_test_index_template_node(rebuild=True)

    def test_index_instance_node_list_api_view_no_permission(self):
        response = self._request_test_index_instance_node_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response.data)

    def test_index_instance_node_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_instance_view
        )

        response = self._request_test_index_instance_node_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_index_instance_node.pk
        )

    def test_index_instance_node_detail_api_view_no_permission(self):
        response = self._request_test_index_instance_node_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response.data)

    def test_index_instance_node_detail_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_instance_view
        )

        response = self._request_test_index_instance_node_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_index_instance_node.pk
        )

    def test_index_instance_node_document_list_api_view_no_permission(self):
        response = self._request_test_index_instance_node_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response.data)

    def test_index_instance_node_document_list_api_view_with_index_access(self):
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_instance_view
        )

        response = self._request_test_index_instance_node_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_index_instance_node_document_list_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_view
        )
        response = self._request_test_index_instance_node_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response.data)

    def test_index_instance_node_document_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_instance_view
        )

        response = self._request_test_index_instance_node_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'], self.test_document.pk
        )


class IndexTemplateAPIViewTestCase(
    IndexTemplateTestMixin, IndexTemplateAPIViewTestMixin, BaseAPITestCase
):
    def test_index_template_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_template_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(IndexTemplate.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_index_template_create)

        self._clear_events()

        response = self._request_test_index_template_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['id'], self.test_index_template.pk)
        self.assertEqual(response.data['label'], self.test_index_template.label)

        self.assertEqual(IndexTemplate.objects.count(), 1)
        self.assertEqual(
            self.test_index_template.label, TEST_INDEX_TEMPLATE_LABEL
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_index_template)
        self.assertEqual(events[0].verb, event_index_template_created.id)

    def test_index_template_delete_api_view_no_permission(self):
        self._create_test_index_template()

        self._clear_events()

        response = self._request_test_index_template_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_index_template in IndexTemplate.objects.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_delete_api_view_with_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_delete
        )

        self._clear_events()

        response = self._request_test_index_template_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertTrue(self.test_index_template not in IndexTemplate.objects.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_detail_api_view_no_permission(self):
        self._create_test_index_template()

        self._clear_events()

        response = self._request_test_index_template_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('id' not in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_detail_api_view_with_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_view
        )

        self._clear_events()

        response = self._request_test_index_template_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_index_template.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_edit_via_patch_api_view_no_permission(self):
        self._create_test_index_template()

        self._clear_events()

        response = self._request_test_index_template_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('id' not in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_edit_via_patch_api_view_with_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_index_template.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_index_template)
        self.assertEqual(events[0].verb, event_index_template_edited.id)

    def test_index_template_list_api_view_no_permission(self):
        self._create_test_index_template()

        self._clear_events()

        response = self._request_test_index_template_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_list_api_view_with_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_view
        )

        self._clear_events()

        response = self._request_test_index_template_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'], self.test_index_template.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexTemplateDocumentTypeAPIViewTestCase(
    IndexTemplateTestMixin, IndexTemplateDocumentTypeAPIViewTestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def test_index_template_document_type_list_api_view_no_permission(self):
        self._create_test_index_template(add_test_document_type=True)

        self._clear_events()

        response = self._request_test_index_template_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_list_api_view_with_document_type_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_list_api_view_with_index_template_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_view
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_list_api_view_with_full_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_view
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'], self.test_document_type.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_api_view_no_permission(self):
        self._create_test_index_template()

        self._clear_events()

        response = self._request_test_index_template_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            self.test_document_type not in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_api_view_with_document_type_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            self.test_document_type not in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_api_view_with_index_template_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            self.test_document_type not in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_api_view_with_full_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            self.test_document_type in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_index_template)
        self.assertEqual(events[0].verb, event_index_template_edited.id)

    def test_index_template_document_type_remove_api_view_no_permission(self):
        self._create_test_index_template(add_test_document_type=True)

        self._clear_events()

        response = self._request_test_index_template_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            self.test_document_type in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_remove_api_view_with_document_type_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            self.test_document_type in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_remove_api_view_with_index_template_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(
            self.test_document_type in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_remove_api_view_with_full_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            self.test_document_type not in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_index_template)
        self.assertEqual(events[0].verb, event_index_template_edited.id)


class IndexTemplateRebuildAPIViewTestCase(
    IndexTemplateTestMixin, IndexTemplateActionAPIViewTestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()

        self._upload_test_document()
        self._create_test_index_template(add_test_document_type=True)
        self._create_test_index_template_node()

    def test_index_template_rebuild_api_view_no_permission(self):
        test_index_instance_node_count = IndexInstanceNode.objects.count()

        self._clear_events()

        response = self._request_test_index_template_rebuild_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            IndexInstanceNode.objects.count(), test_index_instance_node_count
        )
        self.assertEqual(IndexInstanceNode.objects.first().parent, None)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_rebuild_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        test_index_instance_node_count = IndexInstanceNode.objects.count()

        self._clear_events()

        response = self._request_test_index_template_rebuild_api_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            IndexInstanceNode.objects.count(),
            test_index_instance_node_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexTemplateResetAPIViewTestCase(
    IndexTemplateTestMixin, IndexTemplateActionAPIViewTestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()

        self._create_test_index_template(add_test_document_type=True)
        self._create_test_index_template_node()

        self._create_test_document_stub()
        self.test_index_template.rebuild()

    def test_index_template_reset_api_view_no_permission(self):
        test_index_instance_node_count = self.test_index_template.instance_root.get_children_count()

        self._clear_events()

        response = self._request_test_index_template_reset_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_index_template.instance_root.get_children_count(),
            test_index_instance_node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_reset_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        test_index_instance_node_count = self.test_index_template.instance_root.get_children_count()

        self._clear_events()

        response = self._request_test_index_template_reset_api_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            self.test_index_template.instance_root.get_children_count(),
            test_index_instance_node_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexTemplateNodeAPIViewTestCase(
    IndexTemplateTestMixin, IndexTemplateNodeAPITestMixin, DocumentTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_index_template()

    def test_index_template_node_no_parent_create_api_view_no_permission(self):
        index_template_node_count = IndexTemplateNode.objects.count()

        response = self._request_test_index_template_node_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

    def test_index_template_node_no_parent_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_edit
        )
        index_template_node_count = IndexTemplateNode.objects.count()

        response = self._request_test_index_template_node_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

    def test_index_template_node_bad_parent_create_api_view_no_permission(self):
        self._create_test_index_template()

        index_template_node_count = IndexTemplateNode.objects.count()
        response = self._request_test_index_template_node_create_api_view(
            extra_data={
                'parent': self.test_index_templates[0].template_root.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

    def test_index_template_node_bad_parent_create_api_view_with_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_edit
        )
        index_template_node_count = IndexTemplateNode.objects.count()

        response = self._request_test_index_template_node_create_api_view(
            extra_data={
                'parent': self.test_index_templates[0].template_root.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

    def test_index_template_node_create_api_view_no_permission(self):
        index_template_node_count = IndexTemplateNode.objects.count()
        response = self._request_test_index_template_node_create_api_view(
            extra_data={
                'parent': self.test_index_template.template_root.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

    def test_index_template_node_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_edit
        )
        index_template_node_count = IndexTemplateNode.objects.count()

        response = self._request_test_index_template_node_create_api_view(
            extra_data={
                'parent': self.test_index_template.template_root.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['id'], self.test_index_template_node.pk
        )

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count + 1
        )

    def test_index_template_node_delete_api_view_no_permission(self):
        self._create_test_index_template_node()

        index_template_node_count = IndexTemplateNode.objects.count()
        response = self._request_test_index_template_node_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

    def test_index_template_node_delete_api_view_with_access(self):
        self._create_test_index_template_node()

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_edit
        )
        index_template_node_count = IndexTemplateNode.objects.count()

        response = self._request_test_index_template_node_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count - 1
        )

    def test_index_template_node_detail_api_view_no_permission(self):
        self._create_test_index_template_node()

        response = self._request_test_index_template_node_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response.data)

    def test_index_template_node_detail_api_view_with_access(self):
        self._create_test_index_template_node()

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_view
        )

        response = self._request_test_index_template_node_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_index_template_node.pk
        )

    def test_index_template_node_edit_via_patch_api_view_no_permission(self):
        self._create_test_index_template_node()

        index_template_node_expression = self.test_index_template_node.expression

        response = self._request_test_index_template_node_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_index_template_node.refresh_from_db()
        self.assertEqual(
            index_template_node_expression,
            self.test_index_template_node.expression
        )

    def test_index_template_node_edit_via_patch_api_view_with_access(self):
        self._create_test_index_template_node()

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_edit
        )
        index_template_node_expression = self.test_index_template_node.expression

        response = self._request_test_index_template_node_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_index_template_node.refresh_from_db()
        self.assertNotEqual(
            index_template_node_expression,
            self.test_index_template_node.expression
        )

    def test_index_template_node_list_api_view_no_permission(self):
        self._create_test_index_template_node()

        response = self._request_test_index_template_node_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response)

    def test_index_template_node_list_api_view_with_access(self):
        self._create_test_index_template_node()

        self.grant_access(
            obj=self.test_index_template, permission=permission_index_template_view
        )

        response = self._request_test_index_template_node_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_index_template_node.pk
        )
