from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import (
    event_index_template_created, event_index_template_edited
)
from ..models import IndexInstanceNode, IndexTemplate
from ..permissions import (
    permission_index_template_create, permission_index_template_delete,
    permission_index_template_edit, permission_index_template_rebuild
)

from .literals import TEST_INDEX_TEMPLATE_LABEL, TEST_INDEX_TEMPLATE_LABEL_EDITED
from .mixins import (
    DocumentTypeAddRemoveIndexTemplateViewTestMixin,
    IndexTemplateNodeViewTestMixin, IndexTemplateTestMixin,
    IndexToolsViewTestMixin, IndexTemplateViewTestMixin
)


class DocumentTypeAddRemoveIndexTemplateViewTestCase(
    DocumentTypeAddRemoveIndexTemplateViewTestMixin, IndexTemplateTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_index_template()

    def test_document_type_index_template_add_remove_get_view_no_permission(self):
        self.test_document_type.index_templates.add(self.test_index_template)

        self._clear_events()

        response = self._request_test_document_type_index_template_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_index_template),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_index_template_add_remove_get_view_with_document_type_access(self):
        self.test_document_type.index_templates.add(self.test_index_template)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_index_template_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=str(self.test_index_template),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_index_template_add_remove_get_view_with_index_template_access(self):
        self.test_document_type.index_templates.add(self.test_index_template)

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_index_template_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_index_template),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_index_template_add_remove_get_view_with_full_access(self):
        self.test_document_type.index_templates.add(self.test_index_template)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_index_template_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_index_template),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_index_template_add_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_type_index_template_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_index_template not in self.test_document_type.index_templates.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_index_template_add_view_with_document_type_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_index_template_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_index_template not in self.test_document_type.index_templates.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_index_template_add_view_with_index_template_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_index_template_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_index_template not in self.test_document_type.index_templates.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_index_template_add_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_index_template_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_index_template in self.test_document_type.index_templates.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_index_template)
        self.assertEqual(events[0].verb, event_index_template_edited.id)

    def test_document_type_index_template_remove_view_no_permission(self):
        self.test_document_type.index_templates.add(self.test_index_template)

        self._clear_events()

        response = self._request_test_document_type_index_template_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_index_template in self.test_document_type.index_templates.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_index_template_remove_view_with_document_type_access(self):
        self.test_document_type.index_templates.add(self.test_index_template)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_index_template_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_index_template in self.test_document_type.index_templates.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_index_template_remove_view_with_index_template_access(self):
        self.test_document_type.index_templates.add(self.test_index_template)

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_index_template_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_index_template in self.test_document_type.index_templates.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_index_template_remove_view_with_full_access(self):
        self.test_document_type.index_templates.add(self.test_index_template)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_index_template_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_index_template not in self.test_document_type.index_templates.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_index_template)
        self.assertEqual(events[0].verb, event_index_template_edited.id)


class IndexTemplateViewTestCase(
    IndexTemplateTestMixin, IndexTemplateViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_index_template_create_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_template_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(IndexTemplate.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_create_view_with_permission(self):
        self.grant_permission(
            permission=permission_index_template_create
        )

        self._clear_events()

        response = self._request_test_index_template_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(IndexTemplate.objects.count(), 1)
        self.assertEqual(self.test_index_template.label, TEST_INDEX_TEMPLATE_LABEL)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_index_template)
        self.assertEqual(events[0].verb, event_index_template_created.id)

    def test_index_template_delete_view_no_permission(self):
        self._create_test_index_template()

        self._clear_events()

        response = self._request_test_index_template_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(IndexTemplate.objects.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_delete_view_with_permission(self):
        self._create_test_index_template()

        self.grant_permission(permission=permission_index_template_delete)

        self._clear_events()

        response = self._request_test_index_template_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(IndexTemplate.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_edit_view_no_permission(self):
        self._create_test_index_template()

        self._clear_events()

        response = self._request_test_index_template_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_index_template.refresh_from_db()
        self.assertEqual(self.test_index_template.label, TEST_INDEX_TEMPLATE_LABEL)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_edit_view_with_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_index_template.refresh_from_db()
        self.assertEqual(
            self.test_index_template.label, TEST_INDEX_TEMPLATE_LABEL_EDITED
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_index_template)
        self.assertEqual(events[0].verb, event_index_template_edited.id)

    def test_index_template_rebuild_view_no_permission(self):
        self._create_test_document_stub()
        self._create_test_index_template()
        self._create_test_index_template_node()

        self._clear_events()

        response = self._request_test_index_template_rebuild_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(IndexInstanceNode.objects.count(), 1)
        self.assertEqual(IndexInstanceNode.objects.first().parent, None)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_rebuild_view_with_access(self):
        self._create_test_document_stub()
        self._create_test_index_template()
        self._create_test_index_template_node()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        self._clear_events()

        response = self._request_test_index_template_rebuild_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(IndexInstanceNode.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexTemplateAddRemoveDocumentTypeViewTestCase(
    IndexTemplateTestMixin, IndexTemplateViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_index_template_document_type_add_remove_get_view_no_permission(self):
        self._create_test_index_template(add_test_document_type=True)

        self._clear_events()

        response = self._request_test_index_template_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_index_template),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_remove_get_view_with_document_type_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_index_template),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_remove_get_view_with_index_template_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_index_template),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_remove_get_view_with_full_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_index_template),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_view_no_permission(self):
        self._create_test_index_template()

        self._clear_events()

        response = self._request_test_index_template_document_type_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_document_type not in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_view_with_document_type_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_document_type not in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_view_with_index_template_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_document_type not in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_add_view_with_full_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_document_type in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_index_template)
        self.assertEqual(events[0].verb, event_index_template_edited.id)

    def test_index_template_document_type_remove_view_no_permission(self):
        self._create_test_index_template(add_test_document_type=True)

        self._clear_events()

        response = self._request_test_index_template_document_type_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_document_type in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_remove_view_with_document_type_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_document_type in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_remove_view_with_index_template_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_document_type in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_document_type_remove_view_with_full_access(self):
        self._create_test_index_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_document_type_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_document_type not in self.test_index_template.document_types.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_index_template)
        self.assertEqual(events[0].verb, event_index_template_edited.id)


class IndexTemplateNodeViewTestCase(
    IndexTemplateTestMixin, IndexTemplateNodeViewTestMixin,
    GenericViewTestCase
):
    def test_index_template_node_create_view_no_permission(self):
        self._create_test_index_template()
        node_count = self.test_index_template.node_templates.count()

        self._clear_events()

        response = self._request_test_index_node_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            self.test_index_template.node_templates.count(), node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_create_view_with_access(self):
        self._create_test_index_template()
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )
        node_count = self.test_index_template.node_templates.count()

        self._clear_events()

        response = self._request_test_index_node_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_index_template.node_templates.count(), node_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_delete_view_no_permission(self):
        self._create_test_index_template()
        self._create_test_index_template_node()
        node_count = self.test_index_template.node_templates.count()

        self._clear_events()

        response = self._request_test_index_node_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_index_template.node_templates.count(), node_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_delete_view_with_access(self):
        self._create_test_index_template()
        self._create_test_index_template_node()
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )
        node_count = self.test_index_template.node_templates.count()

        self._clear_events()

        response = self._request_test_index_node_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_index_template.node_templates.count(), node_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_edit_view_no_permission(self):
        self._create_test_index_template()
        self._create_test_index_template_node()
        node_expression = self.test_index_template_node.expression

        self._clear_events()

        response = self._request_test_index_node_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_index_template_node.refresh_from_db()
        self.assertEqual(
            self.test_index_template_node.expression, node_expression
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_edit_view_with_access(self):
        self._create_test_index_template()
        self._create_test_index_template_node()
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )
        node_expression = self.test_index_template_node.expression

        self._clear_events()

        response = self._request_test_index_node_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_index_template_node.refresh_from_db()
        self.assertNotEqual(
            self.test_index_template_node.expression, node_expression
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_list_get_view_no_permission(self):
        self._create_test_index_template()

        self._clear_events()

        response = self._request_test_index_node_list_get_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_node_list_get_view_with_access(self):
        self._create_test_index_template()
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_node_list_get_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexToolsViewTestCase(
    IndexTemplateTestMixin, IndexTemplateViewTestMixin, IndexToolsViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_index_all_rebuild_no_permission(self):
        self._create_test_index_template()

        response = self._request_index_all_rebuild_get_view()
        self.assertNotContains(
            response=response, text=self.test_index_template.label,
            status_code=200
        )

        response = self._request_indexes_rebuild_post_view()
        # No error since we just don't see the index.
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_index_template.instance_root.get_children_count(), 0
        )

    def test_index_all_rebuild_with_access(self):
        self._create_test_index_template()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        response = self._request_index_all_rebuild_get_view()
        self.assertContains(
            response=response, text=self.test_index_template.label,
            status_code=200
        )

        response = self._request_indexes_rebuild_post_view()
        self.assertEqual(response.status_code, 302)

        # An instance root exists.
        self.assertTrue(self.test_index_template.instance_root.pk)

    def test_index_all_reset_no_permission(self):
        self._create_test_index_template(add_test_document_type=True)
        self._create_test_index_template_node()
        self.test_index_template.rebuild()

        response = self._request_index_all_reset_get_view()
        self.assertNotContains(
            response=response, text=self.test_index_template.label,
            status_code=200
        )

        response = self._request_index_all_reset_post_view()
        # No error since we just don't see the index.
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_index_template.instance_root.get_children_count(), 1
        )

    def test_index_all_reset_with_access(self):
        self._create_test_index_template(add_test_document_type=True)
        self._create_test_index_template_node()
        self.test_index_template.rebuild()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        response = self._request_index_all_reset_get_view()
        self.assertContains(
            response=response, text=self.test_index_template.label,
            status_code=200
        )

        response = self._request_index_all_reset_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_index_template.instance_root.get_children_count(), 0
        )
