from rest_framework import status

from mayan.apps.documents.events import (
    event_document_created, event_document_file_created,
    event_document_file_edited, event_document_version_created,
    event_document_version_page_created
)
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.literals import TEST_FILE_COMPRESSED_PATH
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..source_backends.literals import (
    SOURCE_UNCOMPRESS_CHOICE_ASK, SOURCE_UNCOMPRESS_CHOICE_NEVER
)

from .mixins.web_form_source_mixins import (
    WebFormSourceBackendAPITestMixin, WebFormSourceBackendTestMixin
)


class WebFormSourceBackendAPITestCase(
    WebFormSourceBackendTestMixin, WebFormSourceBackendAPITestMixin,
    DocumentTestMixin, BaseAPITestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def test_web_form_file_upload_api_view_with_no_permission(self):
        self._create_test_web_form_source(
            extra_data={'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER}
        )

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_web_form_file_upload_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.objects.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_form_file_upload_api_view_with_document_type_access(self):
        self._create_test_web_form_source(
            extra_data={'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER}
        )

        self.grant_access(
            obj=self._test_document_type, permission=permission_document_create
        )

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_web_form_file_upload_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.objects.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_form_file_upload_api_view_with_source_access(self):
        self._create_test_web_form_source(
            extra_data={'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER}
        )

        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_web_form_file_upload_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.objects.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_form_file_upload_api_view_with_full_access(self):
        self._create_test_web_form_source(
            extra_data={'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER}
        )

        self.grant_access(
            obj=self._test_document_type, permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_web_form_file_upload_action_api_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(Document.objects.count(), document_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 5)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active
        test_document_version_page = test_document_version.pages.first()

        self.assertEqual(events[0].action_object, self._test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_file)
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        self.assertEqual(events[3].action_object, test_document)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version)
        self.assertEqual(events[3].verb, event_document_version_created.id)

        self.assertEqual(events[4].action_object, test_document_version)
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(events[4].target, test_document_version_page)
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )

    def test_web_form_compressed_file_upload_api_view_with_full_access(self):
        self._create_test_web_form_source(
            extra_data={'uncompress': SOURCE_UNCOMPRESS_CHOICE_ASK}
        )

        self.grant_access(
            obj=self._test_document_type, permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_web_form_file_upload_action_api_view(test_file_path=TEST_FILE_COMPRESSED_PATH)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(Document.objects.count(), document_count + 2)

        events = self._get_test_events()
        self.assertEqual(events.count(), 11)

        test_documents = (Document.objects.first(), Document.objects.last())
        test_document_files = (
            test_documents[0].file_latest, test_documents[1].file_latest
        )
        test_document_versions = (
            test_documents[0].version_active, test_documents[1].version_active
        )
        test_document_version_pages = (
            test_document_versions[0].pages.first(),
            test_document_versions[1].pages.first(),
            test_document_versions[1].pages.last()
        )

        self.assertEqual(events[0].action_object, self._test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_documents[0])
        self.assertEqual(events[0].verb, event_document_created.id)

        self.assertEqual(events[1].action_object, test_documents[0])
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_files[0])
        self.assertEqual(events[1].verb, event_document_file_created.id)

        self.assertEqual(events[2].action_object, test_documents[0])
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_files[0])
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        self.assertEqual(events[3].action_object, test_documents[0])
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_versions[0])
        self.assertEqual(events[3].verb, event_document_version_created.id)

        self.assertEqual(events[4].action_object, test_document_versions[0])
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(events[4].target, test_document_version_pages[0])
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )

        self.assertEqual(events[5].action_object, self._test_document_type)
        self.assertEqual(events[5].actor, self._test_case_user)
        self.assertEqual(events[5].target, test_documents[1])
        self.assertEqual(events[5].verb, event_document_created.id)

        self.assertEqual(events[6].action_object, test_documents[1])
        self.assertEqual(events[6].actor, self._test_case_user)
        self.assertEqual(events[6].target, test_document_files[1])
        self.assertEqual(events[6].verb, event_document_file_created.id)

        self.assertEqual(events[7].action_object, test_documents[1])
        self.assertEqual(events[7].actor, self._test_case_user)
        self.assertEqual(events[7].target, test_document_files[1])
        self.assertEqual(events[7].verb, event_document_file_edited.id)

        self.assertEqual(events[8].action_object, test_documents[1])
        self.assertEqual(events[8].actor, self._test_case_user)
        self.assertEqual(events[8].target, test_document_versions[1])
        self.assertEqual(events[8].verb, event_document_version_created.id)

        self.assertEqual(events[9].action_object, test_document_versions[1])
        self.assertEqual(events[9].actor, self._test_case_user)
        self.assertEqual(events[9].target, test_document_version_pages[1])
        self.assertEqual(
            events[9].verb, event_document_version_page_created.id
        )

        self.assertEqual(events[10].action_object, test_document_versions[1])
        self.assertEqual(events[10].actor, self._test_case_user)
        self.assertEqual(events[10].target, test_document_version_pages[2])
        self.assertEqual(
            events[10].verb, event_document_version_page_created.id
        )
