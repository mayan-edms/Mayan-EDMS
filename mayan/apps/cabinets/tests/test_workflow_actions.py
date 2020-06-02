from mayan.apps.tests.tests.base import GenericViewTestCase
from mayan.apps.document_states.permissions import permission_workflow_edit
from mayan.apps.document_states.tests.base import ActionTestCase
from mayan.apps.document_states.tests.mixins import (
    WorkflowStateActionViewTestMixin, WorkflowTestMixin
)

from ..models import Cabinet
from ..workflow_actions import CabinetAddAction, CabinetRemoveAction

from .mixins import CabinetTestMixin


class CabinetWorkflowActionTestCase(CabinetTestMixin, ActionTestCase):
    def setUp(self):
        super(CabinetWorkflowActionTestCase, self).setUp()
        self._create_test_cabinet()

    def test_cabinet_add_action(self):
        action = CabinetAddAction(
            form_data={'cabinets': Cabinet.objects.all()}
        )
        action.execute(context={'document': self.test_document})

        self.assertTrue(
            self.test_document in self.test_cabinet.documents.all()
        )

    def test_cabinet_remove_action(self):
        self.test_cabinet.document_add(document=self.test_document)

        action = CabinetRemoveAction(
            form_data={'cabinets': Cabinet.objects.all()}
        )
        action.execute(context={'document': self.test_document})

        self.assertFalse(
            self.test_document in self.test_cabinet.documents.all()
        )


class CabinetWorkflowActionViewTestCase(
    CabinetTestMixin, WorkflowStateActionViewTestMixin, WorkflowTestMixin,
    GenericViewTestCase
):
    def test_cabinet_add_action_create_get_view(self):
        self._create_test_workflow()
        self._create_test_workflow_state()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_template_state_action_create_get_view(
            class_path='mayan.apps.cabinets.workflow_actions.CabinetAddAction'
        )
        self.assertEqual(response.status_code, 200)

    def test_cabinet_remove_action_create_get_view(self):
        self._create_test_workflow()
        self._create_test_workflow_state()
        self._create_test_cabinet()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_template_state_action_create_get_view(
            class_path='mayan.apps.cabinets.workflow_actions.CabinetRemoveAction'
        )
        self.assertEqual(response.status_code, 200)
