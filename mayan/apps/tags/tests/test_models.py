from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import TagTestMixin


class TagDocumentTestCase(DocumentTestMixin, TagTestMixin, BaseTestCase):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_method_document_attach(self):
        self._create_test_tag()

        self._test_tag.attach_to(document=self._test_document)

        self.assertTrue(self._test_document in self._test_tag.documents.all())

    def test_method_document_count(self):
        self._create_test_tag(add_test_document=True)

        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self.assertEqual(
            self._test_tag.get_document_count(user=self._test_case_user),
            len(self._test_documents)
        )

    def test_method_document_count_with_trashed_document(self):
        self._create_test_tag(add_test_document=True)
        self._test_document.delete()

        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self.assertEqual(
            self._test_tag.get_document_count(user=self._test_case_user),
            len(self._test_documents) - 1
        )

    def test_method_document_remove(self):
        self._create_test_tag(add_test_document=True)

        self._test_tag.remove_from(document=self._test_document)

        self.assertTrue(
            self._test_document not in self._test_tag.documents.all()
        )

    def test_method_get_absolute_url(self):
        self._create_test_tag()

        self.assertTrue(self._test_tag.get_absolute_url())
