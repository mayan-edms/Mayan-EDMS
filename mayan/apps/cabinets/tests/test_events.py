from actstream.models import Action

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import (
    event_cabinet_created, event_cabinet_edited, event_cabinet_document_added,
    event_cabinet_document_removed
)
from ..models import Cabinet
from ..permissions import permission_cabinet_create, permission_cabinet_edit

from .mixins import CabinetTestMixin, CabinetViewTestMixin


class CabinetsEventsTestCase(
    CabinetTestMixin, CabinetViewTestMixin, GenericViewTestCase
):
    def test_cabinet_create_event_no_permission(self):
        action_count = Action.objects.count()

        response = self._request_test_cabinet_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Action.objects.count(), action_count)

    def test_cabinet_create_event_with_permissions(self):
        self.grant_permission(permission=permission_cabinet_create)

        action_count = Action.objects.count()

        response = self._request_test_cabinet_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Action.objects.count(), action_count + 1)

        event = Action.objects.first()

        cabinet = Cabinet.objects.first()

        self.assertEqual(event.verb, event_cabinet_created.id)
        self.assertEqual(event.target, cabinet)
        self.assertEqual(event.actor, self._test_case_user)

    def test_cabinet_edit_event_no_permission(self):
        self._create_test_cabinet()

        action_count = Action.objects.count()

        response = self._request_test_cabinet_edit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Action.objects.count(), action_count)

    def test_cabinet_edit_event_with_access(self):
        self._create_test_cabinet()

        self.grant_access(
            obj=self.test_cabinet, permission=permission_cabinet_edit
        )

        action_count = Action.objects.count()

        response = self._request_test_cabinet_edit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Action.objects.count(), action_count + 1)

        event = Action.objects.first()

        self.assertEqual(event.verb, event_cabinet_edited.id)
        self.assertEqual(event.target, self.test_cabinet)
        self.assertEqual(event.actor, self._test_case_user)


class CabinetDocumentsEventsTestCase(
    CabinetTestMixin, CabinetViewTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_cabinet_add_event(self):
        self._create_test_cabinet()

        Action.objects.all().delete()
        self.test_cabinet.document_add(document=self.test_document)

        self.assertEqual(Action.objects.last().target, self.test_document)
        self.assertEqual(
            Action.objects.last().verb,
            event_cabinet_document_added.id
        )

    def test_document_cabinet_remove_event(self):
        self._create_test_cabinet()

        self.test_cabinet.document_add(document=self.test_document)
        Action.objects.all().delete()
        self.test_cabinet.document_remove(document=self.test_document)

        self.assertEqual(Action.objects.first().target, self.test_document)
        self.assertEqual(
            Action.objects.first().verb,
            event_cabinet_document_removed.id
        )
