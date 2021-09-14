from django.core.exceptions import ValidationError

from mayan.apps.documents.events import (
    event_document_created, event_document_file_created,
    event_document_file_edited, event_document_version_created
)
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.metadata.models import MetadataType

from ..events import event_source_created
from ..models import Source
from ..permissions import permission_sources_create, permission_sources_edit

from .literals import TEST_EMAIL_BASE64_FILENAME
from .mixins.email_source_mixins import (
    EmailSourceBackendTestMixin, EmailSourceBackendViewTestMixin
)


class EmailSourceViewTestCase(
    EmailSourceBackendTestMixin, EmailSourceBackendViewTestMixin,
    GenericDocumentViewTestCase
):
    _test_email_source_content = TEST_EMAIL_BASE64_FILENAME
    auto_upload_test_document = False

    def test_email_source_create_view(self):
        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_email_source_create_view()

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Source.objects.count(), source_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_created.id)

    def test_metadata_type_validation_invalid_from(self):
        self._silence_logger(name='mayan.apps.logging.middleware')
        self._silence_logger(name='mayan.apps.navigation.classes')

        test_metadata_type = MetadataType.objects.create(
            name='test_metadata_type'
        )

        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        with self.assertRaises(expected_exception=ValidationError):
            response = self._request_test_email_source_create_view(
                extra_data={
                    'from_metadata_type_id': test_metadata_type.pk,
                }
            )
            self.assertEqual(response.status_code, 200)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_validation_valid_from(self):
        test_metadata_type = MetadataType.objects.create(
            name='test_metadata_type'
        )

        self.test_document_type.metadata.create(
            metadata_type=test_metadata_type
        )

        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_email_source_create_view(
            extra_data={
                'from_metadata_type_id': test_metadata_type.pk,
            }
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Source.objects.count(), source_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_created.id)

    def test_metadata_type_validation_invalid_subject(self):
        self._silence_logger(name='mayan.apps.logging.middleware')
        self._silence_logger(name='mayan.apps.navigation.classes')

        test_metadata_type = MetadataType.objects.create(
            name='test_metadata_type'
        )

        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        with self.assertRaises(expected_exception=ValidationError):
            response = self._request_test_email_source_create_view(
                extra_data={
                    'subject_metadata_type_id': test_metadata_type.pk
                }
            )
            self.assertEqual(response.status_code, 200)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_metadata_type_validation_valid_subject(self):
        test_metadata_type = MetadataType.objects.create(
            name='test_metadata_type'
        )

        self.test_document_type.metadata.create(
            metadata_type=test_metadata_type
        )

        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_email_source_create_view(
            extra_data={
                'subject_metadata_type_id': test_metadata_type.pk
            }
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Source.objects.count(), source_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_created.id)

    def test_email_source_test_view_no_permission(self):
        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_source_test_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Document.objects.count(), document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_email_source_test_view_with_access(self):
        self._silence_logger(name='mayan.apps.converter')

        self.grant_access(
            obj=self.test_source, permission=permission_sources_edit
        )

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_source_test_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Document.objects.count(), document_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, test_document)
        self.assertEqual(events[0].target, test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, test_document_file)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, test_document_file)
        self.assertEqual(events[2].target, test_document_file)
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        self.assertEqual(events[3].action_object, test_document)
        self.assertEqual(events[3].actor, test_document_version)
        self.assertEqual(events[3].target, test_document_version)
        self.assertEqual(events[3].verb, event_document_version_created.id)
