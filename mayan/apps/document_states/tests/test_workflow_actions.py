from __future__ import unicode_literals

import json
import mock

from mayan.apps.common.tests.base import GenericViewTestCase
from mayan.apps.common.tests.mixins import TestServerTestCaseMixin
from mayan.apps.common.tests.mocks import request_method_factory
from mayan.apps.document_states.tests.mixins import WorkflowTestMixin
from mayan.apps.document_states.tests.base import ActionTestCase

from ..workflow_actions import HTTPPostAction

from .literals import (
    TEST_HEADERS_AUTHENTICATION_KEY, TEST_HEADERS_AUTHENTICATION_VALUE,
    TEST_HEADERS_KEY, TEST_HEADERS_JSON, TEST_HEADERS_JSON_TEMPLATE,
    TEST_HEADERS_JSON_TEMPLATE_KEY, TEST_HEADERS_VALUE, TEST_PAYLOAD_JSON,
    TEST_PAYLOAD_TEMPLATE_DOCUMENT_LABEL, TEST_SERVER_USERNAME,
    TEST_SERVER_PASSWORD
)


class HTTPPostWorkflowActionTestCase(
    TestServerTestCaseMixin, GenericViewTestCase, WorkflowTestMixin,
    ActionTestCase
):
    auto_add_test_view = True

    @mock.patch('requests.api.request')
    def test_http_post_action_simple(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPPostAction(
            form_data={
                'url': self.testserver_url,
            }
        )
        action.execute(context={'document': self.test_document})

        self.assertFalse(self.test_view_request is None)

    @mock.patch('requests.api.request')
    def test_http_post_action_payload_simple(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPPostAction(
            form_data={
                'url': self.testserver_url,
                'payload': TEST_PAYLOAD_JSON,
            }
        )
        action.execute(context={'document': self.test_document})

        self.assertEqual(
            json.loads(self.test_view_request.body),
            {'label': 'label'}
        )

    @mock.patch('requests.api.request')
    def test_http_post_action_payload_template(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPPostAction(
            form_data={
                'url': self.testserver_url,
                'payload': TEST_PAYLOAD_TEMPLATE_DOCUMENT_LABEL,
            }
        )
        action.execute(context={'document': self.test_document})

        self.assertEqual(
            json.loads(self.test_view_request.body),
            {'label': self.test_document.label}
        )

    @mock.patch('requests.api.request')
    def test_http_post_action_headers_simple(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPPostAction(
            form_data={
                'url': self.testserver_url,
                'headers': TEST_HEADERS_JSON,
            }
        )
        action.execute(context={'document': self.test_document})

        self.assertTrue(
            TEST_HEADERS_KEY in self.test_view_request.META,
        )
        self.assertEqual(
            self.test_view_request.META[TEST_HEADERS_KEY], TEST_HEADERS_VALUE
        )

    @mock.patch('requests.api.request')
    def test_http_post_action_headers_template(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPPostAction(
            form_data={
                'url': self.testserver_url,
                'headers': TEST_HEADERS_JSON_TEMPLATE,
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

    @mock.patch('requests.api.request')
    def test_http_post_action_authentication(self, mock_object):
        mock_object.side_effect = request_method_factory(test_case=self)

        action = HTTPPostAction(
            form_data={
                'url': self.testserver_url,
                'username': TEST_SERVER_USERNAME,
                'password': TEST_SERVER_PASSWORD
            }
        )
        action.execute(context={'document': self.test_document})

        self.assertTrue(
            TEST_HEADERS_AUTHENTICATION_KEY in self.test_view_request.META,
        )
        self.assertEqual(
            self.test_view_request.META[TEST_HEADERS_AUTHENTICATION_KEY],
            TEST_HEADERS_AUTHENTICATION_VALUE
        )
