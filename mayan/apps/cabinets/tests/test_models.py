from django.core.exceptions import ValidationError

from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.tests.tests.base import BaseTestCase

from ..models import Cabinet

from .literals import TEST_CABINET_LABEL
from .mixins import CabinetTestMixin


class CabinetTestCase(CabinetTestMixin, BaseTestCase):
    def test_cabinet_creation(self):
        self._create_test_cabinet()

        self.assertEqual(Cabinet.objects.all().count(), 1)
        self.assertQuerysetEqual(
            Cabinet.objects.all(), (repr(self.test_cabinet),)
        )

    def test_cabinet_duplicate_creation(self):
        self._create_test_cabinet()

        with self.assertRaises(expected_exception=ValidationError):
            cabinet_2 = Cabinet(label=TEST_CABINET_LABEL)
            cabinet_2.validate_unique()
            cabinet_2.save()

        self.assertEqual(Cabinet.objects.all().count(), 1)
        self.assertQuerysetEqual(
            Cabinet.objects.all(), (repr(self.test_cabinet),)
        )

    def test_inner_cabinet_creation(self):
        self._create_test_cabinet()

        inner_cabinet = Cabinet.objects.create(
            parent=self.test_cabinet, label=TEST_CABINET_LABEL
        )

        self.assertEqual(Cabinet.objects.all().count(), 2)
        self.assertQuerysetEqual(
            Cabinet.objects.all(),
            map(repr, (self.test_cabinet, inner_cabinet))
        )

    def test_method_get_absolute_url(self):
        self._create_test_cabinet()

        self.assertTrue(self.test_cabinet.get_absolute_url())


class CabinetDocumentTestCase(
    CabinetTestMixin, DocumentTestMixin, BaseTestCase
):
    def setUp(self):
        super(CabinetDocumentTestCase, self).setUp()
        self._create_test_cabinet()

    def test_addition_of_documents(self):
        self.test_cabinet.documents.add(self.test_document)

        self.assertEqual(self.test_cabinet.documents.count(), 1)
        self.assertQuerysetEqual(
            self.test_cabinet.documents.all(), (repr(self.test_document),)
        )

    def test_addition_and_deletion_of_documents(self):
        self.test_cabinet.documents.add(self.test_document)

        self.assertEqual(self.test_cabinet.documents.count(), 1)
        self.assertQuerysetEqual(
            self.test_cabinet.documents.all(), (repr(self.test_document),)
        )

        self.test_cabinet.documents.remove(self.test_document)

        self.assertEqual(self.test_cabinet.documents.count(), 0)
        self.assertQuerysetEqual(self.test_cabinet.documents.all(), ())
