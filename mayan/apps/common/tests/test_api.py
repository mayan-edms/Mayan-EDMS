from django.test import override_settings

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..classes import Template

TEST_TEMPLATE_RESULT = '<div'


class CommonAPITestCase(BaseAPITestCase):
    auto_login_user = False

    def _request_content_type_list_api_view(self):
        return self.get(viewname='rest_api:content-type-list')

    def test_content_type_list_api_view(self):
        response = self._request_content_type_list_api_view()
        self.assertEqual(response.status_code, 200)

    def test_template_detail_anonymous_view(self):
        template_main_menu = Template.get(name='menu_main')

        response = self.get(path=template_main_menu.get_absolute_url())
        self.assertNotContains(
            response=response, text=TEST_TEMPLATE_RESULT, status_code=403
        )

    @override_settings(LANGUAGE_CODE='de')
    def test_template_detail_view(self):
        self.login_user()
        template_main_menu = Template.get(name='menu_main')

        response = self.get(path=template_main_menu.get_absolute_url())
        self.assertContains(
            response=response, text=TEST_TEMPLATE_RESULT, status_code=200
        )
