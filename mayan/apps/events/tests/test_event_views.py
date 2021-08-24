from django.contrib.contenttypes.models import ContentType

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..permissions import permission_events_view

from .mixins import (
    EventTestMixin, EventTypeTestMixin, EventViewTestMixin,
    UserEventViewsTestMixin
)


class EventsViewTestCase(
    EventTestMixin, EventTypeTestMixin, EventViewTestMixin,
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

    def test_event_list_view_no_permission(self):
        self._create_test_event(target=self.test_object)

        response = self._request_test_events_list_view()

        self.assertNotContains(
            response=response, status_code=200,
            text=str(self.test_event_type)
        )

    def test_event_list_view_with_access(self):
        self._create_test_event(target=self.test_object)

        self.grant_access(
            obj=self.test_object, permission=permission_events_view
        )

        response = self._request_test_events_list_view()

        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_event_type)
        )

    def test_events_for_object_view_no_permission(self):
        self._create_test_event(
            actor=self.test_user, action_object=self.test_object
        )

        response = self._request_events_for_object_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=str(self.test_event_type)
        )

    def test_events_for_object_view_with_access(self):
        self._create_test_event(
            actor=self.test_user, action_object=self.test_object
        )

        self.grant_access(
            obj=self.test_object, permission=permission_events_view
        )

        response = self._request_events_for_object_view()
        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_event_type)
        )

    def test_events_by_verb_view_no_permission(self):
        self._create_test_event(
            actor=self.test_user, action_object=self.test_object
        )

        response = self._request_test_events_by_verb_view()
        self.assertContains(
            count=3, response=response, status_code=200,
            text=str(self.test_event_type)
        )

    def test_events_by_verb_view_with_access(self):
        self._create_test_event(
            actor=self.test_user, action_object=self.test_object
        )

        self.grant_access(
            obj=self.test_object, permission=permission_events_view
        )

        response = self._request_test_events_by_verb_view()
        self.assertContains(
            count=4, response=response, status_code=200,
            text=str(self.test_event_type)
        )

    def test_current_user_events_view_no_permission(self):
        self._create_test_event(
            actor=self._test_case_user, action_object=self.test_object
        )

        response = self._request_test_current_user_events_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=str(self.test_event_type)
        )

    def test_current_user_events_view_with_access(self):
        self._create_test_event(
            actor=self._test_case_user, action_object=self.test_object
        )

        self.grant_access(
            obj=self.test_object, permission=permission_events_view
        )

        response = self._request_test_current_user_events_view()
        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_event_type)
        )


class UserEventViewsTestCase(UserEventViewsTestMixin, GenericViewTestCase):
    def test_user_event_type_subscription_list_view(self):
        response = self._request_test_user_event_type_subscription_list_view()
        self.assertEqual(response.status_code, 200)
