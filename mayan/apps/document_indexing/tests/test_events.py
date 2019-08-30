from __future__ import unicode_literals

from actstream.models import Action

from mayan.apps.common.tests.base import GenericViewTestCase
from mayan.apps.documents.tests.mixins import DocumentTestMixin

from ..permissions import (
    permission_document_indexing_create, permission_document_indexing_edit,
)

from ..events import event_index_template_created, event_index_template_edited

from .mixins import IndexTestMixin, IndexViewTestMixin


class IndexTemplateEventsTestCase(DocumentTestMixin, IndexTestMixin, IndexViewTestMixin, GenericViewTestCase):
    auto_upload_document = False

    def test_index_template_create_event(self):
        Action.objects.all().delete()

        self.grant_permission(
            permission=permission_document_indexing_create
        )
        response = self._request_test_index_create_view()
        self.assertEqual(response.status_code, 302)

        action = Action.objects.last()

        self.assertEqual(action.actor, self._test_case_user)
        self.assertEqual(action.target, self.test_index)
        self.assertEqual(action.verb, event_index_template_created.id)

    def test_index_template_edit_event(self):
        self._create_test_index()

        self.grant_access(
            obj=self.test_index, permission=permission_document_indexing_edit
        )
        Action.objects.all().delete()

        response = self._request_test_index_edit_view()
        self.assertEqual(response.status_code, 302)

        action = Action.objects.last()

        self.assertEqual(action.actor, self._test_case_user)
        self.assertEqual(action.target, self.test_index)
        self.assertEqual(action.verb, event_index_template_edited.id)
