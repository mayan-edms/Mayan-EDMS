from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_smart_link_created, event_smart_link_edited
from ..models import SmartLink
from ..permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)

from .literals import TEST_SMART_LINK_LABEL, TEST_SMART_LINK_LABEL_EDITED
from .mixins import (
    DocumentTypeAddRemoveSmartLinkViewTestMixin,
    SmartLinkDocumentTypeViewTestMixin, SmartLinkTestMixin,
    SmartLinkViewTestMixin
)


class DocumentTypeAddRemoveSmartLinkViewTestCase(
    DocumentTypeAddRemoveSmartLinkViewTestMixin, SmartLinkTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_smart_link()

    def test_document_type_smart_link_add_remove_get_view_no_permission(self):
        self.test_document_type.smart_links.add(self.test_smart_link)

        self._clear_events()

        response = self._request_test_document_type_smart_link_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_smart_link),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_smart_link_add_remove_get_view_with_document_type_access(self):
        self.test_document_type.smart_links.add(self.test_smart_link)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_smart_link_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=str(self.test_smart_link),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_smart_link_add_remove_get_view_with_smart_link_access(self):
        self.test_document_type.smart_links.add(self.test_smart_link)

        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_smart_link_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_smart_link),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_smart_link_add_remove_get_view_with_full_access(self):
        self.test_document_type.smart_links.add(self.test_smart_link)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_smart_link_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_smart_link),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_smart_link_add_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_type_smart_link_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_smart_link not in self.test_document_type.smart_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_smart_link_add_view_with_document_type_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_smart_link_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_smart_link not in self.test_document_type.smart_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_smart_link_add_view_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_smart_link_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_smart_link not in self.test_document_type.smart_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_smart_link_add_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_smart_link_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_smart_link in self.test_document_type.smart_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_document_type_smart_link_remove_view_no_permission(self):
        self.test_document_type.smart_links.add(self.test_smart_link)

        self._clear_events()

        response = self._request_test_document_type_smart_link_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_smart_link in self.test_document_type.smart_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_smart_link_remove_view_with_document_type_access(self):
        self.test_document_type.smart_links.add(self.test_smart_link)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_smart_link_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_smart_link in self.test_document_type.smart_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_smart_link_remove_view_with_smart_link_access(self):
        self.test_document_type.smart_links.add(self.test_smart_link)

        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_smart_link_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_smart_link in self.test_document_type.smart_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_smart_link_remove_view_with_full_access(self):
        self.test_document_type.smart_links.add(self.test_smart_link)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_smart_link_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_smart_link not in self.test_document_type.smart_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)


class SmartLinkViewTestCase(
    SmartLinkTestMixin, SmartLinkViewTestMixin, GenericViewTestCase
):
    def test_smart_link_create_view_no_permission(self):
        self._clear_events()

        response = self._request_test_smart_link_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(SmartLink.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_create_view_with_permission(self):
        self.grant_permission(permission=permission_smart_link_create)

        self._clear_events()

        response = self._request_test_smart_link_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(SmartLink.objects.count(), 1)
        self.assertEqual(
            SmartLink.objects.first().label, TEST_SMART_LINK_LABEL
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_created.id)

    def test_smart_link_delete_view_no_permission(self):
        self._create_test_smart_link()

        self._clear_events()

        response = self._request_test_smart_link_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(SmartLink.objects.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_delete_view_with_access(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_delete
        )

        self._clear_events()

        response = self._request_test_smart_link_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(SmartLink.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_edit_view_no_permission(self):
        self._create_test_smart_link()

        self._clear_events()

        response = self._request_test_smart_link_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_smart_link.refresh_from_db()
        self.assertEqual(self.test_smart_link.label, TEST_SMART_LINK_LABEL)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_edit_view_with_access(self):
        self._create_test_smart_link()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_smart_link.refresh_from_db()
        self.assertEqual(
            self.test_smart_link.label, TEST_SMART_LINK_LABEL_EDITED
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_list_view_no_permission(self):
        self._create_test_smart_link()

        self._clear_events()

        response = self._request_test_smart_link_list_view()
        self.assertNotContains(
            response=response, text=str(self.test_smart_link), status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_list_view_with_access(self):
        self._create_test_smart_link()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )

        self._clear_events()

        response = self._request_test_smart_link_list_view()
        self.assertContains(
            response=response, text=str(self.test_smart_link), status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class SmartLinkDocumentTypeViewTestCase(
    SmartLinkDocumentTypeViewTestMixin, SmartLinkTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_smart_link()

    def test_smart_link_document_type_add_remove_get_view_no_permission(self):
        self.test_smart_link.document_types.add(self.test_document_type)

        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_smart_link),
            status_code=404
        )

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_add_remove_get_view_with_document_type_access(self):
        self.test_smart_link.document_types.add(self.test_document_type)

        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_smart_link),
            status_code=404
        )

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_add_remove_get_view_with_smart_link_access(self):
        self.test_smart_link.document_types.add(self.test_document_type)

        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_smart_link),
            status_code=200
        )

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_add_remove_get_view_with_full_access(self):
        self.test_smart_link.document_types.add(self.test_document_type)

        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_smart_link),
            status_code=200
        )

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_add_view_no_permission(self):
        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_add_view_with_document_type_access(self):
        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_add_view_with_smart_link_access(self):
        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_add_view_with_full_access(self):
        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_document_type_remove_view_no_permission(self):
        self.test_smart_link.document_types.add(self.test_document_type)

        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_remove_view_with_document_type_access(self):
        self.test_smart_link.document_types.add(self.test_document_type)

        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_remove_view_with_smart_link_access(self):
        self.test_smart_link.document_types.add(self.test_document_type)

        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_remove_view_with_full_access(self):
        self.test_smart_link.document_types.add(self.test_document_type)

        test_smart_link_document_type_count = self.test_smart_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_type_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)
