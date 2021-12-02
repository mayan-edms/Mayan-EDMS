from mayan.apps.rest_api.tests.base import BaseAPITestCase
from mayan.apps.testing.tests.base import (
    BaseTestCase, BaseTransactionTestCase, GenericViewTestCase,
    GenericTransactionViewTestCase
)


from .mixins.document_mixins import DocumentTestMixin


class GenericDocumentTestCase(DocumentTestMixin, BaseTestCase):
    """Base test case when testing document models or classes."""


class GenericDocumentAPIViewTestCase(DocumentTestMixin, BaseAPITestCase):
    """Base test case when testing document API views."""


class GenericDocumentViewTestCase(DocumentTestMixin, GenericViewTestCase):
    """Base test case when testing document views."""


class GenericTransactionDocumentTestCase(
    DocumentTestMixin, BaseTransactionTestCase
):
    """
    Base test case when testing document models or classes with transactions.
    """


class GenericTransactionDocumentViewTestCase(
    DocumentTestMixin, GenericTransactionViewTestCase
):
    """Base test case when testing document views with transactions."""
