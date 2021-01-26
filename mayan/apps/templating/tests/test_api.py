from django.test import override_settings

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..classes import AJAXTemplate

from .literals import TEST_AJAXTEMPLATE_RESULT


class AJAXTemplateAPIViewTestCase(BaseAPITestCase):
    auto_login_user = False

    def test_template_detail_anonymous_api_view(self):
        template_main_menu = AJAXTemplate.get(name='menu_main')

        response = self.get(path=template_main_menu.get_absolute_url())
        self.assertNotContains(
            response=response, text=TEST_AJAXTEMPLATE_RESULT, status_code=403
        )

    @override_settings(LANGUAGE_CODE='de')
    def test_template_detail_api_view(self):
        self.login_user()
        template_main_menu = AJAXTemplate.get(name='menu_main')

        response = self.get(path=template_main_menu.get_absolute_url())
        self.assertContains(
            response=response, text=TEST_AJAXTEMPLATE_RESULT, status_code=200
        )
