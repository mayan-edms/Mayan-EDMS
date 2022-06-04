from mayan.apps.acls.classes import ModelPermission
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..permissions import permission_events_view

from .mixins import (
    EventObjectTestMixin, EventTypeTestMixin,
    ObjectEventSubscriptionTestMixin, UserEventViewTestMixin,
    UserObjectSubscriptionViewTestMixin
)


class UserEventTypeSubscriptionViewTestCase(
    UserEventViewTestMixin, GenericViewTestCase
):
    def test_user_event_type_subscription_list_view_no_permission(self):
        response = self._request_test_user_event_type_subscription_list_view()
        self.assertEqual(response.status_code, 200)


class UserObjectSubscriptionViewTestCase(
    EventObjectTestMixin, EventTypeTestMixin,
    ObjectEventSubscriptionTestMixin, UserObjectSubscriptionViewTestMixin,
    GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_event_type()
        self._create_test_object_with_event_type_and_permission()

        self._create_test_object_event_subscription()
        ModelPermission.register(
            model=self.TestModel, permissions=(
                permission_events_view,
            )
        )

    def test_user_event_type_subscription_list_view_no_permission(self):
        response = self._request_user_object_subscription_list_view()
        self.assertNotContains(
            response=response, text=self._test_event_type.label,
            status_code=200
        )
        self.assertNotContains(
            response=response, text=str(self._test_object),
            status_code=200
        )

    def test_user_event_type_subscription_list_view_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_events_view
        )
        response = self._request_user_object_subscription_list_view()
        self.assertContains(
            response=response, text=self._test_event_type.label,
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self._test_object),
            status_code=200
        )
