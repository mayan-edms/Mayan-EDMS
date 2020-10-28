import unittest

from mayan.apps.common.tests.base import GenericViewTestCase

from .mixins import RESTAPIViewTestMixin


class RESTAPIViewTestCase(RESTAPIViewTestMixin, GenericViewTestCase):
    def test_browser_api_view(self):
        response = self._request_test_browser_api_view()
        self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_redoc_ui_view(self):
        response = self._request_test_redoc_ui_view()
        self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_swagger_ui_view(self):
        response = self._request_test_swagger_ui_view()
        self.assertEqual(response.status_code, 200)

    def test_swagger_no_ui_json_view(self):
        self.expected_content_types = ('application/json',)

        response = self._request_test_swagger_no_ui_json_view()
        self.assertEqual(response.status_code, 200)

    def test_swagger_no_ui_yaml_view(self):
        self.expected_content_types = ('application/yaml',)

        response = self._request_test_swagger_no_ui_yaml_view()
        self.assertEqual(response.status_code, 200)
