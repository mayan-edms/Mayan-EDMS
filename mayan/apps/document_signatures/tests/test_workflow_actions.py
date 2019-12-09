from __future__ import unicode_literals

from mayan.apps.django_gpg.tests.literals import TEST_KEY_PRIVATE_PASSPHRASE
from mayan.apps.django_gpg.tests.mixins import KeyTestMixin
from mayan.apps.document_states.tests.mixins import WorkflowTestMixin
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import DetachedSignature, EmbeddedSignature
from ..workflow_actions import (
    DocumentSignatureDetachedAction, DocumentSignatureEmbeddedAction
)


class DocumentSignatureWorkflowActionTestCase(
    GenericDocumentViewTestCase, KeyTestMixin, WorkflowTestMixin,
):
    def test_document_signature_detached_action(self):
        self._create_test_key_private()
        signature_count = DetachedSignature.objects.count()

        action = DocumentSignatureDetachedAction(
            form_data={
                'key': self.test_key_private,
                'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertNotEqual(signature_count, DetachedSignature.objects.count())

    def test_document_signature_embedded_action(self):
        self._create_test_key_private()
        signature_count = EmbeddedSignature.objects.count()

        action = DocumentSignatureEmbeddedAction(
            form_data={
                'key': self.test_key_private,
                'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertNotEqual(signature_count, EmbeddedSignature.objects.count())
