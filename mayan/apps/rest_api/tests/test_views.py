import unittest

from django.db import connection

from mayan.apps.testing.tests.base import GenericViewTestCase

from .mixins import RESTAPIViewTestMixin


class RESTAPIViewTestCase(RESTAPIViewTestMixin, GenericViewTestCase):
    def test_browser_api_view(self):
        response = self._request_test_browser_api_view()
        self.assertEqual(response.status_code, 200)

    @unittest.skipIf(connection.vendor != 'sqlite', 'Skip for known Django issues #15802 and #27074')
    def test_redoc_ui_view(self):
        response = self._request_test_redoc_ui_view()
        self.assertEqual(response.status_code, 200)

    @unittest.skipIf(connection.vendor != 'sqlite', 'Skip for known Django issues #15802 and #27074')
    def test_swagger_ui_view(self):
        response = self._request_test_swagger_ui_view()
        self.assertEqual(response.status_code, 200)

    def test_swagger_no_ui_json_view(self):
        self.expected_content_types = ('application/json; charset=utf-8',)

        response = self._request_test_swagger_no_ui_json_view()
        self.assertEqual(response.status_code, 200)

    def test_swagger_no_ui_yaml_view(self):
        self.expected_content_types = ('application/yaml; charset=utf-8',)

        response = self._request_test_swagger_no_ui_yaml_view()
        self.assertEqual(response.status_code, 200)
