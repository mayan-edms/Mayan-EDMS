from rest_framework import status

from mayan.apps.documents.tests.base import GenericDocumentAPIViewTestCase
from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_type_view
)

from ..events import event_index_template_created, event_index_template_edited
from ..models import IndexInstanceNode, IndexTemplate, IndexTemplateNode
from ..permissions import (
    permission_index_template_create, permission_index_template_delete,
    permission_index_template_edit, permission_index_template_rebuild,
    permission_index_template_view
)

from .literals import TEST_INDEX_TEMPLATE_LABEL
from .mixins import (
    IndexInstanceTestMixin, IndexTemplateTestMixin,
    IndexTemplateActionAPIViewTestMixin, IndexTemplateAPIViewTestMixin,
    IndexTemplateDocumentTypeAPIViewTestMixin, IndexTemplateNodeAPITestMixin
)


class IndexTemplateAPIViewTestCase(
    IndexTemplateTestMixin, IndexTemplateAPIViewTestMixin,
    GenericDocumentAPIViewTestCase
):
    auto_create_test_index_template = False
    auto_upload_test_document = False

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
        self.assertEqual(
            response.data['label'], self.test_index_template.label
        )

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

        self.assertTrue(
            self.test_index_template in IndexTemplate.objects.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_delete_api_view_with_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_delete
        )

        self._clear_events()

        response = self._request_test_index_template_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertTrue(
            self.test_index_template not in IndexTemplate.objects.all()
        )

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
            obj=self.test_index_template,
            permission=permission_index_template_view
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
            obj=self.test_index_template,
            permission=permission_index_template_edit
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
            obj=self.test_index_template,
            permission=permission_index_template_view
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
    IndexTemplateTestMixin, IndexTemplateDocumentTypeAPIViewTestMixin,
    GenericDocumentAPIViewTestCase
):
    auto_upload_test_document = False

    def test_index_template_document_type_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_template_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_list_api_view_with_document_type_access(self):
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
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_view
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_view
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
        self.test_document_type.index_templates.remove(
            self.test_index_template
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            self.test_document_type not in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_api_view_with_document_type_access(self):
        self.test_document_type.index_templates.remove(
            self.test_index_template
        )

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
        self.test_document_type.index_templates.remove(
            self.test_index_template
        )

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
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
        self.test_document_type.index_templates.remove(
            self.test_index_template
        )

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
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
        self._clear_events()

        response = self._request_test_index_template_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(
            self.test_document_type in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_remove_api_view_with_document_type_access(self):
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
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
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
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
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
    IndexInstanceTestMixin, IndexTemplateTestMixin,
    IndexTemplateActionAPIViewTestMixin, GenericDocumentAPIViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        IndexInstanceNode.objects.exclude(parent=None).delete()

    def test_index_template_rebuild_api_view_no_permission(self):
        test_index_instance_node_count = self.test_index_instance.get_descendants().count()

        self._clear_events()

        response = self._request_test_index_template_rebuild_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_index_instance.get_descendants().count(),
            test_index_instance_node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_rebuild_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        test_index_instance_node_count = self.test_index_instance.get_descendants().count()

        self._clear_events()

        response = self._request_test_index_template_rebuild_api_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            self.test_index_instance.get_descendants().count(),
            test_index_instance_node_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexTemplateResetAPIViewTestCase(
    IndexInstanceTestMixin, IndexTemplateTestMixin,
    IndexTemplateActionAPIViewTestMixin, GenericDocumentAPIViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()

        self.test_index_template.rebuild()

    def test_index_template_reset_api_view_no_permission(self):
        test_index_instance_node_count = self.test_index_instance.get_descendants().count()

        self._clear_events()

        response = self._request_test_index_template_reset_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_index_instance.get_descendants().count(),
            test_index_instance_node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_reset_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        test_index_instance_node_count = self.test_index_instance.get_descendants().count()

        self._clear_events()

        response = self._request_test_index_template_reset_api_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            self.test_index_instance.get_descendants().count(),
            test_index_instance_node_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexTemplateNodeAPIViewTestCase(
    IndexTemplateTestMixin, IndexTemplateNodeAPITestMixin,
    GenericDocumentAPIViewTestCase
):
    auto_upload_test_document = False

    def test_index_template_node_no_parent_create_api_view_no_permission(self):
        IndexTemplateNode.objects.all().delete()

        index_template_node_count = IndexTemplateNode.objects.count()

        self._clear_events()

        response = self._request_test_index_template_node_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_no_parent_create_api_view_with_access(self):
        IndexTemplateNode.objects.all().delete()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )
        index_template_node_count = IndexTemplateNode.objects.count()

        self._clear_events()

        response = self._request_test_index_template_node_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_bad_parent_create_api_view_no_permission(self):
        self._create_test_index_template()

        index_template_node_count = IndexTemplateNode.objects.count()

        self._clear_events()

        response = self._request_test_index_template_node_create_api_view(
            extra_data={
                'parent': self.test_index_templates[0].index_template_root_node.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_bad_parent_create_api_view_with_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )
        index_template_node_count = IndexTemplateNode.objects.count()

        self._clear_events()

        response = self._request_test_index_template_node_create_api_view(
            extra_data={
                'parent': self.test_index_templates[0].index_template_root_node.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_create_api_view_no_permission(self):
        index_template_node_count = IndexTemplateNode.objects.count()

        self._clear_events()

        response = self._request_test_index_template_node_create_api_view(
            extra_data={
                'parent': self.test_index_template.index_template_root_node.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )
        index_template_node_count = IndexTemplateNode.objects.count()

        self._clear_events()

        response = self._request_test_index_template_node_create_api_view(
            extra_data={
                'parent': self.test_index_template.index_template_root_node.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['id'], self.test_index_template_node.pk
        )

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_delete_api_view_no_permission(self):
        index_template_node_count = IndexTemplateNode.objects.count()

        self._clear_events()

        response = self._request_test_index_template_node_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_delete_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )
        index_template_node_count = IndexTemplateNode.objects.count()

        self._clear_events()

        response = self._request_test_index_template_node_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            IndexTemplateNode.objects.count(), index_template_node_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_detail_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_template_node_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_detail_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_view
        )

        self._clear_events()

        response = self._request_test_index_template_node_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_index_template_node.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_edit_via_patch_api_view_no_permission(self):
        index_template_node_expression = self.test_index_template_node.expression

        self._clear_events()

        response = self._request_test_index_template_node_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_index_template_node.refresh_from_db()
        self.assertEqual(
            index_template_node_expression,
            self.test_index_template_node.expression
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_edit_via_patch_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )
        index_template_node_expression = self.test_index_template_node.expression

        self._clear_events()

        response = self._request_test_index_template_node_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_index_template_node.refresh_from_db()
        self.assertNotEqual(
            index_template_node_expression,
            self.test_index_template_node.expression
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_template_node_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_view
        )

        self._clear_events()

        response = self._request_test_index_template_node_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_index_template_node.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
