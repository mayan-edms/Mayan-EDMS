from mayan.apps.document_states.permissions import permission_workflow_template_edit
from mayan.apps.document_states.tests.base import ActionTestCase
from mayan.apps.document_states.tests.mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from mayan.apps.document_states.tests.mixins.workflow_template_state_mixins import WorkflowTemplateStateActionViewTestMixin

from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import (
    event_cabinet_document_added, event_cabinet_document_removed
)
from ..models import Cabinet
from ..workflow_actions import CabinetAddAction, CabinetRemoveAction

from .mixins import CabinetTestMixin


class CabinetWorkflowActionTestCase(CabinetTestMixin, ActionTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_cabinet()

    def test_cabinet_document_add_action(self):
        action = CabinetAddAction(
            form_data={'cabinets': Cabinet.objects.all()}
        )

        self._clear_events()

        action.execute(context={'document': self._test_document})

        self.assertTrue(
            self._test_document in self._test_cabinet.documents.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_cabinet)
        self.assertEqual(events[0].actor, self._test_document)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_cabinet_document_added.id)

    def test_cabinet_document_remove_action(self):
        self._test_cabinet.document_add(document=self._test_document)

        action = CabinetRemoveAction(
            form_data={'cabinets': Cabinet.objects.all()}
        )

        self._clear_events()

        action.execute(context={'document': self._test_document})

        self.assertFalse(
            self._test_document in self._test_cabinet.documents.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_cabinet)
        self.assertEqual(events[0].actor, self._test_document)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_cabinet_document_removed.id)


class CabinetWorkflowActionViewTestCase(
    CabinetTestMixin, WorkflowTemplateStateActionViewTestMixin,
    WorkflowTemplateTestMixin, GenericViewTestCase
):
    def test_cabinet_add_action_create_get_view(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        response = self._request_test_workflow_template_state_action_create_get_view(
            class_path='mayan.apps.cabinets.workflow_actions.CabinetAddAction'
        )
        self.assertEqual(response.status_code, 200)

    def test_cabinet_remove_action_create_get_view(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_cabinet()
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        response = self._request_test_workflow_template_state_action_create_get_view(
            class_path='mayan.apps.cabinets.workflow_actions.CabinetRemoveAction'
        )
        self.assertEqual(response.status_code, 200)
