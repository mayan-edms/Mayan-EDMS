import json

from mayan.apps.document_states.events import event_workflow_instance_transitioned
from mayan.apps.document_states.literals import WORKFLOW_ACTION_ON_ENTRY
from mayan.apps.document_states.tests.mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from mayan.apps.documents.tests.base import (
    GenericDocumentTestCase, GenericDocumentViewTestCase
)

from ..events import event_message_created
from ..models import Message
from ..workflow_actions import WorkflowActionMessageSend

from .literals import TEST_MESSAGE_BODY, TEST_MESSAGE_SUBJECT


class WorkflowActionMessageSendTestCase(
    WorkflowTemplateTestMixin, GenericDocumentTestCase
):
    def test_message_send_workflow_action(self):
        action = WorkflowActionMessageSend(
            form_data={
                'body': TEST_MESSAGE_BODY,
                'subject': TEST_MESSAGE_SUBJECT,
                'username_list': self._test_case_user.username
            }
        )

        test_message_count = Message.objects.count()

        self._clear_events()

        action.execute(context={})

        self.assertEqual(
            Message.objects.count(), test_message_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, Message.objects.first())
        self.assertEqual(events[0].target, Message.objects.first())
        self.assertEqual(events[0].verb, event_message_created.id)


class WorkflowActionMessageSendViewTestCase(
    WorkflowTemplateTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_message_send_workflow_action(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

        action_data = json.dumps(
            obj={
                'body': TEST_MESSAGE_BODY,
                'subject': TEST_MESSAGE_SUBJECT,
                'username_list': self._test_case_user.username
            }
        )

        self._test_workflow_template_states[1].actions.create(
            action_data=action_data,
            action_path=WorkflowActionMessageSend.backend_id,
            label='', when=WORKFLOW_ACTION_ON_ENTRY,
        )
        self._test_workflow_template.document_types.add(
            self._test_document_type
        )

        self._create_test_document_stub()

        self._clear_events()

        self._test_document.workflows.first().do_transition(
            transition=self._test_workflow_template_transition
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, Message.objects.first())
        self.assertEqual(events[0].target, Message.objects.first())
        self.assertEqual(events[0].verb, event_message_created.id)

        self.assertEqual(events[1].action_object, self._test_document)
        self.assertEqual(
            events[1].actor, self._test_document.workflows.first()
        )
        self.assertEqual(
            events[1].target, self._test_document.workflows.first()
        )
        self.assertEqual(
            events[1].verb, event_workflow_instance_transitioned.id
        )
