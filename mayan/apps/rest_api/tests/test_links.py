from django.test import override_settings

from mayan.apps.testing.tests.base import GenericViewTestCase

from ..links import (
    link_api, link_api_documentation, link_api_documentation_redoc
)


class RESTAPILinkTestCase(GenericViewTestCase):
    @override_settings(REST_API_DISABLE_LINKS=False)
    def test_api_link_false(self):
        response = self.get(viewname='common:tools_list')

        self.assertContains(
            response=response, text=link_api.text
        )

    @override_settings(REST_API_DISABLE_LINKS=True)
    def test_api_link_true(self):
        response = self.get(viewname='common:tools_list')

        self.assertNotContains(
            response=response, text=link_api.text
        )

    @override_settings(REST_API_DISABLE_LINKS=False)
    def test_redoc_documentation_link_false(self):
        response = self.get(viewname='common:tools_list')

        self.assertContains(
            response=response, text=link_api_documentation_redoc.text
        )

    @override_settings(REST_API_DISABLE_LINKS=True)
    def test_redoc_documentation_link_true(self):
        response = self.get(viewname='common:tools_list')

        self.assertNotContains(
            response=response, text=link_api_documentation_redoc.text
        )

    @override_settings(REST_API_DISABLE_LINKS=False)
    def test_swagger_documentation_link_false(self):
        response = self.get(viewname='common:tools_list')

        self.assertContains(
            response=response, text=link_api_documentation.text
        )

    @override_settings(REST_API_DISABLE_LINKS=True)
    def test_swagger_documentation_link_true(self):
        response = self.get(viewname='common:tools_list')

        self.assertNotContains(
            response=response, text=link_api_documentation.text
        )
