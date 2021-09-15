from django.db import models

from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import QuerysetParametersSerializer


class QuerysetParametersSerializerTestCase(BaseTestCase):
    def _assertQuerysetEqual(self):
        rebuilt_items = list(map(repr, self.queryset_rebuilt))

        self.assertQuerysetEqual(
            qs=self.queryset_original, values=rebuilt_items
        )

    def test_without_kwargs(self):
        self._create_test_object()

        self.queryset_original = self.TestModel.objects.all()

        decomposed_queryset = QuerysetParametersSerializer.decompose(
            _model=self.TestModel, _method_name='all'
        )

        self.queryset_rebuilt = QuerysetParametersSerializer.rebuild(
            decomposed_queryset=decomposed_queryset
        )

        self._assertQuerysetEqual()

    def test_foreign_key_model(self):
        self.TestModelParent = self._create_test_model(
            model_name='TestModelParent'
        )
        self.TestModelChild = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelParent',
                )
            }, model_name='TestModelChild'
        )

        parent = self.TestModelParent.objects.create()
        self.TestModelChild.objects.create(parent=parent)

        self.queryset_original = self.TestModelChild.objects.all()

        decomposed_queryset = QuerysetParametersSerializer.decompose(
            _model=self.TestModelChild, _method_name='filter', parent=parent
        )

        self.queryset_rebuilt = QuerysetParametersSerializer.rebuild(
            decomposed_queryset=decomposed_queryset
        )

        self._assertQuerysetEqual()

    def test_foreign_key_model_id_query(self):
        self.TestModelParent = self._create_test_model(
            model_name='TestModelParent'
        )
        self.TestModelChild = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelParent',
                )
            }, model_name='TestModelChild'
        )

        parent = self.TestModelParent.objects.create()
        self.TestModelChild.objects.create(parent_id=parent.pk)

        self.queryset_original = self.TestModelChild.objects.all()

        decomposed_queryset = QuerysetParametersSerializer.decompose(
            _model=self.TestModelChild, _method_name='filter',
            parent_id=parent.pk
        )

        self.queryset_rebuilt = QuerysetParametersSerializer.rebuild(
            decomposed_queryset=decomposed_queryset
        )

        self._assertQuerysetEqual()
