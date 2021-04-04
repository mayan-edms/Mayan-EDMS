from django.test import override_settings
from django.utils.encoding import force_text

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import document_search
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.storage.utils import fs_cleanup, mkdtemp
from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import SearchBackend
from ..settings import setting_backend_arguments


@override_settings(SEARCH_BACKEND='mayan.apps.dynamic_search.backends.django.DjangoSearchBackend')
class DjangoSearchBackendDocumentSearchTestCase(
    DocumentTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self.search_backend = SearchBackend.get_instance()

    def test_simple_search(self):
        self._upload_test_document(label='first_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'q': 'first'}, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_advanced_search_after_related_name_change(self):
        # Test versions__filename
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': self.test_document.label},
            user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        # Test versions__mimetype
        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={
                'versions__mimetype': self.test_document.file_latest.mimetype
            }, user=self._test_case_user
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
            query_string={'q': 'OR first'}, user=self._test_case_user
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
            query_string={'q': 'first OR second'}, user=self._test_case_user
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
            query_string={'label': 'first OR second'},
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
            query_string={'q': 'non_valid second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'q': 'second non_valid'},
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
            query_string={'q': '-non_valid second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-second -Mayan'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-second OR -Mayan'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-non_valid -second'},
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
            query_string={'label': '-second-document'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-"second-document"'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_search_field_transformation_functions(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'uuid': force_text(s=self.test_document.uuid)},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)


@override_settings(SEARCH_BACKEND='mayan.apps.dynamic_search.backends.whoosh.WhooshSearchBackend')
class WhooshSearchBackendDocumentSearchTestCase(
    DocumentTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        self.old_value = setting_backend_arguments.value
        super().setUp()
        setting_backend_arguments.set(
            value={'index_path': mkdtemp()}
        )
        self.search_backend = SearchBackend.get_instance()

    def tearDown(self):
        fs_cleanup(
            filename=setting_backend_arguments.value['index_path']
        )
        setting_backend_arguments.set(value=self.old_value)
        super().tearDown()

    def test_simple_search(self):
        self._upload_test_document(label='first_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'q': 'first*'}, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_advanced_search_related(self):
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={
                'files__mimetype': self.test_document.file_latest.mimetype
            }, user=self._test_case_user
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
            query_string={'q': 'OR first*'}, user=self._test_case_user
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
            query_string={'q': 'first* OR second*'}, user=self._test_case_user
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
            query_string={'label': 'first* OR second*'},
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
            query_string={'q': 'non_valid AND second*'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'q': 'second* AND non_valid'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_search_field_transformation_functions(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'uuid': force_text(s=self.test_document.uuid)},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
