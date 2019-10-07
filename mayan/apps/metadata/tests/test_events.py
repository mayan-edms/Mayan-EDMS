from __future__ import unicode_literals

from actstream.models import Action

from mayan.apps.common.tests.base import GenericViewTestCase

from ..events import (
    event_metadata_type_created, event_metadata_type_edited
)
from ..models import MetadataType
from ..permissions import (
    permission_metadata_type_create, permission_metadata_type_edit
)

from .mixins import MetadataTypeTestMixin, MetadataTypeViewTestMixin


class MetadataTypeEventsTestCase(
    MetadataTypeTestMixin, MetadataTypeViewTestMixin, GenericViewTestCase
):
    def test_metadata_type_create_event_no_permissions(self):
        Action.objects.all().delete()

        response = self._request_test_metadata_type_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Action.objects.count(), 0)

    def test_metadata_type_create_event_with_permissions(self):
        Action.objects.all().delete()

        self.grant_permission(permission=permission_metadata_type_create)

        response = self._request_test_metadata_type_create_view()
        self.assertEqual(response.status_code, 302)

        event = Action.objects.first()

        metadata_type = MetadataType.objects.first()

        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, metadata_type)
        self.assertEqual(event.verb, event_metadata_type_created.id)

    def test_metadata_type_edit_event_no_permissions(self):
        self._create_test_metadata_type()

        Action.objects.all().delete()

        response = self._request_test_metadata_type_edit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Action.objects.count(), 0)

    def test_metadata_type_edit_event_with_access(self):
        self._create_test_metadata_type()

        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_metadata_type, permission=permission_metadata_type_edit
        )

        response = self._request_test_metadata_type_edit_view()

        self.assertEqual(response.status_code, 302)

        event = Action.objects.first()

        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_metadata_type)
        self.assertEqual(event.verb, event_metadata_type_edited.id)
