from mayan.apps.documents.tests.base import GenericDocumentTestCase

from ..models import DuplicateBackendEntry

from .mixins import DuplicatedDocumentTaskTestMixin


class DuplicatedDocumentTaskTestCase(
    DuplicatedDocumentTaskTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._upload_test_document()
        self._upload_test_document()
        DuplicateBackendEntry.objects.all().delete()

    def test_task_duplicates_scan_all(self):
        self._clear_events()

        self._execute_task_duplicates_scan_all()

        self.assertEqual(
            list(
                DuplicateBackendEntry.objects.get_duplicates_of(
                    document=self.test_documents[0]
                )
            ), [self.test_documents[1]]
        )
        self.assertEqual(
            list(
                DuplicateBackendEntry.objects.get_duplicates_of(
                    document=self.test_documents[1]
                )
            ), [self.test_documents[0]]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_task_duplicates_scan_for(self):
        self._clear_events()

        self._execute_task_duplicates_scan_for()

        self.assertEqual(
            list(
                DuplicateBackendEntry.objects.get_duplicates_of(
                    document=self.test_documents[0]
                )
            ), [self.test_documents[1]]
        )
        self.assertEqual(
            list(
                DuplicateBackendEntry.objects.get_duplicates_of(
                    document=self.test_documents[1]
                )
            ), [self.test_documents[0]]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
