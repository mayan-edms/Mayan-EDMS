from django.db import models

from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import QuerysetParametersSerializer


class QuerysetParametersSerializerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.TestModelParent = self._create_test_model(
            model_name='TestModelParent'
        )
        self.TestModelChild = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelParent'
                )
            }, model_name='TestModelChild'
        )

        self._test_object_parent = self.TestModelParent.objects.create()
        self.TestModelChild.objects.create(parent_id=self._test_object_parent.pk)

    def _assertQuerysetEqual(self):
        rebuilt_items = list(map(repr, self.queryset_rebuilt))

        self.assertQuerysetEqual(
            qs=self.queryset_original, values=rebuilt_items
        )

    def test_without_kwargs(self):
        self.queryset_original = self.TestModelParent.objects.all()

        decomposed_queryset = QuerysetParametersSerializer.decompose(
            _model=self.TestModelParent, _method_name='all'
        )

        self.queryset_rebuilt = QuerysetParametersSerializer.rebuild(
            decomposed_queryset=decomposed_queryset
        )

        self._assertQuerysetEqual()

    def test_foreign_key_model(self):
        self.queryset_original = self.TestModelChild.objects.all()

        decomposed_queryset = QuerysetParametersSerializer.decompose(
            _model=self.TestModelChild, _method_name='filter',
            parent=self._test_object_parent
        )

        self.queryset_rebuilt = QuerysetParametersSerializer.rebuild(
            decomposed_queryset=decomposed_queryset
        )

        self._assertQuerysetEqual()

    def test_foreign_key_model_id_query(self):
        self.queryset_original = self.TestModelChild.objects.all()

        decomposed_queryset = QuerysetParametersSerializer.decompose(
            _model=self.TestModelChild, _method_name='filter',
            parent_id=self._test_object_parent.pk
        )

        self.queryset_rebuilt = QuerysetParametersSerializer.rebuild(
            decomposed_queryset=decomposed_queryset
        )

        self._assertQuerysetEqual()
