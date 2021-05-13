from mayan.apps.document_states.permissions import permission_workflow_template_edit
from mayan.apps.document_states.tests.base import ActionTestCase
from mayan.apps.document_states.tests.mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from mayan.apps.document_states.tests.mixins.workflow_template_state_mixins import WorkflowTemplateStateActionViewTestMixin
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..models import LayerTransformation
from ..workflow_actions import TransformationAddAction

from .literals import (
    TEST_TRANSFORMATION_ROTATE_ARGUMENT,
    TEST_TRANSFORMATION_ROTATE_NAME
)


class TransformationActionTestCase(ActionTestCase):
    def test_transformation_add_pages_all_action(self):
        action = TransformationAddAction(
            form_data={
                'pages': '',
                'transformation_class': TEST_TRANSFORMATION_ROTATE_NAME,
                'transformation_arguments': TEST_TRANSFORMATION_ROTATE_ARGUMENT
            }
        )

        transformation_count = LayerTransformation.objects.get_for_object(
            obj=self.test_document.pages.first()
        ).count()
        action.execute(context={'document': self.test_document})

        self.assertEqual(
            LayerTransformation.objects.get_for_object(
                obj=self.test_document.pages.first()
            ).count(), transformation_count + 1
        )

    def test_transformation_add_pages_first_action(self):
        action = TransformationAddAction(
            form_data={
                'pages': '1',
                'transformation_class': TEST_TRANSFORMATION_ROTATE_NAME,
                'transformation_arguments': TEST_TRANSFORMATION_ROTATE_ARGUMENT
            }
        )

        transformation_count = LayerTransformation.objects.get_for_object(
            obj=self.test_document.pages.first()
        ).count()
        action.execute(context={'document': self.test_document})

        self.assertEqual(
            LayerTransformation.objects.get_for_object(
                obj=self.test_document.pages.first()
            ).count(), transformation_count + 1
        )


class TransformationActionViewTestCase(
    WorkflowTemplateStateActionViewTestMixin, WorkflowTemplateTestMixin, GenericViewTestCase
):
    def test_transformation_add_pages_all_action_create_view(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_template_edit
        )

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path='mayan.apps.converter.workflow_actions.TransformationAddAction',
            extra_data={
                'pages': '',
                'transformation_class': TEST_TRANSFORMATION_ROTATE_NAME,
                'transformation_arguments': TEST_TRANSFORMATION_ROTATE_ARGUMENT
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_transformation_add_pages_first_action_create_view(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_template_edit
        )

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path='mayan.apps.converter.workflow_actions.TransformationAddAction',
            extra_data={
                'pages': '1',
                'transformation_class': TEST_TRANSFORMATION_ROTATE_NAME,
                'transformation_arguments': TEST_TRANSFORMATION_ROTATE_ARGUMENT
            }
        )
        self.assertEqual(response.status_code, 302)
