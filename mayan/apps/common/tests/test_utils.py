from django.db import models

from mayan.apps.testing.tests.base import BaseTestCase

from ..utils import ResolverPipelineModelAttribute


class ResolverRelatedManagerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.TestModelAttribute = self._create_test_model(
            fields={
                'label': models.CharField(
                    max_length=1
                )
            }, model_name='TestModelAttribute'
        )
        self.TestModelGrandParent = self._create_test_model(
            model_name='TestModelGrandParent'
        )
        self.TestModelParent = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelGrandParent',
                )
            }, model_name='TestModelParent'
        )
        self.TestModelGrandChild = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelParent',
                ),
                'attributes': models.ManyToManyField(
                    related_name='children', to='TestModelAttribute',
                )
            }, model_name='TestModelGrandChild'
        )

        self._test_object_grandparent = self.TestModelGrandParent.objects.create()
        self._test_object_parent = self.TestModelParent.objects.create(
            parent=self._test_object_grandparent
        )
        self._test_object_grandchild = self.TestModelGrandChild.objects.create(
            parent=self._test_object_parent
        )
        self._test_object_attribute = self.TestModelAttribute.objects.create(
            label='test attribute object'
        )
        self._test_object_grandchild.attributes.add(self._test_object_attribute)

    def test_many_to_many(self):
        result = ResolverPipelineModelAttribute.resolve(
            attribute='attributes',
            obj=self._test_object_grandchild,
        )

        self.assertEqual(result.count(), 1)
        self.assertEqual(result[0], self._test_object_attribute)

    def test_many_to_many_field(self):
        result = ResolverPipelineModelAttribute.resolve(
            attribute='attributes__label',
            obj=self._test_object_grandchild,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self._test_object_attribute.label)

    def test_multiple_level_reverse_relation(self):
        result = ResolverPipelineModelAttribute.resolve(
            attribute='parent__parent', obj=self._test_object_grandchild,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].count(), 1)
        self.assertEqual(result[0][0], self._test_object_grandparent)

    def test_single_level_reverse_many_to_many(self):
        result = ResolverPipelineModelAttribute.resolve(
            attribute='children',
            obj=self._test_object_attribute,
        )

        self.assertEqual(result.count(), 1)
        self.assertEqual(result[0], self._test_object_grandchild)

    def test_multiple_level_reverse_relation_from_many_to_many_field(self):
        result = ResolverPipelineModelAttribute.resolve(
            attribute='children__parent__parent',
            obj=self._test_object_attribute,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0].count(), 1)
        self.assertEqual(result[0][0][0], self._test_object_grandparent)

    def test_multiple_level_relation(self):
        result = ResolverPipelineModelAttribute.resolve(
            attribute='children__children',
            obj=self._test_object_grandparent,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].count(), 1)
        self.assertEqual(result[0][0], self._test_object_grandchild)

    def test_multiple_level_relation_to_many_to_many(self):
        result = ResolverPipelineModelAttribute.resolve(
            attribute='children__children__attributes',
            obj=self._test_object_grandparent,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0].count(), 1)
        self.assertEqual(result[0][0][0], self._test_object_attribute)
