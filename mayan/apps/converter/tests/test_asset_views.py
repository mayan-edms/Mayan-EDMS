from mayan.apps.testing.tests.base import GenericViewTestCase

from .mixins import AssetTestMixin, AssetViewTestMixin

from ..events import event_asset_created, event_asset_edited
from ..models import Asset
from ..permissions import (
    permission_asset_create, permission_asset_delete,
    permission_asset_edit, permission_asset_view,
)


class AssetViewTestCase(
    AssetTestMixin, AssetViewTestMixin, GenericViewTestCase
):
    def test_asset_create_view_no_permission(self):
        asset_count = Asset.objects.count()

        self._clear_events()

        response = self._request_test_asset_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Asset.objects.count(), asset_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_create_view_with_permissions(self):
        self.grant_permission(permission=permission_asset_create)

        asset_count = Asset.objects.count()

        self._clear_events()

        response = self._request_test_asset_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Asset.objects.count(), asset_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_asset)
        self.assertEqual(events[0].verb, event_asset_created.id)

    def test_asset_delete_view_no_permission(self):
        self._create_test_asset()

        asset_count = Asset.objects.count()

        self._clear_events()

        response = self._request_test_asset_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Asset.objects.count(), asset_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_delete_view_with_access(self):
        self._create_test_asset()

        self.grant_access(
            obj=self.test_asset, permission=permission_asset_delete
        )

        asset_count = Asset.objects.count()

        self._clear_events()

        response = self._request_test_asset_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Asset.objects.count(), asset_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_detail_view_no_permission(self):
        self._create_test_asset()

        self._clear_events()

        response = self._request_test_asset_detail_view()
        self.assertNotContains(
            response=response, text=self.test_asset.label, status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_detail_view_with_access(self):
        self._create_test_asset()

        self.grant_access(
            obj=self.test_asset, permission=permission_asset_view
        )

        self._clear_events()

        response = self._request_test_asset_detail_view()
        self.assertContains(
            response=response, text=self.test_asset.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_edit_view_no_permission(self):
        self._create_test_asset()

        asset_label = self.test_asset.label

        self._clear_events()

        response = self._request_test_asset_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_asset.refresh_from_db()
        self.assertEqual(self.test_asset.label, asset_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_edit_view_with_access(self):
        self._create_test_asset()

        self.grant_access(
            obj=self.test_asset, permission=permission_asset_edit
        )

        asset_label = self.test_asset.label

        self._clear_events()

        response = self._request_test_asset_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_asset.refresh_from_db()
        self.assertNotEqual(self.test_asset.label, asset_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_asset)
        self.assertEqual(events[0].verb, event_asset_edited.id)

    def test_asset_list_view_with_no_permission(self):
        self._create_test_asset()

        self._clear_events()

        response = self._request_test_asset_list_view()
        self.assertNotContains(
            response=response, text=self.test_asset.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_list_view_with_access(self):
        self._create_test_asset()

        self.grant_access(obj=self.test_asset, permission=permission_asset_view)

        self._clear_events()

        response = self._request_test_asset_list_view()
        self.assertContains(
            response=response, text=self.test_asset.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
