from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from .mixins import CommonAPITestMixin


class CommonAPITestCase(CommonAPITestMixin, BaseAPITestCase):
    auto_login_user = False

    def test_content_type_list_api_view(self):
        response = self._request_content_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
