from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase


class CommonAPITestCase(APITestCase):
    def test_content_type_list_view(self):
        response = self.client.get(reverse('rest_api:content-type-list'))
        self.assertEqual(response.status_code, 200)
