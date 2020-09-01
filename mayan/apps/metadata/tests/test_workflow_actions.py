from mayan.apps.document_states.permissions import permission_workflow_edit
from mayan.apps.document_states.tests.base import ActionTestCase
from mayan.apps.document_states.tests.mixins import (
    WorkflowTestMixin, WorkflowStateActionViewTestMixin
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import MetadataType
from ..workflow_actions import (
    DocumentMetadataAddAction, DocumentMetadataEditAction,
    DocumentMetadataRemoveAction
)
from ..permissions import (
    permission_document_metadata_add, permission_document_metadata_edit,
    permission_document_metadata_remove
)

from .literals import TEST_METADATA_VALUE
from .mixins import DocumentMetadataMixin, MetadataTypeTestMixin

DOCUMENT_METADATA_ADD_ACTION_CLASS_PATH = 'mayan.apps.metadata.workflow_actions.DocumentMetadataAddAction'
DOCUMENT_METADATA_EDIT_ACTION_CLASS_PATH = 'mayan.apps.metadata.workflow_actions.DocumentMetadataEditAction'
DOCUMENT_METADATA_REMOVE_ACTION_CLASS_PATH = 'mayan.apps.metadata.workflow_actions.DocumentMetadataRemoveAction'


class DocumentMetadataActionTestCase(
    DocumentMetadataMixin, MetadataTypeTestMixin, ActionTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

    def test_document_metadata_add_action(self):
        action = DocumentMetadataAddAction(
            form_data={'metadata_types': MetadataType.objects.all()}
        )

        metadata_count = self.test_document.metadata.count()
        action.execute(context={'document': self.test_document})

        self.assertEqual(
            self.test_document.metadata.count(), metadata_count + 1
        )
        self.assertTrue(
            self.test_document.metadata.filter(
                metadata_type=self.test_metadata_type
            ).exists()
        )

    def test_document_metadata_edit_action(self):
        self._create_test_document_metadata()

        action = DocumentMetadataEditAction(
            form_data={
                'metadata_type': self.test_metadata_type.pk,
                'value': TEST_METADATA_VALUE
            }
        )

        metadata_value = self.test_document.metadata.first().value
        action.execute(context={'document': self.test_document})

        self.assertNotEqual(
            metadata_value, self.test_document.metadata.first().value
        )

    def test_document_metadata_remove_action(self):
        self._create_test_document_metadata()

        action = DocumentMetadataRemoveAction(
            form_data={'metadata_types': MetadataType.objects.all()}
        )

        metadata_count = self.test_document.metadata.count()
        action.execute(context={'document': self.test_document})

        self.assertEqual(
            self.test_document.metadata.count(), metadata_count - 1
        )
        self.assertFalse(
            self.test_document.metadata.filter(
                metadata_type=self.test_metadata_type
            ).exists()
        )


class DocumentMetadataActionViewTestCase(
    DocumentMetadataMixin, MetadataTypeTestMixin,
    WorkflowStateActionViewTestMixin, WorkflowTestMixin,
    GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow()
        self._create_test_workflow_state()
        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.test_workflow.document_types.add(
            self.test_document_type
        )

    def test_document_metadata_add_action_create_view(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path=DOCUMENT_METADATA_ADD_ACTION_CLASS_PATH, extra_data={
                'metadata_types': self.test_metadata_type.pk
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_document_metadata_edit_action_create_view(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path=DOCUMENT_METADATA_EDIT_ACTION_CLASS_PATH, extra_data={
                'metadata_type': self.test_metadata_type.pk,
                'value': TEST_METADATA_VALUE
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_document_metadata_remove_action_create_view(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path=DOCUMENT_METADATA_REMOVE_ACTION_CLASS_PATH, extra_data={
                'metadata_types': self.test_metadata_type.pk
            }
        )
        self.assertEqual(response.status_code, 302)
