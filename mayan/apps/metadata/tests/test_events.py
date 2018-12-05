from __future__ import unicode_literals

from actstream.models import Action

from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..events import (
    event_metadata_type_created, event_metadata_type_edited
)
from ..models import MetadataType
from ..permissions import (
    permission_metadata_type_create, permission_metadata_type_edit
)

from .mixins import MetadataTestsMixin


class MetadataTypeEventsTestCase(MetadataTestsMixin, GenericDocumentViewTestCase):
    def test_metadata_type_create_event_no_permissions(self):
        self.login_user()

        Action.objects.all().delete()

        response = self._request_metadata_type_create_view()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Action.objects.count(), 0)

    def test_metadata_type_create_event_with_permissions(self):
        self.login_user()

        Action.objects.all().delete()

        self.grant_permission(permission=permission_metadata_type_create)

        response = self._request_metadata_type_create_view()

        self.assertEqual(response.status_code, 302)

        event = Action.objects.first()

        metadata_type = MetadataType.objects.first()

        self.assertEqual(event.verb, event_metadata_type_created.id)
        self.assertEqual(event.target, metadata_type)
        self.assertEqual(event.actor, self.user)

    def test_metadata_type_edit_event_no_permissions(self):
        self._create_metadata_type()

        self.login_user()

        Action.objects.all().delete()

        response = self._request_metadata_type_edit_view()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Action.objects.count(), 0)

    def test_metadata_type_edit_event_with_access(self):
        self._create_metadata_type()

        self.login_user()

        Action.objects.all().delete()

        self.grant_access(
            permission=permission_metadata_type_edit, obj=self.metadata_type
        )

        response = self._request_metadata_type_edit_view()

        self.assertEqual(response.status_code, 302)

        event = Action.objects.first()

        self.assertEqual(event.verb, event_metadata_type_edited.id)
        self.assertEqual(event.target, self.metadata_type)
        self.assertEqual(event.actor, self.user)
