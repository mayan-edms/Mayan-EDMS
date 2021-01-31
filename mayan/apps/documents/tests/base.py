from mayan.apps.testing.tests.base import (
    BaseTestCase, BaseTransactionTestCase, GenericViewTestCase,
    GenericTransactionViewTestCase
)

from .mixins.document_mixins import DocumentTestMixin


class GenericDocumentTestCase(DocumentTestMixin, BaseTestCase):
    """Base test case when testing models or classes"""


class GenericTransactionDocumentTestCase(
    DocumentTestMixin, BaseTransactionTestCase
):
    """Base test case when testing models or classes with transactions"""


class GenericDocumentViewTestCase(DocumentTestMixin, GenericViewTestCase):
    """Base test case when testing views"""


class GenericTransactionDocumentViewTestCase(
    DocumentTestMixin, GenericTransactionViewTestCase
):
    """Base test case when testing views with transactions"""
