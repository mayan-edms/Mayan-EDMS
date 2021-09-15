from django.db import models

from mayan.apps.testing.tests.base import GenericViewTestCase

from ..classes import ModelCopy
from ..permissions import permission_object_copy

from .literals import TEST_OBJECT_LABEL
from .mixins import CommonViewTestMixin, ObjectCopyViewTestMixin


class CommonViewTestCase(CommonViewTestMixin, GenericViewTestCase):
    def test_about_view(self):
        response = self._request_about_view()
        self.assertContains(response=response, text='About', status_code=200)


class ObjectCopyViewTestCase(ObjectCopyViewTestMixin, GenericViewTestCase):
    auto_create_test_object = True
    auto_create_test_object_fields = {
        'label': models.CharField(max_length=32, unique=True)
    }
    auto_create_test_object_instance_kwargs = {
        'label': TEST_OBJECT_LABEL
    }

    def setUp(self):
        super().setUp()
        ModelCopy(model=self.TestModel, register_permission=True).add_fields(
            field_names=('label',)
        )

    def test_object_copy_view_no_permission(self):
        test_object_count = self.TestModel.objects.count()
        response = self._request_object_copy_view()
        self.assertTrue(response.status_code, 404)

        queryset = self.TestModel.objects.all()
        self.assertEqual(queryset.count(), test_object_count)
        test_object_labels = queryset.values_list('label', flat=True)

        self.assertTrue(
            TEST_OBJECT_LABEL in test_object_labels
        )
        self.assertFalse(
            '{}_1'.format(TEST_OBJECT_LABEL) in test_object_labels
        )

    def test_object_copy_view_with_access(self):
        self.grant_access(obj=self.test_object, permission=permission_object_copy)

        test_object_count = self.TestModel.objects.count()
        response = self._request_object_copy_view()
        self.assertTrue(response.status_code, 302)

        queryset = self.TestModel.objects.all()
        self.assertEqual(queryset.count(), test_object_count + 1)
        test_object_labels = queryset.values_list('label', flat=True)

        self.assertTrue(
            TEST_OBJECT_LABEL in test_object_labels
        )
        self.assertTrue(
            '{}_1'.format(TEST_OBJECT_LABEL) in test_object_labels
        )
