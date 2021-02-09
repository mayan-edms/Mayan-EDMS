import json

from mayan.apps.django_gpg.tests.literals import TEST_KEY_PRIVATE_PASSPHRASE
from mayan.apps.django_gpg.tests.mixins import KeyTestMixin
from mayan.apps.document_states.literals import WORKFLOW_ACTION_ON_ENTRY
from mayan.apps.document_states.permissions import permission_workflow_edit
from mayan.apps.document_states.tests.mixins import (
    WorkflowTestMixin, WorkflowStateActionViewTestMixin
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import DetachedSignature, EmbeddedSignature
from ..workflow_actions import (
    DocumentSignatureDetachedAction, DocumentSignatureEmbeddedAction
)

from .literals import (
    DOCUMENT_SIGNATURE_DETACHED_ACTION_CLASS_PATH,
    DOCUMENT_SIGNATURE_EMBEDDED_ACTION_CLASS_PATH
)


class DocumentSignatureWorkflowActionTestCase(
    GenericDocumentViewTestCase, KeyTestMixin, WorkflowTestMixin,
    WorkflowStateActionViewTestMixin
):
    auto_upload_test_document = False

    def test_document_signature_detached_action_create_view(self):
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_state()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        request = self._request_test_workflow_template_state_action_create_get_view(
            class_path=DOCUMENT_SIGNATURE_DETACHED_ACTION_CLASS_PATH
        )
        self.assertEqual(request.status_code, 200)

    def test_document_signature_embedded_action_create_view(self):
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_state()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        request = self._request_test_workflow_template_state_action_create_get_view(
            class_path=DOCUMENT_SIGNATURE_EMBEDDED_ACTION_CLASS_PATH
        )
        self.assertEqual(request.status_code, 200)

    def test_document_signature_detached_action(self):
        self._upload_test_document()
        self._create_test_key_private()
        signature_count = DetachedSignature.objects.count()

        action = DocumentSignatureDetachedAction(
            form_data={
                'key': self.test_key_private.pk,
                'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertNotEqual(signature_count, DetachedSignature.objects.count())

    def test_document_signature_embedded_action(self):
        self._upload_test_document()
        self._create_test_key_private()
        signature_count = EmbeddedSignature.objects.count()

        action = DocumentSignatureEmbeddedAction(
            form_data={
                'key': self.test_key_private.pk,
                'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertNotEqual(signature_count, EmbeddedSignature.objects.count())

    def test_document_signature_detached_action_via_workflow(self):
        self._create_test_workflow()
        self.test_workflow.document_types.add(self.test_document_type)
        self._create_test_workflow_states()
        self._create_test_workflow_transitions()
        self._create_test_key_private()

        self.test_workflow_state_2.actions.create(
            label='test action', when=WORKFLOW_ACTION_ON_ENTRY,
            enabled=True,
            action_path='mayan.apps.document_signatures.workflow_actions.DocumentSignatureDetachedAction',
            action_data=json.dumps(
                obj={
                    'key': self.test_key_private.pk,
                    'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
                }
            ),
        )

        self._upload_test_document()
        self.test_workflow_instance = self.test_document.workflows.first()

        signature_count = DetachedSignature.objects.count()

        self.test_workflow_instance.do_transition(
            transition=self.test_workflow_transition
        )
        self.assertNotEqual(signature_count, DetachedSignature.objects.count())

    def test_document_signature_embedded_action_via_workflow(self):
        self._create_test_workflow()
        self.test_workflow.document_types.add(self.test_document_type)
        self._create_test_workflow_states()
        self._create_test_workflow_transitions()
        self._create_test_key_private()

        self.test_workflow_state_2.actions.create(
            label='test action', when=WORKFLOW_ACTION_ON_ENTRY,
            enabled=True,
            action_path='mayan.apps.document_signatures.workflow_actions.DocumentSignatureEmbeddedAction',
            action_data=json.dumps(
                obj={
                    'key': self.test_key_private.pk,
                    'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
                }
            ),
        )

        self._upload_test_document()
        self.test_workflow_instance = self.test_document.workflows.first()

        signature_count = EmbeddedSignature.objects.count()

        self.test_workflow_instance.do_transition(
            transition=self.test_workflow_transition
        )
        self.assertNotEqual(signature_count, EmbeddedSignature.objects.count())
