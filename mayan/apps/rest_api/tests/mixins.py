from django.conf.urls import url
from django.urls import clear_url_caches

from rest_framework.authtoken.models import Token

from mayan.apps.testing.tests.mixins import TestViewTestCaseMixin


class APIUserTestCaseMixin:
    def setUp(self):
        super().setUp()
        self._test_case_user_token = self.get_test_user_token(
            user=self._test_case_user
        )

    def get_test_user_token(self, user):
        token, created = Token.objects.get_or_create(
            user=user
        )

        return token


class RESTAPIViewTestMixin:
    def _request_test_browser_api_view(self):
        return self.get(query={'format': 'api'}, viewname='rest_api:api_root')

    def _request_test_redoc_ui_view(self):
        return self.get(viewname='rest_api:schema-redoc')

    def _request_test_swagger_ui_view(self):
        return self.get(viewname='rest_api:schema-swagger-ui')

    def _request_test_swagger_no_ui_json_view(self):
        return self.get(
            kwargs={'format': '.json'}, viewname='rest_api:schema-json'
        )

    def _request_test_swagger_no_ui_yaml_view(self):
        return self.get(
            kwargs={'format': '.yaml'}, viewname='rest_api:schema-json'
        )


class TestAPIViewTestCaseMixin(TestViewTestCaseMixin):
    def add_test_view(self, test_object=None):
        from ..urls import api_urls as urlpatterns

        urlpatterns.insert(
            0, url(
                regex=self.test_view_url, view=self._test_view_factory(
                    test_object=test_object
                ), name=self.test_view_name
            )
        )
        clear_url_caches()
        self.has_test_view = True
