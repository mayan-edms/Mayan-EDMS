from django.utils.encoding import force_text

from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_web_link_created, event_web_link_edited
from ..links import link_web_link_instance_view
from ..models import ResolvedWebLink, WebLink
from ..permissions import (
    permission_web_link_create, permission_web_link_delete,
    permission_web_link_edit, permission_web_link_view,
    permission_web_link_instance_view
)

from .literals import TEST_WEB_LINK_TEMPLATE
from .mixins import (
    DocumentTypeAddRemoveWebLinkViewTestMixin,
    WebLinkDocumentTypeViewTestMixin, WebLinkTestMixin, WebLinkViewTestMixin
)


class DocumentTypeAddRemoveWebLinkViewTestCase(
    DocumentTypeAddRemoveWebLinkViewTestMixin, WebLinkTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_web_link()

    def test_document_type_web_link_add_remove_get_view_no_permission(self):
        self.test_document_type.web_links.add(self.test_web_link)

        self._clear_events()

        response = self._request_test_document_type_web_link_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_web_link),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_web_link_add_remove_get_view_with_document_type_access(self):
        self.test_document_type.web_links.add(self.test_web_link)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_web_link_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=str(self.test_web_link),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_web_link_add_remove_get_view_with_web_link_access(self):
        self.test_document_type.web_links.add(self.test_web_link)

        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_web_link_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_web_link),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_web_link_add_remove_get_view_with_full_access(self):
        self.test_document_type.web_links.add(self.test_web_link)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_web_link_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_web_link),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_web_link_add_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_type_web_link_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_web_link not in self.test_document_type.web_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_web_link_add_view_with_document_type_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_web_link_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_web_link not in self.test_document_type.web_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_web_link_add_view_with_web_link_access(self):
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_web_link_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_web_link not in self.test_document_type.web_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_web_link_add_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_web_link_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_web_link in self.test_document_type.web_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_web_link)
        self.assertEqual(events[0].verb, event_web_link_edited.id)

    def test_document_type_web_link_remove_view_no_permission(self):
        self.test_document_type.web_links.add(self.test_web_link)

        self._clear_events()

        response = self._request_test_document_type_web_link_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_web_link in self.test_document_type.web_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_web_link_remove_view_with_document_type_access(self):
        self.test_document_type.web_links.add(self.test_web_link)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_web_link_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_web_link in self.test_document_type.web_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_web_link_remove_view_with_web_link_access(self):
        self.test_document_type.web_links.add(self.test_web_link)

        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_web_link_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_web_link in self.test_document_type.web_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_web_link_remove_view_with_full_access(self):
        self.test_document_type.web_links.add(self.test_web_link)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_document_type_web_link_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_web_link not in self.test_document_type.web_links.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_web_link)
        self.assertEqual(events[0].verb, event_web_link_edited.id)


class WebLinkViewTestCase(
    WebLinkTestMixin, WebLinkViewTestMixin, GenericViewTestCase
):
    def test_web_link_create_view_no_permission(self):
        web_link_count = WebLink.objects.count()

        self._clear_events()

        response = self._request_test_web_link_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(WebLink.objects.count(), web_link_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_create_view_with_permissions(self):
        self.grant_permission(permission=permission_web_link_create)

        web_link_count = WebLink.objects.count()

        self._clear_events()

        response = self._request_test_web_link_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WebLink.objects.count(), web_link_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_web_link)
        self.assertEqual(events[0].verb, event_web_link_created.id)

    def test_web_link_delete_view_no_permission(self):
        self._create_test_web_link()

        web_link_count = WebLink.objects.count()

        self._clear_events()

        response = self._request_test_web_link_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(WebLink.objects.count(), web_link_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_delete_view_with_access(self):
        self._create_test_web_link()

        self.grant_access(
            obj=self.test_web_link, permission=permission_web_link_delete
        )

        web_link_count = WebLink.objects.count()

        self._clear_events()

        response = self._request_test_web_link_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WebLink.objects.count(), web_link_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_edit_view_no_permission(self):
        self._create_test_web_link()

        web_link_label = self.test_web_link.label

        self._clear_events()

        response = self._request_test_web_link_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_web_link.refresh_from_db()
        self.assertEqual(self.test_web_link.label, web_link_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_edit_view_with_access(self):
        self._create_test_web_link()

        self.grant_access(
            obj=self.test_web_link, permission=permission_web_link_edit
        )

        web_link_label = self.test_web_link.label

        self._clear_events()

        response = self._request_test_web_link_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_web_link.refresh_from_db()
        self.assertNotEqual(self.test_web_link.label, web_link_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_web_link)
        self.assertEqual(events[0].verb, event_web_link_edited.id)

    def test_web_link_list_view_with_no_permission(self):
        self._create_test_web_link()

        self._clear_events()

        response = self._request_test_web_link_list_view()
        self.assertNotContains(
            response=response, text=self.test_web_link.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_list_view_with_access(self):
        self._create_test_web_link()

        self.grant_access(obj=self.test_web_link, permission=permission_web_link_view)

        self._clear_events()

        response = self._request_test_web_link_list_view()
        self.assertContains(
            response=response, text=self.test_web_link.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class WebLinkDocumentTypeViewTestCase(
    WebLinkDocumentTypeViewTestMixin, WebLinkTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_web_link()

    def test_web_link_document_type_add_remove_get_view_no_permission(self):
        self.test_web_link.document_types.add(self.test_document_type)

        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self._clear_events()

        response = self._request_test_web_link_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_web_link),
            status_code=404
        )

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_document_type_add_remove_get_view_with_document_type_access(self):
        self.test_web_link.document_types.add(self.test_document_type)

        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_web_link),
            status_code=404
        )

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_document_type_add_remove_get_view_with_web_link_access(self):
        self.test_web_link.document_types.add(self.test_document_type)

        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_web_link),
            status_code=200
        )

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_document_type_add_remove_get_view_with_full_access(self):
        self.test_web_link.document_types.add(self.test_document_type)

        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_web_link),
            status_code=200
        )

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_document_type_add_view_no_permission(self):
        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_document_type_add_view_with_document_type_access(self):
        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_document_type_add_view_with_web_link_access(self):
        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_web_link, permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_document_type_add_view_with_full_access(self):
        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_web_link, permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_web_link)
        self.assertEqual(events[0].verb, event_web_link_edited.id)

    def test_web_link_document_type_remove_view_no_permission(self):
        self.test_web_link.document_types.add(self.test_document_type)

        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_document_type_remove_view_with_document_type_access(self):
        self.test_web_link.document_types.add(self.test_document_type)

        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_document_type_remove_view_with_web_link_access(self):
        self.test_web_link.document_types.add(self.test_document_type)

        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_web_link, permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_web_link_document_type_remove_view_with_full_access(self):
        self.test_web_link.document_types.add(self.test_document_type)

        test_web_link_document_type_count = self.test_web_link.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_web_link, permission=permission_web_link_edit
        )

        self._clear_events()

        response = self._request_test_web_link_document_type_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_web_link.document_types.count(),
            test_web_link_document_type_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_web_link)
        self.assertEqual(events[0].verb, event_web_link_edited.id)


class DocumentWebLinkViewTestCase(
    WebLinkTestMixin, WebLinkViewTestMixin, GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_web_link(add_test_document_type=True)

    def test_document_web_links_list_view_no_permission(self):
        response = self._request_test_document_web_link_list_view()
        self.assertNotContains(
            response=response, text=force_text(s=self.test_document),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=force_text(s=self.test_web_link),
            status_code=404
        )

    def test_document_web_links_list_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )

        response = self._request_test_document_web_link_list_view()
        self.assertContains(
            response=response, text=force_text(s=self.test_document),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=force_text(s=self.test_web_link),
            status_code=200
        )

    def test_document_web_links_list_view_with_web_link_access(self):
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )

        response = self._request_test_document_web_link_list_view()
        self.assertNotContains(
            response=response, text=force_text(s=self.test_document),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=force_text(s=self.test_web_link),
            status_code=404
        )

    def test_document_web_links_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )

        response = self._request_test_document_web_link_list_view()
        self.assertContains(
            response=response, text=force_text(s=self.test_document),
            status_code=200
        )
        self.assertContains(
            response=response, text=force_text(s=self.test_web_link),
            status_code=200
        )
        # Test if a valid resolved link navigate link is present.
        # Ensures the view is returning ResolvedWebLink proxies and not the
        # base model WebLink.
        context = self._get_context_from_test_response(response=response)
        context['object'] = ResolvedWebLink.objects.get_for(
            document=self.test_document, user=self._test_case_user
        ).first()
        resolved_web_link_link = link_web_link_instance_view.resolve(context=context)
        self.assertContains(
            response=response, text=resolved_web_link_link.url,
            status_code=200
        )

    def test_trashed_document_web_links_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )

        self.test_document.delete()

        response = self._request_test_document_web_link_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_resolved_web_link_view_no_permission(self):
        response = self._request_test_document_web_link_instance_view()
        self.assertEqual(response.status_code, 404)

    def test_document_resolved_web_link_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )

        response = self._request_test_document_web_link_instance_view()
        self.assertEqual(response.status_code, 404)

    def test_document_resolved_web_link_view_with_web_link_access(self):
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )

        response = self._request_test_document_web_link_instance_view()
        self.assertEqual(response.status_code, 404)

    def test_document_resolved_web_link_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )

        response = self._request_test_document_web_link_instance_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, TEST_WEB_LINK_TEMPLATE.replace(
                '{{ document.uuid }}', force_text(s=self.test_document.uuid)
            )
        )

    def test_trashed_document_resolved_web_link_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_web_link_instance_view
        )
        self.grant_access(
            obj=self.test_web_link,
            permission=permission_web_link_instance_view
        )

        self.test_document.delete()

        response = self._request_test_document_web_link_instance_view()
        self.assertEqual(response.status_code, 404)
