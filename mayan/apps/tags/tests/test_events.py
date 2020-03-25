from actstream.models import Action

from mayan.apps.common.tests.base import GenericViewTestCase

from ..events import event_tag_created, event_tag_edited
from ..models import Tag
from ..permissions import permission_tag_create, permission_tag_edit

from .mixins import TagTestMixin, TagViewTestMixin


class TagEventsTestCase(TagTestMixin, TagViewTestMixin, GenericViewTestCase):
    def test_tag_create_event_no_permissions(self):
        action_count = Action.objects.count()

        response = self._request_test_tag_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Action.objects.count(), action_count)

    def test_tag_create_event_with_permissions(self):
        self.grant_permission(permission=permission_tag_create)

        action_count = Action.objects.count()

        response = self._request_test_tag_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Action.objects.count(), action_count + 1)

        event = Action.objects.first()

        tag = Tag.objects.first()

        self.assertEqual(event.verb, event_tag_created.id)
        self.assertEqual(event.target, tag)
        self.assertEqual(event.actor, self._test_case_user)

    def test_tag_edit_event_no_permissions(self):
        self._create_test_tag()

        action_count = Action.objects.count()

        response = self._request_test_tag_edit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Action.objects.count(), action_count)

    def test_tag_edit_event_with_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self.test_tag, permission=permission_tag_edit
        )

        action_count = Action.objects.count()

        response = self._request_test_tag_edit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Action.objects.count(), action_count + 1)

        event = Action.objects.first()

        self.assertEqual(event.verb, event_tag_edited.id)
        self.assertEqual(event.target, self.test_tag)
        self.assertEqual(event.actor, self._test_case_user)
