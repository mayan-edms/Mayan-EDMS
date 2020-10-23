import json

from mayan.apps.document_states.tests.mixins import WorkflowTestMixin
from mayan.apps.document_states.literals import WORKFLOW_ACTION_ON_ENTRY
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import DocumentPageOCRContent
from ..workflow_actions import UpdateDocumentPageOCRAction

from .literals import (
    TEST_DOCUMENT_PAGE_TEST_CONTENT, TEST_DOCUMENT_PAGE_TEST_CONTENT_UPDATED,
    TEST_UPDATE_DOCUMENT_PAGE_OCR_ACTION_DOTTED_PATH
)


class UpdateDocumentPageOCRActionTestCase(
    WorkflowTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_update_document_page_action_no_page_condition(self):
        self._upload_test_document()

        document_page = self.test_document.pages_valid.first()
        DocumentPageOCRContent.objects.create(
            document_page=document_page, content=TEST_DOCUMENT_PAGE_TEST_CONTENT
        )

        action = UpdateDocumentPageOCRAction(
            form_data={
                'page_condition': '',
                'page_content': TEST_DOCUMENT_PAGE_TEST_CONTENT_UPDATED
            }
        )

        action.execute(context={'document': self.test_document})

        document_page.refresh_from_db()
        self.assertEqual(
            document_page.ocr_content.content, TEST_DOCUMENT_PAGE_TEST_CONTENT
        )

    def test_update_document_page_action_true_page_condition(self):
        self._upload_test_document()

        document_page = self.test_document.pages_valid.first()
        DocumentPageOCRContent.objects.create(
            document_page=document_page, content=TEST_DOCUMENT_PAGE_TEST_CONTENT
        )

        action = UpdateDocumentPageOCRAction(
            form_data={
                'page_condition': '{% if "test" in document_page.ocr_content.content %}Has "test"{% endif %}',
                'page_content': TEST_DOCUMENT_PAGE_TEST_CONTENT_UPDATED
            }
        )
        action.execute(context={'document': self.test_document})

        document_page.refresh_from_db()
        self.assertEqual(
            document_page.ocr_content.content,
            TEST_DOCUMENT_PAGE_TEST_CONTENT_UPDATED
        )

    def test_update_document_page_action_template_page_content(self):
        self._upload_test_document()

        document_page = self.test_document.pages_valid.first()
        DocumentPageOCRContent.objects.create(
            document_page=document_page, content=TEST_DOCUMENT_PAGE_TEST_CONTENT
        )

        action = UpdateDocumentPageOCRAction(
            form_data={
                'page_condition': '{% if "test" in document_page.ocr_content.content %}Has "test"{% endif %}',
                'page_content': '{{ document_page.ocr_content.content }}+update'
            }
        )
        action.execute(context={'document': self.test_document})

        document_page.refresh_from_db()
        self.assertEqual(
            document_page.ocr_content.content,
            '{}+update'.format(TEST_DOCUMENT_PAGE_TEST_CONTENT)
        )

    def test_update_document_page_action_execution(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self.test_workflow_states[1].actions.create(
            action_data=json.dumps(
                obj={
                    'page_condition': True,
                    'page_content': '{{ document.label }}'
                }
            ), action_path=TEST_UPDATE_DOCUMENT_PAGE_OCR_ACTION_DOTTED_PATH,
            label='', when=WORKFLOW_ACTION_ON_ENTRY
        )
        self.test_workflow.document_types.add(self.test_document_type)

        self._upload_test_document()

        self.test_document.workflows.first().do_transition(
            transition=self.test_workflow_transition
        )

        self.assertEqual(
            ''.join(self.test_document.ocr_content()), self.test_document.label
        )
