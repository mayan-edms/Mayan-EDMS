from mayan.apps.document_states.permissions import permission_workflow_edit
from mayan.apps.document_states.tests.base import ActionTestCase
from mayan.apps.document_states.tests.mixins import (
    WorkflowStateActionViewTestMixin, WorkflowTestMixin
)
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..models import Tag
from ..workflow_actions import AttachTagAction, RemoveTagAction

from .mixins import TagTestMixin


class TagActionTestCase(TagTestMixin, ActionTestCase):
    def setUp(self):
        super(TagActionTestCase, self).setUp()
        self._create_test_tag()

    def test_tag_attach_action(self):
        action = AttachTagAction(form_data={'tags': Tag.objects.all()})
        action.execute(context={'document': self.test_document})

        self.assertEqual(self.test_tag.documents.count(), 1)
        self.assertTrue(self.test_document in self.test_tag.documents.all())

    def test_tag_remove_action(self):
        self.test_tag.attach_to(document=self.test_document)

        action = RemoveTagAction(form_data={'tags': Tag.objects.all()})
        action.execute(context={'document': self.test_document})

        self.assertEqual(self.test_tag.documents.count(), 0)


class TagActionViewTestCase(
    WorkflowStateActionViewTestMixin, WorkflowTestMixin, GenericViewTestCase
):
    def test_tag_attach_action_create_view(self):
        self._create_test_workflow()
        self._create_test_workflow_state()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path='mayan.apps.tags.workflow_actions.AttachTagAction'
        )
        self.assertEqual(response.status_code, 302)

    def test_tag_remove_action_create_view(self):
        self._create_test_workflow()
        self._create_test_workflow_state()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path='mayan.apps.tags.workflow_actions.RemoveTagAction'
        )
        self.assertEqual(response.status_code, 302)
