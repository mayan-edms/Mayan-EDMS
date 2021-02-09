from actstream.models import Action

from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_role_created, event_role_edited
from ..permissions import permission_role_create, permission_role_edit

from .mixins import RoleTestMixin, RoleViewTestMixin


class RoleEventsTestCase(RoleTestMixin, RoleViewTestMixin, GenericViewTestCase):
    def test_role_created_event_no_permission(self):
        Action.objects.all().delete()

        response = self._request_test_role_create_view()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Action.objects.count(), 0)

    def test_role_created_event_with_permissions(self):
        Action.objects.all().delete()

        self.grant_permission(permission=permission_role_create)
        response = self._request_test_role_create_view()
        self.assertEqual(response.status_code, 302)

        event = Action.objects.first()

        self.assertEqual(event.verb, event_role_created.id)
        self.assertEqual(event.target, self.test_role)
        self.assertEqual(event.actor, self._test_case_user)

    def test_role_edited_event_no_permission(self):
        self._create_test_role()
        Action.objects.all().delete()

        response = self._request_test_role_edit_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Action.objects.count(), 0)

    def test_role_edited_event_with_access(self):
        self._create_test_role()
        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_role, permission=permission_role_edit
        )

        response = self._request_test_role_edit_view()
        self.assertEqual(response.status_code, 302)
        event = Action.objects.first()

        self.assertEqual(event.verb, event_role_edited.id)
        self.assertEqual(event.target, self.test_role)
        self.assertEqual(event.actor, self._test_case_user)
