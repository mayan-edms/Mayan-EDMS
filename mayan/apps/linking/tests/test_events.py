from __future__ import unicode_literals

from actstream.models import Action

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.documents.tests import DocumentTestMixin

from ..permissions import (
    permission_smart_link_create, permission_smart_link_edit,
)

from ..events import event_smart_link_created, event_smart_link_edited

from .mixins import SmartLinkTestMixin, SmartLinkViewTestMixin


class SmartLinkTemplateEventsTestCase(DocumentTestMixin, SmartLinkTestMixin, SmartLinkViewTestMixin, GenericViewTestCase):
    auto_upload_document = False

    def test_smart_link_create_event(self):
        self.grant_permission(
            permission=permission_smart_link_create
        )
        Action.objects.all().delete()

        response = self._request_test_smart_link_create_view()
        self.assertEqual(response.status_code, 302)

        action = Action.objects.last()

        self.assertEqual(action.actor, self._test_case_user)
        self.assertEqual(action.target, self.test_smart_link)
        self.assertEqual(action.verb, event_smart_link_created.id)

    def test_smart_link_edit_event(self):
        self._create_test_smart_link()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )
        Action.objects.all().delete()

        response = self._request_test_smart_link_edit_view()
        self.assertEqual(response.status_code, 302)

        action = Action.objects.last()

        self.assertEqual(action.actor, self._test_case_user)
        self.assertEqual(action.target, self.test_smart_link)
        self.assertEqual(action.verb, event_smart_link_edited.id)
