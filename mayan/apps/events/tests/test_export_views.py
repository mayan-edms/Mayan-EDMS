from django.contrib.contenttypes.models import ContentType

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.messaging.events import event_message_created
from mayan.apps.messaging.models import Message
from mayan.apps.storage.events import event_download_file_created
from mayan.apps.storage.models import DownloadFile

from ..events import event_events_exported
from ..permissions import permission_events_export

from .mixins import (
    EventsExportViewTestMixin, EventTestMixin, EventTypeTestMixin
)


class EventExportViewTestCase(
    EventTestMixin, EventTypeTestMixin, EventsExportViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_event_type()
        self._create_test_user()
        self.test_object = self.test_document_type

        content_type = ContentType.objects.get_for_model(
            model=self.test_object
        )

        self.view_arguments = {
            'app_label': content_type.app_label,
            'model_name': content_type.model,
            'object_id': self.test_object.pk
        }

        ModelPermission.register(
            model=self.test_object._meta.model, permissions=(
                permission_events_export,
            )
        )

        self._clear_events()

    def test_events_list_export_view_no_permission(self):
        self._clear_events()

        self._create_test_event(target=self.test_object)

        response = self._request_test_events_list_export_view()
        self.assertEqual(response.status_code, 302)

        test_download_file = DownloadFile.objects.first()
        test_message = Message.objects.first()

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        self.assertEqual(events.first(), self.test_event)

        self.assertEqual(
            events[0].action_object, self.test_event.action_object
        )
        self.assertEqual(events[0].actor, self.test_event.actor)
        self.assertEqual(events[0].target, self.test_event.target)
        self.assertEqual(events[0].verb, self.test_event.verb)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_download_file)
        self.assertEqual(events[1].verb, event_download_file_created.id)

        self.assertEqual(events[2].action_object, None)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_download_file)
        self.assertEqual(events[2].verb, event_events_exported.id)

        self.assertEqual(events[3].action_object, None)
        self.assertEqual(events[3].actor, test_message)
        self.assertEqual(events[3].target, test_message)
        self.assertEqual(events[3].verb, event_message_created.id)

        with test_download_file.open() as file_object:
            self.assertTrue(
                str(self.test_object).encode() not in file_object.read()
            )

    def test_events_list_export_view_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_events_export
        )

        self._clear_events()

        self._create_test_event(target=self.test_object)

        response = self._request_test_events_list_export_view()
        self.assertEqual(response.status_code, 302)

        test_download_file = DownloadFile.objects.first()
        test_message = Message.objects.first()

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        self.assertEqual(
            events[0].action_object, self.test_event.action_object
        )
        self.assertEqual(events[0].actor, self.test_event.actor)
        self.assertEqual(events[0].target, self.test_event.target)
        self.assertEqual(events[0].verb, self.test_event.verb)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_download_file)
        self.assertEqual(events[1].verb, event_download_file_created.id)

        self.assertEqual(events[2].action_object, None)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_download_file)
        self.assertEqual(events[2].verb, event_events_exported.id)

        self.assertEqual(events[3].action_object, None)
        self.assertEqual(events[3].actor, test_message)
        self.assertEqual(events[3].target, test_message)
        self.assertEqual(events[3].verb, event_message_created.id)

        with test_download_file.open() as file_object:
            self.assertTrue(
                str(self.test_object).encode() in file_object.read()
            )

    def test_events_for_object_export_view_no_permission(self):
        self._clear_events()

        self._create_test_event(
            actor=self.test_user, action_object=self.test_object
        )

        response = self._request_events_for_object_export_view()
        self.assertEqual(response.status_code, 302)

        test_download_file = DownloadFile.objects.first()
        test_message = Message.objects.first()

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        self.assertEqual(
            events[0].action_object, self.test_event.action_object
        )
        self.assertEqual(events[0].actor, self.test_event.actor)
        self.assertEqual(events[0].target, self.test_event.target)
        self.assertEqual(events[0].verb, self.test_event.verb)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_download_file)
        self.assertEqual(events[1].verb, event_download_file_created.id)

        self.assertEqual(events[2].action_object, None)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_download_file)
        self.assertEqual(events[2].verb, event_events_exported.id)

        self.assertEqual(events[3].action_object, None)
        self.assertEqual(events[3].actor, test_message)
        self.assertEqual(events[3].target, test_message)
        self.assertEqual(events[3].verb, event_message_created.id)

        with test_download_file.open() as file_object:
            self.assertTrue(
                str(self.test_object).encode() not in file_object.read()
            )

    def test_events_for_object_export_view_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_events_export
        )

        self._clear_events()

        self._create_test_event(
            actor=self.test_user, action_object=self.test_object
        )

        response = self._request_events_for_object_export_view()
        self.assertEqual(response.status_code, 302)

        test_download_file = DownloadFile.objects.first()
        test_message = Message.objects.first()

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        self.assertEqual(
            events[0].action_object, self.test_event.action_object
        )
        self.assertEqual(events[0].actor, self.test_event.actor)
        self.assertEqual(events[0].target, self.test_event.target)
        self.assertEqual(events[0].verb, self.test_event.verb)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_download_file)
        self.assertEqual(events[1].verb, event_download_file_created.id)

        self.assertEqual(events[2].action_object, None)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_download_file)
        self.assertEqual(events[2].verb, event_events_exported.id)

        self.assertEqual(events[3].action_object, None)
        self.assertEqual(events[3].actor, test_message)
        self.assertEqual(events[3].target, test_message)
        self.assertEqual(events[3].verb, event_message_created.id)

        with test_download_file.open() as file_object:
            self.assertTrue(
                str(self.test_object).encode() in file_object.read()
            )

    def test_events_by_verb_export_view_no_permission(self):
        self._clear_events()

        self._create_test_event(
            actor=self.test_user, action_object=self.test_object
        )

        response = self._request_test_events_by_verb_export_view()
        self.assertEqual(response.status_code, 302)

        test_download_file = DownloadFile.objects.first()
        test_message = Message.objects.first()

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        self.assertEqual(
            events[0].action_object, self.test_event.action_object
        )
        self.assertEqual(events[0].actor, self.test_event.actor)
        self.assertEqual(events[0].target, self.test_event.target)
        self.assertEqual(events[0].verb, self.test_event.verb)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_download_file)
        self.assertEqual(events[1].verb, event_download_file_created.id)

        self.assertEqual(events[2].action_object, None)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_download_file)
        self.assertEqual(events[2].verb, event_events_exported.id)

        self.assertEqual(events[3].action_object, None)
        self.assertEqual(events[3].actor, test_message)
        self.assertEqual(events[3].target, test_message)
        self.assertEqual(events[3].verb, event_message_created.id)

        with test_download_file.open() as file_object:
            self.assertTrue(
                str(self.test_object).encode() not in file_object.read()
            )

    def test_events_by_verb_view_export_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_events_export
        )

        self._clear_events()

        self._create_test_event(
            actor=self.test_user, action_object=self.test_object
        )

        response = self._request_test_events_by_verb_export_view()
        self.assertEqual(response.status_code, 302)

        test_download_file = DownloadFile.objects.first()
        test_message = Message.objects.first()

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        self.assertEqual(
            events[0].action_object, self.test_event.action_object
        )
        self.assertEqual(events[0].actor, self.test_event.actor)
        self.assertEqual(events[0].target, self.test_event.target)
        self.assertEqual(events[0].verb, self.test_event.verb)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_download_file)
        self.assertEqual(events[1].verb, event_download_file_created.id)

        self.assertEqual(events[2].action_object, None)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_download_file)
        self.assertEqual(events[2].verb, event_events_exported.id)

        self.assertEqual(events[3].action_object, None)
        self.assertEqual(events[3].actor, test_message)
        self.assertEqual(events[3].target, test_message)
        self.assertEqual(events[3].verb, event_message_created.id)

        with test_download_file.open() as file_object:
            self.assertTrue(
                str(self.test_object).encode() in file_object.read()
            )

    def test_current_user_events_export_view_no_permission(self):
        self._clear_events()

        self._create_test_event(
            actor=self._test_case_user, action_object=self.test_object
        )

        response = self._request_test_current_user_events_export_view()
        self.assertNotContains(
            response=response, text=str(self.test_event_type), status_code=302
        )

        test_download_file = DownloadFile.objects.first()
        test_message = Message.objects.first()

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        self.assertEqual(
            events[0].action_object, self.test_event.action_object
        )
        self.assertEqual(events[0].actor, self.test_event.actor)
        self.assertEqual(events[0].target, self.test_event.target)
        self.assertEqual(events[0].verb, self.test_event.verb)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_download_file)
        self.assertEqual(events[1].verb, event_download_file_created.id)

        self.assertEqual(events[2].action_object, None)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_download_file)
        self.assertEqual(events[2].verb, event_events_exported.id)

        self.assertEqual(events[3].action_object, None)
        self.assertEqual(events[3].actor, test_message)
        self.assertEqual(events[3].target, test_message)
        self.assertEqual(events[3].verb, event_message_created.id)

        with test_download_file.open() as file_object:
            self.assertTrue(
                str(self.test_object).encode() not in file_object.read()
            )

    def test_current_user_events_export_view_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_events_export
        )

        self._clear_events()

        self._create_test_event(
            actor=self._test_case_user, action_object=self.test_object
        )

        response = self._request_test_current_user_events_export_view()
        self.assertEqual(response.status_code, 302)

        test_download_file = DownloadFile.objects.first()
        test_message = Message.objects.first()

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        self.assertEqual(
            events[0].action_object, self.test_event.action_object
        )
        self.assertEqual(events[0].actor, self.test_event.actor)
        self.assertEqual(events[0].target, self.test_event.target)
        self.assertEqual(events[0].verb, self.test_event.verb)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_download_file)
        self.assertEqual(events[1].verb, event_download_file_created.id)

        self.assertEqual(events[2].action_object, None)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_download_file)
        self.assertEqual(events[2].verb, event_events_exported.id)

        self.assertEqual(events[3].action_object, None)
        self.assertEqual(events[3].actor, test_message)
        self.assertEqual(events[3].target, test_message)
        self.assertEqual(events[3].verb, event_message_created.id)

        with test_download_file.open() as file_object:
            self.assertTrue(
                str(self.test_object).encode() in file_object.read()
            )
