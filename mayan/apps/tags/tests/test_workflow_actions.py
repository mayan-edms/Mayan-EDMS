from mayan.apps.document_states.events import event_workflow_template_edited
from mayan.apps.document_states.permissions import permission_workflow_template_edit
from mayan.apps.document_states.tests.base import ActionTestCase
from mayan.apps.document_states.tests.mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from mayan.apps.document_states.tests.mixins.workflow_template_state_mixins import WorkflowTemplateStateActionViewTestMixin
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_tag_attached, event_tag_removed
from ..models import Tag
from ..workflow_actions import AttachTagAction, RemoveTagAction

from .mixins import TagTestMixin


class TagWorkflowActionTestCase(TagTestMixin, ActionTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_tag()

    def test_tag_attach_action(self):
        self._clear_events()

        action = AttachTagAction(form_data={'tags': Tag.objects.all()})
        action.execute(context={'document': self._test_document})

        self.assertEqual(self._test_tag.documents.count(), 1)
        self.assertTrue(
            self._test_document in self._test_tag.documents.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_tag)
        self.assertEqual(events[0].actor, self._test_document)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_tag_attached.id)

    def test_tag_remove_action(self):
        self._test_tag.attach_to(document=self._test_document)

        self._clear_events()

        action = RemoveTagAction(form_data={'tags': Tag.objects.all()})
        action.execute(context={'document': self._test_document})

        self.assertEqual(self._test_tag.documents.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_tag)
        self.assertEqual(events[0].actor, self._test_document)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_tag_removed.id)


class TagWorkflowActionViewTestCase(
    WorkflowTemplateStateActionViewTestMixin, WorkflowTemplateTestMixin,
    GenericViewTestCase
):
    def test_tag_attach_action_create_view(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path='mayan.apps.tags.workflow_actions.AttachTagAction'
        )
        self.assertEqual(response.status_code, 302)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object,
            self._test_workflow_template_state_action
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_tag_remove_action_create_view(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path='mayan.apps.tags.workflow_actions.RemoveTagAction'
        )
        self.assertEqual(response.status_code, 302)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object,
            self._test_workflow_template_state_action
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)
