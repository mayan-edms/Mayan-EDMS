from __future__ import unicode_literals

from django.urls import reverse
from django.test import override_settings

from rest_api.tests import BaseAPITestCase

from ..classes import Template


class CommonAPITestCase(BaseAPITestCase):
    def test_content_type_list_view(self):
        response = self.client.get(reverse('rest_api:content-type-list'))
        self.assertEqual(response.status_code, 200)

    @override_settings(LANGUAGE_CODE='de')
    def test_template_detail_view(self):
        template_main_menu = Template.get(name='main_menu')
        response = self.client.get(template_main_menu.get_absolute_url())
        self.assertEqual(response.status_code, 200)
