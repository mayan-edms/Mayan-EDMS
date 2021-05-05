from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_asset_created, event_asset_edited
from ..models import Asset
from ..permissions import (
    permission_asset_create, permission_asset_delete,
    permission_asset_edit, permission_asset_view
)

from .mixins import AssetAPIViewTestMixin, AssetTestMixin


class AssetAPIViewTestCase(
    AssetAPIViewTestMixin, AssetTestMixin, BaseAPITestCase
):
    def test_asset_create_api_view_no_permission(self):
        asset_count = Asset.objects.count()

        self._clear_events()

        response = self._request_test_asset_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Asset.objects.count(), asset_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_asset_create)

        asset_count = Asset.objects.count()

        self._clear_events()

        response = self._request_test_asset_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Asset.objects.count(), asset_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_asset)
        self.assertEqual(events[0].verb, event_asset_created.id)

    def test_asset_delete_api_view_no_permission(self):
        self._create_test_asset()

        asset_count = Asset.objects.count()

        self._clear_events()

        response = self._request_test_asset_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Asset.objects.count(), asset_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_delete_api_view_with_access(self):
        self._create_test_asset()

        self.grant_access(obj=self.test_asset, permission=permission_asset_delete)

        asset_count = Asset.objects.count()

        self._clear_events()

        response = self._request_test_asset_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Asset.objects.count(), asset_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_detail_api_view_no_permission(self):
        self._create_test_asset()

        self._clear_events()

        response = self._request_test_asset_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_detail_api_view_with_access(self):
        self._create_test_asset()
        self.grant_access(
            obj=self.test_asset, permission=permission_asset_view
        )

        self._clear_events()

        response = self._request_test_asset_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['label'], self.test_asset.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_edit_api_view_via_patch_no_permission(self):
        self._create_test_asset()

        asset_label = self.test_asset.label

        self._clear_events()

        response = self._request_test_asset_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_asset.refresh_from_db()
        self.assertEqual(self.test_asset.label, asset_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_edit_api_view_via_patch_with_access(self):
        self._create_test_asset()

        self.grant_access(obj=self.test_asset, permission=permission_asset_edit)

        asset_label = self.test_asset.label

        self._clear_events()

        response = self._request_test_asset_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_asset.refresh_from_db()
        self.assertNotEqual(self.test_asset.label, asset_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_asset)
        self.assertEqual(events[0].verb, event_asset_edited.id)

    def test_asset_edit_api_view_via_put_no_permission(self):
        self._create_test_asset()

        asset_label = self.test_asset.label

        self._clear_events()

        response = self._request_test_asset_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_asset.refresh_from_db()
        self.assertEqual(self.test_asset.label, asset_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_edit_api_view_via_put_with_access(self):
        self._create_test_asset()

        self.grant_access(obj=self.test_asset, permission=permission_asset_edit)

        asset_label = self.test_asset.label

        self._clear_events()

        response = self._request_test_asset_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_asset.refresh_from_db()
        self.assertNotEqual(self.test_asset.label, asset_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_asset)
        self.assertEqual(events[0].verb, event_asset_edited.id)

    def test_asset_list_api_view_no_permission(self):
        self._create_test_asset()

        self._clear_events()

        response = self._request_test_asset_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_asset_list_api_view_with_access(self):
        self._create_test_asset()
        self.grant_access(
            obj=self.test_asset, permission=permission_asset_view
        )

        self._clear_events()

        response = self._request_test_asset_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_asset.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
