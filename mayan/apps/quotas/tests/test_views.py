from mayan.apps.tests.tests.base import GenericViewTestCase

from ..models import Quota
from ..permissions import (
    permission_quota_create, permission_quota_delete, permission_quota_edit,
    permission_quota_view
)

from .mixins import QuotaTestMixin, QuotaViewTestMixin


class QuotaViewTestCase(
    QuotaTestMixin, QuotaViewTestMixin, GenericViewTestCase
):
    def test_quota_backend_selection_get_view_no_permissions(self):
        response = self._request_test_quota_backend_selection_get_view()
        self.assertEqual(response.status_code, 403)

    def test_quota_backend_selection_get_view_with_permissions(self):
        self.grant_permission(permission=permission_quota_create)

        response = self._request_test_quota_backend_selection_get_view()
        self.assertEqual(response.status_code, 200)

    def test_quota_create_view_no_permissions(self):
        quota_count = Quota.objects.count()

        response = self._request_test_quota_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Quota.objects.count(), quota_count)

    def test_quota_create_view_with_permissions(self):
        self.grant_permission(permission=permission_quota_create)

        quota_count = Quota.objects.count()

        response = self._request_test_quota_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Quota.objects.count(), quota_count + 1)

    def test_quota_delete_view_no_permissions(self):
        self._create_test_quota()

        quota_count = Quota.objects.count()

        response = self._request_test_quota_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Quota.objects.count(), quota_count)

    def test_quota_delete_view_with_access(self):
        self._create_test_quota()

        self.grant_access(
            obj=self.test_quota, permission=permission_quota_delete
        )

        quota_count = Quota.objects.count()

        response = self._request_test_quota_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Quota.objects.count(), quota_count - 1)

    def test_quota_edit_view_no_permissions(self):
        self._create_test_quota()

        quota_test_limit = self.test_quota.loads()['test_limit']

        response = self._request_test_quota_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_quota.refresh_from_db()
        self.assertEqual(
            self.test_quota.loads()['test_limit'], quota_test_limit
        )

    def test_quota_edit_view_with_access(self):
        self._create_test_quota()

        quota_test_limit = self.test_quota.loads()['test_limit']

        self.grant_access(
            obj=self.test_quota, permission=permission_quota_edit
        )

        response = self._request_test_quota_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_quota.refresh_from_db()
        self.assertNotEqual(
            self.test_quota.loads()['test_limit'], quota_test_limit
        )

    def test_quota_list_view_with_no_permission(self):
        self._create_test_quota()

        response = self._request_test_quota_list_view()
        self.assertNotContains(
            response=response, text=self.test_quota.backend_label(),
            status_code=200
        )

    def test_quota_list_view_with_access(self):
        self._create_test_quota()

        self.grant_access(
            obj=self.test_quota, permission=permission_quota_view
        )

        response = self._request_test_quota_list_view()
        self.assertContains(
            response=response, text=self.test_quota.backend_label(),
            status_code=200
        )
