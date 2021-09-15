from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_smart_link_edited
from ..permissions import permission_smart_link_edit

from .mixins import (
    SmartLinkConditionViewTestMixin, SmartLinkTestMixin,
    SmartLinkViewTestMixin
)


class SmartLinkConditionViewTestCase(
    SmartLinkConditionViewTestMixin, SmartLinkTestMixin,
    SmartLinkViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_smart_link()

    def test_smart_link_condition_create_view_no_permission(self):
        condition_count = self.test_smart_link.conditions.count()

        self._clear_events()

        response = self._request_test_smart_link_condition_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_smart_link.conditions.count(), condition_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_create_view_with_access(self):
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        condition_count = self.test_smart_link.conditions.count()

        self._clear_events()

        response = self._request_test_smart_link_condition_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_smart_link.conditions.count(), condition_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_smart_link_condition
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_condition_delete_view_no_permission(self):
        self._create_test_smart_link_condition()
        condition_count = self.test_smart_link.conditions.count()

        self._clear_events()

        response = self._request_test_smart_link_condition_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_smart_link.conditions.count(), condition_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_delete_view_with_access(self):
        self._create_test_smart_link_condition()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )
        condition_count = self.test_smart_link.conditions.count()

        self._clear_events()

        response = self._request_test_smart_link_condition_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_smart_link.conditions.count(), condition_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_condition_edit_view_no_permission(self):
        self._create_test_smart_link_condition()
        instance_values = self._model_instance_to_dictionary(
            instance=self.test_smart_link_condition
        )

        self._clear_events()

        response = self._request_test_smart_link_condition_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_smart_link_condition.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_smart_link_condition
            ), instance_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_edit_view_with_access(self):
        self._create_test_smart_link_condition()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )
        instance_values = self._model_instance_to_dictionary(
            instance=self.test_smart_link_condition
        )

        self._clear_events()

        response = self._request_test_smart_link_condition_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_smart_link_condition.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_smart_link_condition
            ), instance_values
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_smart_link_condition
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_condition_list_view_no_permission(self):
        self._create_test_smart_link_condition()

        self._clear_events()

        response = self._request_test_smart_link_condition_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self.test_smart_link_condition.smart_link.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_list_view_with_access(self):
        self._create_test_smart_link_condition()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_condition_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_smart_link_condition.smart_link.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
