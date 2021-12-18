from mayan.apps.dynamic_search.tests.mixins import SearchTestMixin

from ..permissions import permission_document_file_view
from ..search import document_file_page_search, document_file_search

from .base import GenericDocumentViewTestCase
from .literals import TEST_DOCUMENT_FILE_COMMENT


class DocumentFileSearchTestCase(
    SearchTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def _do_test_search(self, query):
        terms = str(tuple((query.values()))[0]).strip()
        self.assertTrue(terms is not None)
        self.assertTrue(terms != '')

        return self.search_backend.search(
            search_model=document_file_search, query=query,
            user=self._test_case_user
        )

    def setUp(self):
        super().setUp()
        self._upload_test_document(
            document_file_attributes={'comment': TEST_DOCUMENT_FILE_COMMENT}
        )

    def test_document_file_search_by_checksum_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'checksum': self.test_document_file.checksum
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_checksum_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'checksum': self.test_document_file.checksum
            }
        )
        self.assertTrue(self.test_document_file in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_search_by_checksum_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'checksum': self.test_document_file.checksum
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_comment_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'comment': self.test_document_file.comment
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_comment_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'comment': self.test_document_file.comment
            }
        )
        self.assertTrue(self.test_document_file in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_search_by_comment_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'comment': self.test_document_file.comment
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_filename_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'filename': self.test_document_file.filename
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_filename_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'filename': self.test_document_file.filename
            }
        )
        self.assertTrue(self.test_document_file in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_search_by_filename_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'filename': self.test_document_file.filename
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_mime_type_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'mimetype': self.test_document_file.mimetype
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_mime_type_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'mimetype': self.test_document_file.mimetype
            }
        )
        self.assertTrue(self.test_document_file in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_search_by_mime_type_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'mimetype': self.test_document_file.mimetype
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_document_description_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_document_description_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_file in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_search_by_document_description_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_document_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_document_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_file in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_search_by_document_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_document_uuid_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_document_uuid_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_file in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_search_by_document_uuid_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_document_type_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_search_by_document_type_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_file in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_search_by_document_type_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_file not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentFilePageSearchTestCase(
    SearchTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def _do_test_search(self, query):
        terms = str(tuple((query.values()))[0]).strip()
        self.assertTrue(terms is not None)
        self.assertTrue(terms != '')

        return self.search_backend.search(
            search_model=document_file_page_search, query=query,
            user=self._test_case_user
        )

    def setUp(self):
        super().setUp()
        self._upload_test_document()

    def test_document_file_page_search_by_document_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_file_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_page_search_by_document_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__label': self.test_document.label
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_description_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_description_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_file_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_page_search_by_document_description_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__description': self.test_document.description
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_file_checksum_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__checksum': self.test_document_file.checksum
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_file_checksum_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__checksum': self.test_document_file.checksum
            }
        )
        self.assertTrue(self.test_document_file_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_page_search_by_document_file_checksum_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__checksum': self.test_document_file.checksum
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_file_mime_type_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__mimetype': self.test_document_file.mimetype
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_file_mime_type_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__mimetype': self.test_document_file.mimetype
            }
        )
        self.assertTrue(self.test_document_file_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_page_search_by_document_file_mime_type_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__mimetype': self.test_document_file.mimetype
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_uuid_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_uuid_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_file_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_page_search_by_document_uuid_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__uuid': self.test_document.uuid
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_type_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_search_by_document_type_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_file_page in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_page_search_by_document_type_label_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self.test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'document_file__document__document_type__label': self.test_document_type.label
            }
        )
        self.assertTrue(self.test_document_file_page not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
