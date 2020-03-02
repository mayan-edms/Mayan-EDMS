from __future__ import unicode_literals

from django.test import override_settings

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..classes import Template

TEST_TEMPLATE_RESULT = '<div'


class ContentTypeAPITestMixin(object):
    def _request_content_type_list_api_view(self):
        return self.get(viewname='rest_api:content_type-list')


class ContentTypeAPITestCase(ContentTypeAPITestMixin, BaseAPITestCase):
    auto_login_user = False

    def test_content_type_list_api_view(self):
        response = self._request_content_type_list_api_view()
        self.assertEqual(response.status_code, 200)


class TemplateAPITestMixin(object):
    def _request_test_template_list_api_view(self):
        return self.get(viewname='rest_api:template-list')

    def _request_test_template_retrieve_api_view(self):
        return self.get(
            viewname='rest_api:template-detail', kwargs={
                'template_name': self.test_template.name
            }
        )


class TemplateAPITestCase(TemplateAPITestMixin, BaseAPITestCase):
    auto_login_user = False

    def test_template_list_api_view(self):
        self.login_user()

        response = self._request_test_template_list_api_view()
        self.assertEqual(response.data['count'], len(Template.all()))

    def test_template_retrieve_anonymous_api_view(self):
        self.test_template = Template.get(name='menu_main')

        response = self._request_test_template_retrieve_api_view()
        self.assertNotContains(
            response=response, text=TEST_TEMPLATE_RESULT, status_code=403
        )
        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )

    @override_settings(LANGUAGE_CODE='de')
    def test_template_retrieve_api_view(self):
        self.login_user()
        self.test_template = Template.get(name='menu_main')

        response = self._request_test_template_retrieve_api_view()
        self.assertContains(
            response=response, text=TEST_TEMPLATE_RESULT, status_code=200
        )
