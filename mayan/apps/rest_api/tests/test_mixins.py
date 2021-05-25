from rest_framework import serializers, status

from ..api_view_mixins import ExternalObjectAPIViewMixin
from ..generics import RetrieveAPIView

from .base import BaseAPITestCase
from .mixins import APIUserTestCaseMixin, TestAPIViewTestCaseMixin


class ExternalObjectAPIViewMixinTestCase(
    APIUserTestCaseMixin, TestAPIViewTestCaseMixin, BaseAPITestCase
):
    auto_add_test_view = True
    auto_create_test_object = True
    auto_create_test_object_permission = True
    auto_login_user = False
    test_view_url = r'^test-view-url/(?P<test_object_id>\d+)/$'

    def _test_view_factory(self, test_object=None):
        class TestModelSerializer(serializers.Serializer):
            """Empty serializer."""

        class TestView(ExternalObjectAPIViewMixin, RetrieveAPIView):
            external_object_queryset = self.TestModel.objects.all()
            external_object_pk_url_kwarg = 'test_object_id'
            mayan_external_object_permissions = {
                'GET': (self.test_permission,)
            }
            serializer_class = TestModelSerializer

            def get_object(self):
                return None

        return TestView.as_view()

    def _request_test_api_view(self):
        return self.get(
            headers={
                'HTTP_AUTHORIZATION': 'Token {}'.format(
                    self._test_case_user_token
                )
            }, viewname='rest_api:{}'.format(self.test_view_name), kwargs={
                'test_object_id': self.test_object.pk,
            },
        )

    def test_mixin_using_token_authentication_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=self.test_permission
        )

        response = self._request_test_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mixin_using_token_authentication_no_permission(self):
        response = self._request_test_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
