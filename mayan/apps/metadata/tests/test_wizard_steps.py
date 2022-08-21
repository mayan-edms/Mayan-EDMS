from mayan.apps.documents.events import (
    event_document_created, event_document_file_created,
    event_document_file_edited, event_document_version_created,
    event_document_version_page_created
)
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.sources.tests.mixins.web_form_source_mixins import WebFormSourceBackendTestMixin

from ..events import (
    event_document_metadata_added, event_document_metadata_edited
)

from .literals import (
    TEST_METADATA_VALUE_UNICODE, TEST_METADATA_VALUE_WITH_AMPERSAND
)
from .mixins import (
    MetadataDocumentUploadWizardStepTestMixin, MetadataTypeTestMixin
)


class DocumentUploadMetadataTestCase(
    MetadataDocumentUploadWizardStepTestMixin, MetadataTypeTestMixin,
    WebFormSourceBackendTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type()
        self._test_document_type.metadata.create(
            metadata_type=self._test_metadata_type, required=True
        )

    def test_upload_interactive_with_unicode_metadata(self):
        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        self._clear_events()

        response = self._request_upload_interactive_document_create_view(
            metadata_value=TEST_METADATA_VALUE_UNICODE
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(
            Document.objects.first().metadata.first().value,
            TEST_METADATA_VALUE_UNICODE
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 7)

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

        self.assertEqual(events[5].action_object, self._test_metadata_type)
        self.assertEqual(events[5].actor, test_document)
        self.assertEqual(events[5].target, test_document)
        self.assertEqual(events[5].verb, event_document_metadata_added.id)

        self.assertEqual(events[6].action_object, self._test_metadata_type)
        self.assertEqual(events[6].actor, test_document)
        self.assertEqual(events[6].target, test_document)
        self.assertEqual(events[6].verb, event_document_metadata_edited.id)

    def test_upload_interactive_with_ampersand_metadata(self):
        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        self._clear_events()

        response = self._request_upload_interactive_document_create_view(
            metadata_value=TEST_METADATA_VALUE_WITH_AMPERSAND
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(
            Document.objects.first().metadata.first().value,
            TEST_METADATA_VALUE_WITH_AMPERSAND
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 7)

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

        self.assertEqual(events[5].action_object, self._test_metadata_type)
        self.assertEqual(events[5].actor, test_document)
        self.assertEqual(events[5].target, test_document)
        self.assertEqual(events[5].verb, event_document_metadata_added.id)

        self.assertEqual(events[6].action_object, self._test_metadata_type)
        self.assertEqual(events[6].actor, test_document)
        self.assertEqual(events[6].target, test_document)
        self.assertEqual(events[6].verb, event_document_metadata_edited.id)

    def test_initial_step_conditions(self):
        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        self._clear_events()

        response = self._request_document_create_view()
        self.assertContains(
            response=response, status_code=200, text='Step 2'
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
