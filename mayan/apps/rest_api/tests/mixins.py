from django.db import models

from rest_framework.authtoken.models import Token

from mayan.apps.testing.tests.mixins import TestViewTestCaseMixin

from .. import serializers


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


class DynamicFieldSerializerAPIViewTestCaseMixin:
    auto_add_test_view = True
    auto_create_test_object = False
    test_view_url = r'^test-view-url/(?P<test_object_id>\d+)/$'

    def _test_view_factory(self, test_object=None):
        self.TestModelParent = self._create_test_model(
            fields={
                'test_field_1': models.CharField(
                    blank=True, max_length=1
                ),
                'test_field_2': models.CharField(
                    blank=True, max_length=1
                )
            }, model_name='TestModelParent'
        )

        self.TestModelChild = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelParent',
                ),
                'test_field_3': models.CharField(
                    blank=True, max_length=1
                ),
                'test_field_4': models.CharField(
                    blank=True, max_length=1
                )
            }, model_name='TestModelChild'
        )

        self._test_object_parent = self.TestModelParent.objects.create()
        self._test_object_child = self.TestModelChild.objects.create(
            parent=self._test_object_parent
        )

        TestModelParent = self.TestModelParent
        TestModelChild = self.TestModelChild

        class TestModelParentSerializer(serializers.ModelSerializer):
            class Meta:
                fields = ('id', 'test_field_1', 'test_field_2')
                model = TestModelParent

        class TestModelChildSerializer(serializers.ModelSerializer):
            parent = TestModelParentSerializer()

            class Meta:
                fields = ('parent', 'id', 'test_field_3', 'test_field_4')
                model = TestModelChild

        class TestView(
            self._get_test_view_class(
                serializer_class=TestModelChildSerializer
            )
        ):
            """
            Flat subclass to allow the test class view to be called without
            code changes.
            """

        return TestView.as_view()

    def _request_test_api_view(self, query):
        return self.get(
            viewname='rest_api:{}'.format(self._test_view_name), kwargs={
                'test_object_id': self._test_object_child.pk,
            }, query=query
        )


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
    def _get_test_view_urlpatterns(self):
        from ..urls import api_version_urls
        return api_version_urls
