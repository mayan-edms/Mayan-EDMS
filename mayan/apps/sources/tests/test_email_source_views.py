from django.core.exceptions import ValidationError

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.metadata.models import MetadataType

from ..events import event_source_created
from ..models import Source
from ..permissions import permission_sources_create

from .mixins.email_source_mixins import (
    EmailSourceBackendTestMixin, EmailSourceBackendViewTestMixin
)


class EmailSourceViewTestCase(
    EmailSourceBackendTestMixin, EmailSourceBackendViewTestMixin,
    GenericDocumentViewTestCase
):
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
