from mayan.apps.dynamic_search.tests.mixins import SearchTestMixin

from ..permissions import permission_document_version_view
from ..search import document_version_page_search, document_version_search

from .base import GenericDocumentViewTestCase
from .literals import TEST_DOCUMENT_VERSION_COMMENT


class DocumentVersionSearchTestCase(
    SearchTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def _do_test_search(self, query):
        terms = str(tuple((query.values()))[0]).strip()
        self.assertTrue(terms is not None)
        self.assertTrue(terms != '')

        return self.search_backend.search(
            search_model=document_version_search, query=query,
            user=self._test_case_user
        )

    def setUp(self):
        super().setUp()
        self._upload_test_document(
            document_version_attributes={
                'comment': TEST_DOCUMENT_VERSION_COMMENT
            }
        )

    def test_document_version_search_by_comment_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'comment': self.test_document_version.comment
            }
        )
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_by_comment_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'comment': self.test_document_version.comment
            }
        )
        self.assertTrue(self.test_document_version in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_search_by_comment_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'comment': self.test_document_version.comment
            }
        )
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_by_document_description_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_by_document_description_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_version in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_search_by_document_description_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_by_document_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_by_document_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_version in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_search_by_document_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_by_document_uuid_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_by_document_uuid_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_version in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_search_by_document_uuid_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_by_document_type_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_search_by_document_type_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_version in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_search_by_document_type_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_version not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionPageSearchTestCase(
    SearchTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def _do_test_search(self, query):
        terms = str(tuple((query.values()))[0]).strip()
        self.assertTrue(terms is not None)
        self.assertTrue(terms != '')

        return self.search_backend.search(
            search_model=document_version_page_search, query=query,
            user=self._test_case_user
        )

    def setUp(self):
        super().setUp()
        self._upload_test_document(
            document_version_attributes={
                'comment': TEST_DOCUMENT_VERSION_COMMENT
            }
        )

    def test_document_version_page_search_by_document_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_search_by_document_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_version_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_page_search_by_document_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_search_by_document_description_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_search_by_document_description_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_version_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_page_search_by_document_description_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_search_by_document_uuid_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_search_by_document_uuid_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_version_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_page_search_by_document_uuid_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_search_by_document_type_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_search_by_document_type_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_version_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_page_search_by_document_type_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_search_by_document_version_comment_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__comment': self.test_document_version.comment
            }
        )
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_search_by_document_version_comment_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__comment': self.test_document_version.comment
            }
        )
        self.assertTrue(self.test_document_version_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_page_search_by_document_version_comment_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_version__comment': self.test_document_version.comment
            }
        )
        self.assertTrue(self.test_document_version_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
