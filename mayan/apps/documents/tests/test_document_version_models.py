from mayan.apps.messaging.events import event_message_created
from mayan.apps.messaging.models import Message
from mayan.apps.storage.events import event_download_file_created
from mayan.apps.storage.models import DownloadFile

from ..document_file_actions import (
    DocumentFileActionAppendNewPages, DocumentFileActionNothing,
    DocumentFileActionUseNewPages
)
from ..events import event_document_version_exported
from ..literals import DOCUMENT_VERSION_EXPORT_MESSAGE_SUBJECT

from .base import GenericDocumentTestCase
from .mixins.document_file_mixins import DocumentFileTestMixin


class DocumentVersionTestCase(
    DocumentFileTestMixin, GenericDocumentTestCase
):
    def test_version_new_file_new_pages(self):
        test_document_version_page_content_objects = self._test_document_version.page_content_objects

        self.assertEqual(self._test_document.versions.count(), 1)

        self._upload_test_document_file(
            action=DocumentFileActionUseNewPages.backend_id
        )

        self.assertEqual(self._test_document.versions.count(), 2)

        self.assertNotEqual(
            self._test_document_version.page_content_objects,
            test_document_version_page_content_objects
        )
        self.assertEqual(
            self._test_document_version.page_content_objects,
            list(self._test_document.file_latest.pages.all())
        )

    def test_version_new_version_keep_pages(self):
        test_document_version_page_content_objects = self._test_document_version.page_content_objects

        self.assertEqual(self._test_document.versions.count(), 1)

        self._upload_test_document_file(
            action=DocumentFileActionNothing.backend_id
        )

        self.assertEqual(self._test_document.versions.count(), 1)

        self.assertEqual(
            self._test_document_version.page_content_objects,
            test_document_version_page_content_objects
        )
        self.assertNotEqual(
            self._test_document_version.page_content_objects,
            list(self._test_document.file_latest.pages.all())
        )

    def test_version_new_file_append_pages(self):
        test_document_version_page_content_objects = self._test_document_version.page_content_objects

        self.assertEqual(self._test_document.versions.count(), 1)
        self.assertEqual(self._test_document.files.count(), 1)

        self._upload_test_document_file(
            action=DocumentFileActionAppendNewPages.backend_id
        )

        self.assertEqual(self._test_document.files.count(), 2)
        self.assertEqual(self._test_document.versions.count(), 2)

        test_document_version_expected_page_content_objects = list(
            self._test_document.files.first().pages.all()
        )
        test_document_version_expected_page_content_objects.extend(
            list(
                self._test_document.files.last().pages.all()
            )
        )

        self.assertNotEqual(
            self._test_document_version.page_content_objects,
            test_document_version_page_content_objects
        )
        self.assertEqual(
            self._test_document_version.page_content_objects,
            test_document_version_expected_page_content_objects
        )

    def test_method_get_absolute_url(self):
        self.assertTrue(self._test_document.version_active.get_absolute_url())


class DocumentVersionExportModelTestCase(GenericDocumentTestCase):
    def test_document_version_export(self):
        self._create_test_user()

        download_file_count = DownloadFile.objects.count()

        self._clear_events()

        self._test_user.locale_profile.language = 'es'

        self._test_document_version.export_to_download_file(
            user=self._test_user
        )

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count + 1
        )

        test_download_file = DownloadFile.objects.first()
        test_message = Message.objects.first()

        self.assertNotEqual(
            test_message.subject, DOCUMENT_VERSION_EXPORT_MESSAGE_SUBJECT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 3)

        self.assertEqual(events[0].action_object, self._test_document_version)
        self.assertEqual(events[0].actor, self._test_user)
        self.assertEqual(events[0].target, test_download_file)
        self.assertEqual(events[0].verb, event_download_file_created.id)

        self.assertEqual(events[1].action_object, test_download_file)
        self.assertEqual(events[1].actor, self._test_user)
        self.assertEqual(events[1].target, self._test_document_version)
        self.assertEqual(events[1].verb, event_document_version_exported.id)

        self.assertEqual(events[2].action_object, None)
        self.assertEqual(events[2].actor, test_message)
        self.assertEqual(events[2].target, test_message)
        self.assertEqual(events[2].verb, event_message_created.id)

    def test_document_version_empty_content_type_export(self):
        self._create_test_user()

        download_file_count = DownloadFile.objects.count()
        self._test_document_file.delete()

        self._clear_events()

        self._test_user.locale_profile.language = 'es'

        self._test_document_version.export_to_download_file(
            user=self._test_user
        )

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count + 1
        )

        test_download_file = DownloadFile.objects.first()
        test_message = Message.objects.first()

        self.assertNotEqual(
            test_message.subject, DOCUMENT_VERSION_EXPORT_MESSAGE_SUBJECT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 3)

        self.assertEqual(events[0].action_object, self._test_document_version)
        self.assertEqual(events[0].actor, self._test_user)
        self.assertEqual(events[0].target, test_download_file)
        self.assertEqual(events[0].verb, event_download_file_created.id)

        self.assertEqual(events[1].action_object, test_download_file)
        self.assertEqual(events[1].actor, self._test_user)
        self.assertEqual(events[1].target, self._test_document_version)
        self.assertEqual(events[1].verb, event_document_version_exported.id)

        self.assertEqual(events[2].action_object, None)
        self.assertEqual(events[2].actor, test_message)
        self.assertEqual(events[2].target, test_message)
        self.assertEqual(events[2].verb, event_message_created.id)
