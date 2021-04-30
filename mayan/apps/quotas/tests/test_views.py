from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_quota_created, event_quota_edited
from ..models import Quota
from ..permissions import (
    permission_quota_create, permission_quota_delete, permission_quota_edit,
    permission_quota_view
)

from .mixins import QuotaTestMixin, QuotaViewTestMixin


class QuotaViewTestCase(
    QuotaTestMixin, QuotaViewTestMixin, GenericViewTestCase
):
    def test_quota_backend_selection_get_view_no_permission(self):
        self._clear_events()

        response = self._request_test_quota_backend_selection_get_view()
        self.assertEqual(response.status_code, 403)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_quota_backend_selection_get_view_with_permissions(self):
        self.grant_permission(permission=permission_quota_create)

        self._clear_events()

        response = self._request_test_quota_backend_selection_get_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_quota_create_get_view_no_permission(self):
        quota_count = Quota.objects.count()

        self._clear_events()

        response = self._request_test_quota_create_get_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Quota.objects.count(), quota_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_quota_create_get_view_with_permissions(self):
        self.grant_permission(permission=permission_quota_create)

        quota_count = Quota.objects.count()

        self._clear_events()

        response = self._request_test_quota_create_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Quota.objects.count(), quota_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_quota_with_mixins_create_get_view_with_permissions(self):
        self.grant_permission(permission=permission_quota_create)

        quota_count = Quota.objects.count()

        self._clear_events()

        response = self._request_test_quota_with_mixins_create_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Quota.objects.count(), quota_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_quota_create_post_view_no_permission(self):
        quota_count = Quota.objects.count()

        self._clear_events()

        response = self._request_test_quota_create_post_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Quota.objects.count(), quota_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_quota_create_post_view_with_permissions(self):
        self.grant_permission(permission=permission_quota_create)

        quota_count = Quota.objects.count()

        self._clear_events()

        response = self._request_test_quota_create_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Quota.objects.count(), quota_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_quota)
        self.assertEqual(events[0].verb, event_quota_created.id)

    def test_quota_delete_view_no_permission(self):
        self._create_test_quota()

        quota_count = Quota.objects.count()

        self._clear_events()

        response = self._request_test_quota_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Quota.objects.count(), quota_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_quota_delete_view_with_access(self):
        self._create_test_quota()

        self.grant_access(
            obj=self.test_quota, permission=permission_quota_delete
        )

        quota_count = Quota.objects.count()

        self._clear_events()

        response = self._request_test_quota_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Quota.objects.count(), quota_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_quota_edit_view_no_permission(self):
        self._create_test_quota()

        quota_test_limit = self.test_quota.loads()['test_limit']

        self._clear_events()

        response = self._request_test_quota_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_quota.refresh_from_db()
        self.assertEqual(
            self.test_quota.loads()['test_limit'], quota_test_limit
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_quota_edit_view_with_access(self):
        self._create_test_quota()

        quota_test_limit = self.test_quota.loads()['test_limit']

        self.grant_access(
            obj=self.test_quota, permission=permission_quota_edit
        )

        self._clear_events()

        response = self._request_test_quota_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_quota.refresh_from_db()
        self.assertNotEqual(
            self.test_quota.loads()['test_limit'], quota_test_limit
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_quota)
        self.assertEqual(events[0].verb, event_quota_edited.id)

    def test_quota_list_view_with_no_permission(self):
        self._create_test_quota()

        self._clear_events()

        response = self._request_test_quota_list_view()
        self.assertNotContains(
            response=response, text=self.test_quota.backend_label(),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_quota_list_view_with_access(self):
        self._create_test_quota()

        self.grant_access(
            obj=self.test_quota, permission=permission_quota_view
        )

        self._clear_events()

        response = self._request_test_quota_list_view()
        self.assertContains(
            response=response, text=self.test_quota.backend_label(),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
