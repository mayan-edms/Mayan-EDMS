from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.events.classes import ModelEventType

from ..events import event_index_template_edited
from ..permissions import permission_index_template_edit

from .mixins import (
    IndexTemplateEventTriggerViewTestMixin, IndexTemplateTestMixin
)


class IndexTemplateEventTriggerViewTestCase(
    IndexTemplateTestMixin, IndexTemplateEventTriggerViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_index_template_event_trigger_get_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_template_event_trigger_get_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_event_trigger_get_view_with_access(self):
        self.grant_access(
            obj=self._test_index_template,
            permission=permission_index_template_edit
        )

        self._clear_events()

        response = self._request_test_index_template_event_trigger_get_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_event_trigger_add_view_no_permission(self):
        stored_event_type_id = ModelEventType.get_for_class(
            klass=Document
        )[3].stored_event_type.pk

        self._test_index_template.event_triggers.get(
            stored_event_type_id=stored_event_type_id
        ).delete()

        test_index_template_event_trigger_count = self._test_index_template.event_triggers.count()

        self._clear_events()

        response = self._request_test_index_template_event_trigger_add_view(
            stored_event_type_id=stored_event_type_id
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self._test_index_template.event_triggers.count(),
            test_index_template_event_trigger_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_event_trigger_add_view_with_access(self):
        self.grant_access(
            obj=self._test_index_template,
            permission=permission_index_template_edit
        )

        stored_event_type_id = ModelEventType.get_for_class(
            klass=Document
        )[3].stored_event_type.pk

        self._test_index_template.event_triggers.get(
            stored_event_type_id=stored_event_type_id
        ).delete()

        test_index_template_event_trigger_count = self._test_index_template.event_triggers.count()

        self._clear_events()

        response = self._request_test_index_template_event_trigger_add_view(
            stored_event_type_id=stored_event_type_id
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_index_template.event_triggers.count(),
            test_index_template_event_trigger_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_index_template)
        self.assertEqual(events[0].verb, event_index_template_edited.id)

    def test_index_template_event_trigger_remove_view_no_permission(self):
        test_index_template_event_trigger_count = self._test_index_template.event_triggers.count()

        stored_event_type_id = ModelEventType.get_for_class(
            klass=Document
        )[3].stored_event_type.pk

        self._clear_events()

        response = self._request_test_index_template_event_trigger_remove_view(
            stored_event_type_id=stored_event_type_id
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self._test_index_template.event_triggers.count(),
            test_index_template_event_trigger_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_template_event_trigger_remove_view_with_access(self):
        self.grant_access(
            obj=self._test_index_template,
            permission=permission_index_template_edit
        )

        test_index_template_event_trigger_count = self._test_index_template.event_triggers.count()

        stored_event_type_id = ModelEventType.get_for_class(
            klass=Document
        )[3].stored_event_type.pk

        self._clear_events()

        response = self._request_test_index_template_event_trigger_remove_view(
            stored_event_type_id=stored_event_type_id
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_index_template.event_triggers.count(),
            test_index_template_event_trigger_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_index_template)
        self.assertEqual(events[0].verb, event_index_template_edited.id)
