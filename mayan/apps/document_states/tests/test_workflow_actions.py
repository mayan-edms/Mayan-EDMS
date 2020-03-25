import json
import mock

from mayan.apps.common.tests.mixins import TestServerTestCaseMixin
from mayan.apps.common.tests.mocks import request_method_factory
from mayan.apps.document_states.tests.mixins import WorkflowTestMixin
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.document_states.literals import WORKFLOW_ACTION_ON_ENTRY

from ..workflow_actions import DocumentPropertiesEditAction, HTTPAction

from .literals import (
    TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_DOTTED_PATH,
    TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_LABEL,
    TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_DESCRIPTION,
    TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_DATA,
    TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEMPLATE_DATA,
    TEST_HEADERS_AUTHENTICATION_KEY, TEST_HEADERS_AUTHENTICATION_VALUE,
    TEST_HEADERS_KEY, TEST_HEADERS_JSON, TEST_HEADERS_JSON_TEMPLATE,
    TEST_HEADERS_JSON_TEMPLATE_KEY, TEST_HEADERS_VALUE, TEST_PAYLOAD_JSON,
    TEST_PAYLOAD_TEMPLATE_DOCUMENT_LABEL, TEST_SERVER_USERNAME,
    TEST_SERVER_PASSWORD
)


class HTTPWorkflowActionTestCase(
    TestServerTestCaseMixin, GenericDocumentViewTestCase, WorkflowTestMixin,
):
    auto_upload_test_document = False
    auto_add_test_view = True

    @mock.patch('requests.sessions.Session.get_adapter')
    def test_http_post_action_simple(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPAction(
            form_data={
                'method': 'POST',
                'url': self.testserver_url
            }
        )
        action.execute(context={})

        self.assertFalse(self.test_view_request is None)

    @mock.patch('requests.sessions.Session.get_adapter')
    def test_http_post_action_payload_simple(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPAction(
            form_data={
                'payload': TEST_PAYLOAD_JSON,
                'url': self.testserver_url,
                'method': 'POST'
            }
        )
        action.execute(context={})

        self.assertEqual(
            json.loads(s=self.test_view_request.body),
            {'label': 'label'}
        )

    @mock.patch('requests.sessions.Session.get_adapter')
    def test_http_post_action_payload_template(self, mock_object):
        self._upload_test_document()
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPAction(
            form_data={
                'payload': TEST_PAYLOAD_TEMPLATE_DOCUMENT_LABEL,
                'url': self.testserver_url,
                'method': 'POST'
            }
        )
        action.execute(context={'document': self.test_document})

        self.assertEqual(
            json.loads(s=self.test_view_request.body),
            {'label': self.test_document.label}
        )

    @mock.patch('requests.sessions.Session.get_adapter')
    def test_http_post_action_headers_simple(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPAction(
            form_data={
                'headers': TEST_HEADERS_JSON,
                'url': self.testserver_url,
                'method': 'POST'
            }
        )
        action.execute(context={})

        self.assertTrue(
            TEST_HEADERS_KEY in self.test_view_request.META,
        )
        self.assertEqual(
            self.test_view_request.META[TEST_HEADERS_KEY], TEST_HEADERS_VALUE
        )

    @mock.patch('requests.sessions.Session.get_adapter')
    def test_http_post_action_headers_template(self, mock_object):
        self._upload_test_document()
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPAction(
            form_data={
                'headers': TEST_HEADERS_JSON_TEMPLATE,
                'url': self.testserver_url,
                'method': 'POST'
            }
        )
        action.execute(context={'document': self.test_document})

        self.assertTrue(
            TEST_HEADERS_JSON_TEMPLATE_KEY in self.test_view_request.META,
        )
        self.assertEqual(
            self.test_view_request.META[TEST_HEADERS_JSON_TEMPLATE_KEY],
            self.test_document.label
        )

    @mock.patch('requests.sessions.Session.get_adapter')
    def test_http_post_action_authentication(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPAction(
            form_data={
                'password': TEST_SERVER_PASSWORD,
                'url': self.testserver_url,
                'username': TEST_SERVER_USERNAME,
                'method': 'POST'
            }
        )
        action.execute(context={})

        self.assertTrue(
            TEST_HEADERS_AUTHENTICATION_KEY in self.test_view_request.META,
        )
        self.assertEqual(
            self.test_view_request.META[TEST_HEADERS_AUTHENTICATION_KEY],
            TEST_HEADERS_AUTHENTICATION_VALUE
        )

    @mock.patch('requests.sessions.Session.get_adapter')
    def test_http_post_action_timeout_value_int(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPAction(
            form_data={
                'timeout': '1',
                'url': self.testserver_url,
                'method': 'POST'
            }
        )
        action.execute(context={})

        self.assertEqual(self.timeout, 1)

    @mock.patch('requests.sessions.Session.get_adapter')
    def test_http_post_action_timeout_value_float(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPAction(
            form_data={
                'timeout': '1.5',
                'url': self.testserver_url,
                'method': 'POST'
            }
        )
        action.execute(context={})

        self.assertEqual(self.timeout, 1.5)

    @mock.patch('requests.sessions.Session.get_adapter')
    def test_http_post_action_timeout_value_none(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPAction(
            form_data={
                'url': self.testserver_url,
                'method': 'POST'
            }
        )
        action.execute(context={})

        self.assertEqual(self.timeout, None)


class DocumentPropertiesEditActionTestCase(
    WorkflowTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_properties_edit_action_field_literals(self):
        self._upload_test_document()

        action = DocumentPropertiesEditAction(
            form_data=TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_DATA
        )

        test_values = self._model_instance_to_dictionary(
            instance=self.test_document
        )

        action.execute(context={'document': self.test_document})
        self.test_document.refresh_from_db()

        self.assertNotEqual(
            test_values, self._model_instance_to_dictionary(
                instance=self.test_document
            )
        )

    def test_document_properties_edit_action_field_templates(self):
        self._upload_test_document()

        label = self.test_document.label

        action = DocumentPropertiesEditAction(
            form_data=TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEMPLATE_DATA
        )
        action.execute(context={'document': self.test_document})

        self.assertEqual(
            self.test_document.label,
            '{} new'.format(label)
        )
        self.assertEqual(
            self.test_document.description,
            label
        )

    def test_document_properties_edit_action_workflow_execute(self):
        self._create_test_workflow()
        self._create_test_workflow_state()

        self.test_workflow_state.actions.create(
            action_data=json.dumps(
                obj=TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_DATA
            ),
            action_path=TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_DOTTED_PATH,
            label='', when=WORKFLOW_ACTION_ON_ENTRY,
        )

        self.test_workflow_state.initial = True
        self.test_workflow_state.save()
        self.test_workflow.document_types.add(self.test_document_type)

        self._upload_test_document()

        self.assertEqual(
            self.test_document.label,
            TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_LABEL
        )
        self.assertEqual(
            self.test_document.description,
            TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_DESCRIPTION
        )
