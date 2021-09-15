from django.test import override_settings
from django.utils.encoding import force_text

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import document_search
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.tags.tests.mixins import TagTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import SearchTestMixin


class CommonBackendFunctionalityTestCaseMixin(TagTestMixin):
    def test_advanced_search_related(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={
                'files__mimetype': self.test_document.file_latest.mimetype
            }, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_related_many_to_many_field_with_multiple_values(self):
        self._create_test_document_stub()

        self._create_test_tag()
        self._create_test_tag()

        self.test_tags[0].documents.add(self.test_document)
        self.test_tags[1].documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        query = {
            'tags__label': self.test_tags[0].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        query = {
            'tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_related_many_to_many_field_after_remove_values(self):
        self._create_test_document_stub()

        self._create_test_tag()
        self._create_test_tag()

        self.test_tags[0].documents.add(self.test_document)
        self.test_tags[1].documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        query = {
            'tags__label': self.test_tags[0].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        query = {
            'tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        self.test_tags[1].documents.remove(self.test_document)

        query = {
            'tags__label': self.test_tags[1].label
        }
        queryset = self.search_backend.search(
            search_model=document_search, query=query,
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)
        self.assertTrue(self.test_document not in queryset)

    def test_search_field_transformation_functions(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'uuid': force_text(s=self.test_document.uuid)},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

    def test_undefined_search_field(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        queryset = self.search_backend.search(
            search_model=document_search,
            query={'invalid': 'invalid'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)


@override_settings(SEARCH_BACKEND='mayan.apps.dynamic_search.backends.django.DjangoSearchBackend')
class DjangoSearchBackendDocumentSearchTestCase(
    CommonBackendFunctionalityTestCaseMixin, DocumentTestMixin,
    SearchTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def test_meta_only(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'OR first'}, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)

    def test_simple_or_search(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        self._upload_test_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )
        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'first OR second'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_advanced_or_search(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )

        self._upload_test_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': 'first OR second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_simple_and_search(self):
        self._upload_test_document(label='second_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'non_valid second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'second non_valid'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_simple_negated_search(self):
        self._upload_test_document(label='second_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': '-non_valid second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-second -Mayan'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-second OR -Mayan'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-non_valid -second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_search_with_dashed_content(self):
        self._upload_test_document(label='second-document')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-second-document'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': '-"second-document"'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)


@override_settings(SEARCH_BACKEND='mayan.apps.dynamic_search.backends.whoosh.WhooshSearchBackend')
class WhooshSearchBackendDocumentSearchTestCase(
    CommonBackendFunctionalityTestCaseMixin, DocumentTestMixin,
    SearchTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def test_simple_search(self):
        self._upload_test_document(label='first_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'first*'}, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_meta_only(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'OR first*'}, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)

    def test_simple_or_search(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        self._upload_test_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )
        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'first* OR second*'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_advanced_or_search(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )

        self._upload_test_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'label': 'first* OR second*'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_simple_and_search(self):
        self._upload_test_document(label='second_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'non_valid AND second*'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query={'q': 'second* AND non_valid'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)
