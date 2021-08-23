from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_source_created, event_source_edited
from ..models import Source
from ..permissions import (
    permission_sources_create, permission_sources_delete,
    permission_sources_edit, permission_sources_view
)

from .mixins.base_mixins import SourceAPIViewTestMixin, SourceTestMixin


class SourceAPIViewTestCase(
    SourceAPIViewTestMixin, SourceTestMixin, BaseAPITestCase
):
    auto_create_test_source = False

    def test_source_create_api_view_no_permission(self):
        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Source.objects.count(), source_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_created.id)

    def test_source_delete_api_view_no_permission(self):
        self._create_test_source()

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_delete_api_view_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_delete
        )

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Source.objects.count(), source_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_edit_api_view_via_patch_no_permission(self):
        self._create_test_source()

        source_label = self.test_source.label

        self._clear_events()

        response = self._request_test_source_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_source.refresh_from_db()
        self.assertEqual(self.test_source.label, source_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_edit_api_view_via_patch_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_edit
        )

        source_label = self.test_source.label

        self._clear_events()

        response = self._request_test_source_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_source.refresh_from_db()
        self.assertNotEqual(self.test_source.label, source_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_edited.id)

    def test_source_edit_api_view_via_put_no_permission(self):
        self._create_test_source()

        source_label = self.test_source.label

        self._clear_events()

        response = self._request_test_source_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_source.refresh_from_db()
        self.assertEqual(self.test_source.label, source_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_edit_api_view_via_put_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_edit
        )

        source_label = self.test_source.label

        self._clear_events()

        response = self._request_test_source_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_source.refresh_from_db()
        self.assertNotEqual(self.test_source.label, source_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_source)
        self.assertEqual(events[0].verb, event_source_edited.id)

    def test_source_api_list_api_view_no_permission(self):
        self._create_test_source()

        self._clear_events()

        response = self._request_test_source_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_api_list_api_view_with_access(self):
        self._create_test_source()

        self.grant_access(
            obj=self.test_source, permission=permission_sources_view
        )
        self._clear_events()

        response = self._request_test_source_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_source.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
