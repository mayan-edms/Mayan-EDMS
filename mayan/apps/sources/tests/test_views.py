from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_source_created, event_source_edited
from ..models import Source
from ..permissions import (
    permission_sources_create, permission_sources_delete,
    permission_sources_edit, permission_sources_view
)

from .literals import TEST_SOURCE_LABEL
from .mixins.base_mixins import SourceTestMixin, SourceViewTestMixin


class SourceViewTestCase(
    SourceTestMixin, SourceViewTestMixin, GenericViewTestCase
):
    auto_create_test_source = False

    def test_source_create_view_no_permission(self):
        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_create_view_with_permission(self):
        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_source.label, TEST_SOURCE_LABEL)
        self.assertEqual(Source.objects.count(), source_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_created.id)

    def test_source_delete_view_no_permission(self):
        self._create_test_source()

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_delete_view_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_delete
        )

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Source.objects.count(), source_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_edit_view_no_permission(self):
        self._create_test_source()
        test_instance_values = self._model_instance_to_dictionary(
            instance=self.test_source
        )

        self._clear_events()

        response = self._request_test_source_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_source.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_source
            ), test_instance_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_edit_view_with_access(self):
        self._create_test_source()
        test_instance_values = self._model_instance_to_dictionary(
            instance=self.test_source
        )
        self.grant_access(
            obj=self.test_source, permission=permission_sources_edit
        )

        self._clear_events()

        response = self._request_test_source_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_source.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_source
            ), test_instance_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_edited.id)

    def test_source_list_view_no_permission(self):
        self._create_test_source()

        self._clear_events()

        response = self._request_test_source_list_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_list_view_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_view
        )

        self._clear_events()

        response = self._request_test_source_list_view()
        self.assertContains(
            response=response, text=self.test_source.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_test_get_view_no_permission(self):
        self._create_test_source()

        self._clear_events()

        response = self._request_test_source_test_get_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_test_get_view_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_edit
        )

        self._clear_events()

        response = self._request_test_source_test_get_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_test_post_view_no_permission(self):
        self._create_test_source()

        self._clear_events()

        response = self._request_test_source_test_post_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_test_post_view_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_edit
        )

        self._clear_events()

        response = self._request_test_source_test_post_view()
        self.assertEqual(response.status_code, 302)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
