from mayan.apps.dynamic_search.tests.mixins import SearchTestMixin

from ..permissions import permission_document_view
from ..search import search_model_document

from .base import GenericDocumentViewTestCase


class DocumentSearchTestCase(SearchTestMixin, GenericDocumentViewTestCase):
    auto_upload_test_document = False

    def _do_test_search(self, query):
        terms = str(tuple(query.values())[0]).strip()
        self.assertTrue(terms is not None)
        self.assertTrue(terms != '')

        return self.search_backend.search(
            search_model=search_model_document, query=query,
            user=self._test_case_user
        )

    def setUp(self):
        super().setUp()
        self._upload_test_document()

    def test_search_model_document_by_datetime_created_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={
                'datetime_created': self._test_document.datetime_created.isoformat()
            }
        )
        self.assertFalse(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_datetime_created_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'datetime_created': self._test_document.datetime_created.isoformat()
            }
        )
        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_by_datetime_created_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={
                'datetime_created': self._test_document.datetime_created.isoformat()
            }
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_document_file_checksum_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'files__checksum': self._test_document_file.checksum}
        )
        self.assertFalse(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_document_file_checksum_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'files__checksum': self._test_document_file.checksum}
        )
        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_by_document_file_checksum_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={'files__checksum': self._test_document_file.checksum}
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_document_file_filename_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'files__filename': self._test_document_file.filename}
        )
        self.assertFalse(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_document_file_filename_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'files__filename': self._test_document_file.filename}
        )
        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_by_document_file_filename_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={'files__filename': self._test_document_file.filename}
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_document_file_mime_type_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'files__mimetype': self._test_document_file.mimetype}
        )
        self.assertFalse(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_document_file_mime_type_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'files__mimetype': self._test_document_file.mimetype}
        )
        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_by_document_file_mime_type_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={'files__mimetype': self._test_document_file.mimetype}
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_description_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'description': self._test_document.description}
        )
        self.assertFalse(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_description_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'description': self._test_document.description}
        )
        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_by_description_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={'description': self._test_document.description}
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_label_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'label': self._test_document.label}
        )
        self.assertFalse(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_label_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'label': self._test_document.label}
        )
        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_by_label_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={'label': self._test_document.label}
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_uuid_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search(
            query={'uuid': self._test_document.uuid}
        )
        self.assertFalse(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_by_uuid_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search(
            query={'uuid': self._test_document.uuid}
        )
        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_by_uuid_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search(
            query={'uuid': self._test_document.uuid}
        )
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
