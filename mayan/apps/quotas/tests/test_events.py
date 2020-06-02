from actstream.models import Action

from mayan.apps.tests.tests.base import GenericViewTestCase

from ..events import event_quota_created, event_quota_edited
from ..permissions import permission_quota_create, permission_quota_edit

from .mixins import QuotaTestMixin, QuotaViewTestMixin


class QuotaEventsTestCase(QuotaTestMixin, QuotaViewTestMixin, GenericViewTestCase):
    def test_quota_created_event_no_permissions(self):
        Action.objects.all().delete()

        response = self._request_test_quota_create_view()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Action.objects.count(), 0)

    def test_quota_created_event_with_permissions(self):
        Action.objects.all().delete()

        self.grant_permission(permission=permission_quota_create)
        response = self._request_test_quota_create_view()
        self.assertEqual(response.status_code, 302)

        event = Action.objects.first()

        self.assertEqual(event.verb, event_quota_created.id)
        self.assertEqual(event.target, self.test_quota)
        self.assertEqual(event.actor, self._test_case_user)

    def test_quota_edited_event_no_permissions(self):
        self._create_test_quota()
        Action.objects.all().delete()

        response = self._request_test_quota_edit_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Action.objects.count(), 0)

    def test_quota_edited_event_with_access(self):
        self._create_test_quota()
        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_quota, permission=permission_quota_edit
        )

        response = self._request_test_quota_edit_view()
        self.assertEqual(response.status_code, 302)
        event = Action.objects.first()

        self.assertEqual(event.verb, event_quota_edited.id)
        self.assertEqual(event.target, self.test_quota)
        self.assertEqual(event.actor, self._test_case_user)
