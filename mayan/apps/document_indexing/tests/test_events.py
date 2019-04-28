from __future__ import unicode_literals

from actstream.models import Action

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.documents.tests import DocumentTestMixin

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
        self._request_test_index_create_view()

        self.assertEqual(Action.objects.last().actor, self._test_case_user)
        self.assertEqual(Action.objects.last().target, self.test_index)
        self.assertEqual(
            Action.objects.last().verb, event_index_template_created.id
        )

    def test_index_template_edit_event(self):
        self._create_test_index()

        self.grant_access(
            obj=self.test_index, permission=permission_document_indexing_edit
        )
        Action.objects.all().delete()

        self._request_test_index_edit_view()

        self.assertEqual(Action.objects.last().target, self.test_index)
        self.assertEqual(
            Action.objects.last().verb, event_index_template_edited.id
        )
