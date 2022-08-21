from django.core.exceptions import ValidationError

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.testing.tests.base import BaseTestCase

from ..events import (
    event_cabinet_created, event_cabinet_edited,
    event_cabinet_document_added, event_cabinet_document_removed
)
from ..models import Cabinet

from .literals import TEST_CABINET_LABEL, TEST_CABINET_LABEL_EDITED
from .mixins import CabinetTestMixin


class CabinetTestCase(CabinetTestMixin, BaseTestCase):
    def test_cabinet_creation(self):
        self._clear_events()

        self._create_test_cabinet()

        self.assertEqual(Cabinet.objects.all().count(), 1)
        self.assertQuerysetEqual(
            Cabinet.objects.all(), (repr(self._test_cabinet),)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_cabinet)
        self.assertEqual(events[0].target, self._test_cabinet)
        self.assertEqual(events[0].verb, event_cabinet_created.id)

    def test_cabinet_duplicate_creation(self):
        self._create_test_cabinet()

        self._clear_events()

        with self.assertRaises(expected_exception=ValidationError):
            cabinet_2 = Cabinet(label=TEST_CABINET_LABEL)
            cabinet_2.validate_unique()
            cabinet_2.save()

        self.assertEqual(Cabinet.objects.all().count(), 1)
        self.assertQuerysetEqual(
            Cabinet.objects.all(), (repr(self._test_cabinet),)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_cabinet_editing(self):
        self._create_test_cabinet()

        self._clear_events()

        test_cabinet_label = self._test_cabinet.label

        self._test_cabinet.label = TEST_CABINET_LABEL_EDITED
        self._test_cabinet.save()

        self.assertNotEqual(self._test_cabinet.label, test_cabinet_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_cabinet)
        self.assertEqual(events[0].target, self._test_cabinet)
        self.assertEqual(events[0].verb, event_cabinet_edited.id)

    def test_inner_cabinet_creation(self):
        self._create_test_cabinet()

        test_cabinet_count = Cabinet.objects.count()

        self._clear_events()

        inner_cabinet = Cabinet.objects.create(
            parent=self._test_cabinet, label=TEST_CABINET_LABEL
        )

        self.assertEqual(Cabinet.objects.count(), test_cabinet_count + 1)
        self.assertQuerysetEqual(
            Cabinet.objects.all(),
            map(repr, (self._test_cabinet, inner_cabinet))
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, inner_cabinet)
        self.assertEqual(events[0].target, inner_cabinet)
        self.assertEqual(events[0].verb, event_cabinet_created.id)

    def test_method_get_absolute_url(self):
        self._create_test_cabinet()

        self._clear_events()

        self.assertTrue(self._test_cabinet.get_absolute_url())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class CabinetDocumentTestCase(
    CabinetTestMixin, DocumentTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_cabinet()

    def test_addition_of_documents(self):
        test_cabinet_document_count = self._test_cabinet.documents.count()

        self._clear_events()

        self._test_cabinet.document_add(document=self._test_document)

        self.assertEqual(
            self._test_cabinet.documents.count(),
            test_cabinet_document_count + 1
        )
        self.assertQuerysetEqual(
            self._test_cabinet.documents.all(), (repr(self._test_document),)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_cabinet)
        self.assertEqual(events[0].actor, self._test_document)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_cabinet_document_added.id)

    def test_addition_and_deletion_of_documents(self):
        self._test_cabinet.document_add(document=self._test_document)

        test_cabinet_document_count = self._test_cabinet.documents.count()

        self._clear_events()

        self._test_cabinet.document_remove(document=self._test_document)

        self.assertEqual(
            self._test_cabinet.documents.count(),
            test_cabinet_document_count - 1
        )
        self.assertQuerysetEqual(self._test_cabinet.documents.all(), ())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_cabinet)
        self.assertEqual(events[0].actor, self._test_document)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_cabinet_document_removed.id)

    def test_cabinet_get_document_count_method(self):
        self._test_cabinet.document_add(document=self._test_document)

        test_cabinet_document_count = self._test_cabinet.documents.count()

        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        self.assertEqual(
            self._test_cabinet.get_document_count(user=self._test_case_user),
            test_cabinet_document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_cabinet_document_count_method(self):
        self._test_cabinet.document_add(document=self._test_document)

        test_cabinet_document_count = self._test_cabinet.documents.count()

        self._test_document.delete()

        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        self.assertEqual(
            self._test_cabinet.get_document_count(user=self._test_case_user),
            test_cabinet_document_count - 1,
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
