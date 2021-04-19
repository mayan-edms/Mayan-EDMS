import json

from mayan.apps.document_states.literals import WORKFLOW_ACTION_ON_ENTRY
from mayan.apps.document_states.tests.mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import DocumentVersionPageOCRContent
from ..workflow_actions import UpdateDocumentPageOCRAction

from .literals import (
    TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT,
    TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT_UPDATED,
    TEST_UPDATE_DOCUMENT_PAGE_OCR_ACTION_DOTTED_PATH
)


class UpdateDocumentPageOCRActionTestCase(
    WorkflowTemplateTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_workflow_action_document_version_page_update_action_no_page_condition_execution(self):
        self._upload_test_document()

        document_version_page = self.test_document_version.pages.first()
        DocumentVersionPageOCRContent.objects.create(
            document_version_page=document_version_page,
            content=TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT
        )

        action = UpdateDocumentPageOCRAction(
            form_data={
                'page_condition': '',
                'page_content': TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT_UPDATED
            }
        )

        action.execute(context={'document': self.test_document})

        document_version_page.refresh_from_db()
        self.assertEqual(
            document_version_page.ocr_content.content,
            TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT
        )

    def test_workflow_action_document_version_page_update_action_template_page_content_execution(self):
        self._upload_test_document()

        document_version_page = self.test_document_version.pages.first()
        DocumentVersionPageOCRContent.objects.create(
            document_version_page=document_version_page,
            content=TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT
        )

        action = UpdateDocumentPageOCRAction(
            form_data={
                'page_condition': '{% if "test" in document_version_page.ocr_content.content %}Has "test"{% endif %}',
                'page_content': TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT_UPDATED
            }
        )
        action.execute(context={'document': self.test_document})

        document_version_page.refresh_from_db()
        self.assertEqual(
            document_version_page.ocr_content.content,
            TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT_UPDATED
        )

    def test_workflow_action_update_document_version_page_action_template_page_content_execution(self):
        self._upload_test_document()

        document_version_page = self.test_document_version.pages.first()
        DocumentVersionPageOCRContent.objects.create(
            document_version_page=document_version_page,
            content=TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT
        )

        action = UpdateDocumentPageOCRAction(
            form_data={
                'page_condition': '{% if "test" in document_version_page.ocr_content.content %}Has "test"{% endif %}',
                'page_content': '{{ document_version_page.ocr_content.content }}+update'
            }
        )
        action.execute(context={'document': self.test_document})

        document_version_page.refresh_from_db()
        self.assertEqual(
            document_version_page.ocr_content.content,
            '{}+update'.format(TEST_DOCUMENT_VERSION_PAGE_OCR_CONTENT)
        )

    def test_workflow_action_update_document_version_page_execution(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self.test_workflow_template_states[1].actions.create(
            action_data=json.dumps(
                obj={
                    'page_condition': True,
                    'page_content': '{{ document.label }}'
                }
            ), action_path=TEST_UPDATE_DOCUMENT_PAGE_OCR_ACTION_DOTTED_PATH,
            label='', when=WORKFLOW_ACTION_ON_ENTRY
        )
        self.test_workflow_template.document_types.add(self.test_document_type)

        self._upload_test_document()

        self.test_document.workflows.first().do_transition(
            transition=self.test_workflow_template_transition
        )

        self.assertEqual(
            ''.join(self.test_document.ocr_content()), self.test_document.label
        )
