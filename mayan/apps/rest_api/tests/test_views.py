import json
import unittest

from django.db import connection, models

from rest_framework import serializers, status
from rest_framework.reverse import reverse

from mayan.apps.testing.tests.base import GenericViewTestCase

from .. import generics

from .base import BaseAPITestCase
from .literals import TEST_OBJECT_LABEL, TEST_OBJECT_LABEL_EDITED
from .mixins import RESTAPIViewTestMixin


class RESTAPIViewTestCase(RESTAPIViewTestMixin, GenericViewTestCase):
    def test_browser_api_view(self):
        response = self._request_test_browser_api_view()
        self.assertEqual(response.status_code, 200)

    @unittest.skipIf(connection.vendor != 'sqlite', 'Skip for known Django issues #15802 and #27074')
    def test_redoc_ui_view(self):
        response = self._request_test_redoc_ui_view()
        self.assertEqual(response.status_code, 200)

    @unittest.skipIf(connection.vendor != 'sqlite', 'Skip for known Django issues #15802 and #27074')
    def test_swagger_ui_view(self):
        response = self._request_test_swagger_ui_view()
        self.assertEqual(response.status_code, 200)

    def test_swagger_no_ui_json_view(self):
        self.expected_content_types = ('application/json; charset=utf-8',)

        response = self._request_test_swagger_no_ui_json_view()
        self.assertEqual(response.status_code, 200)

    def test_swagger_no_ui_yaml_view(self):
        self.expected_content_types = ('application/yaml; charset=utf-8',)

        response = self._request_test_swagger_no_ui_yaml_view()
        self.assertEqual(response.status_code, 200)


class BatchAPIRequestViewTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()

        self._create_test_object(
            create_test_permission=True, fields={
                'label': models.CharField(max_length=32, unique=True)
            }, instance_kwargs={
                'label': TEST_OBJECT_LABEL
            }
        )

        class TestModelSerializer(serializers.ModelSerializer):
            class Meta:
                fields = ('id', 'label')
                model = self.TestModel

        def _test_view_factory():
            class TestView(generics.ListCreateAPIView):
                mayan_object_permissions = {
                    'GET': (self.test_permission,)
                }
                mayan_view_permissions = {
                    'POST': (self.test_permission,)
                }
                queryset = self.TestModel.objects.all()
                serializer_class = TestModelSerializer

            return TestView.as_view()

        self.add_test_view(
            test_object=self.test_object, test_view_factory=_test_view_factory,
            test_view_url=r'^test-view-url/$'
        )
        self._test_model_list_api_view_name = self._test_view_name

        def _test_view_factory():
            TestModel = self.TestModel

            class TestView(generics.RetrieveUpdateDestroyAPIView):
                lookup_url_kwarg = 'test_object_id'
                mayan_object_permissions = {
                    'DELETE': (self.test_permission,),
                    'GET': (self.test_permission,),
                    'PATCH': (self.test_permission,),
                    'PUT': (self.test_permission,)
                }
                queryset = TestModel.objects.all()
                serializer_class = TestModelSerializer

            return TestView.as_view()

        self.add_test_view(
            test_object=self.test_object, test_view_factory=_test_view_factory,
            test_view_url=r'^test-view-url/(?P<test_object_id>\d+)/$'
        )
        self._test_model_detail_api_view_name = self._test_view_name

    def _request_batch_api_request_api_view(self, requests):
        return self.post(
            viewname='rest_api:batchrequest-create', data={
                'requests': requests
            }
        )

    def test_create_batch_api_request(self):
        self.grant_permission(permission=self.test_permission)

        requests = [
            {
                'body': {'label': TEST_OBJECT_LABEL},
                'method': 'POST',
                'name': 'test_request',
                'url': reverse(
                    viewname='rest_api:{}'.format(
                        self._test_model_list_api_view_name
                    )
                )
            }
        ]

        self.test_object.delete()

        test_model_count = self.TestModel.objects.count()

        self._clear_events()

        response = self._request_batch_api_request_api_view(
            requests=json.dumps(obj=requests)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        self.assertEqual(
            response.data['results'][0]['status_code'], status.HTTP_201_CREATED
        )

        self.assertEqual(self.TestModel.objects.count(), test_model_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_delete_batch_api_request(self):
        self.grant_access(
            obj=self.test_object, permission=self.test_permission
        )

        requests = [
            {
                'method': 'DELETE',
                'name': 'test_request',
                'url': reverse(
                    viewname='rest_api:{}'.format(
                        self._test_model_detail_api_view_name
                    ), kwargs={'test_object_id': self.test_object.pk}
                )
            }
        ]

        test_model_count = self.TestModel.objects.count()

        self._clear_events()

        response = self._request_batch_api_request_api_view(
            requests=json.dumps(obj=requests)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        self.assertEqual(
            response.data['results'][0]['status_code'], status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(self.TestModel.objects.count(), test_model_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_edit_via_patch_batch_api_request(self):
        self.grant_access(
            obj=self.test_object, permission=self.test_permission
        )

        requests = [
            {
                'body': {'label': TEST_OBJECT_LABEL_EDITED},
                'method': 'PATCH',
                'name': 'test_request',
                'url': reverse(
                    viewname='rest_api:{}'.format(
                        self._test_model_detail_api_view_name
                    ), kwargs={'test_object_id': self.test_object.pk}
                )
            }
        ]

        test_model_label = self.test_object.label

        self._clear_events()

        response = self._request_batch_api_request_api_view(
            requests=json.dumps(obj=requests)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        self.assertEqual(
            response.data['results'][0]['status_code'], status.HTTP_200_OK
        )

        self.test_object.refresh_from_db()
        self.assertNotEqual(self.test_object.label, test_model_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_edit_via_put_batch_api_request(self):
        self.grant_access(
            obj=self.test_object, permission=self.test_permission
        )

        requests = [
            {
                'body': {'label': TEST_OBJECT_LABEL_EDITED},
                'method': 'PUT',
                'name': 'test_request',
                'url': reverse(
                    viewname='rest_api:{}'.format(
                        self._test_model_detail_api_view_name
                    ), kwargs={'test_object_id': self.test_object.pk}
                )
            }
        ]

        test_model_label = self.test_object.label

        self._clear_events()

        response = self._request_batch_api_request_api_view(
            requests=json.dumps(obj=requests)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        self.assertEqual(
            response.data['results'][0]['status_code'], status.HTTP_200_OK
        )

        self.test_object.refresh_from_db()
        self.assertNotEqual(self.test_object.label, test_model_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_list_get_batch_api_request(self):
        self.grant_access(
            obj=self.test_object, permission=self.test_permission
        )

        requests = [
            {
                'name': 'test_request',
                'url': reverse(
                    viewname='rest_api:{}'.format(
                        self._test_model_list_api_view_name
                    )
                )
            }
        ]

        self._clear_events()

        response = self._request_batch_api_request_api_view(
            requests=json.dumps(obj=requests)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        self.assertEqual(
            response.data['results'][0]['status_code'], status.HTTP_200_OK
        )
        self.assertEqual(response.data['results'][0]['data']['count'], 1)
        self.assertEqual(
            response.data['results'][0]['data']['results'][0]['id'],
            self.test_object.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_mass_edit_get_batch_api_request(self):
        self.grant_access(
            obj=self.test_object, permission=self.test_permission
        )

        requests = [
            {
                'name': 'test_object_list',
                'url': reverse(
                    viewname='rest_api:{}'.format(
                        self._test_model_list_api_view_name
                    )
                )
            },
            {
                'body': {'label': TEST_OBJECT_LABEL_EDITED},
                'iterables': ['test_object_list.data.results'],
                'method': 'PATCH',
                'name': 'test_object_edit',
                'url': '{}{{{{ iterables.0.id }}}}/'.format(
                    reverse(
                        viewname='rest_api:{}'.format(
                            self._test_model_list_api_view_name
                        )
                    )
                )
            }
        ]

        test_model_label = self.test_object.label

        self._clear_events()

        response = self._request_batch_api_request_api_view(
            requests=json.dumps(obj=requests)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        self.assertEqual(
            response.data['results'][0]['status_code'], status.HTTP_200_OK
        )
        self.assertEqual(response.data['results'][0]['data']['count'], 1)
        self.assertEqual(
            response.data['results'][0]['data']['results'][0]['id'],
            self.test_object.pk
        )

        self.assertEqual(
            response.data['results'][1]['status_code'], status.HTTP_200_OK
        )

        self.test_object.refresh_from_db()
        self.assertNotEqual(self.test_object.label, test_model_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
