from django.utils.encoding import force_text

from mayan.apps.events.classes import EventModelRegistry
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_acl_created, event_acl_deleted, event_acl_edited
from ..models import AccessControlList
from ..permissions import permission_acl_edit, permission_acl_view

from .mixins import ACLTestMixin, AccessControlListViewTestMixin


class AccessControlListViewTestCase(
    AccessControlListViewTestMixin, ACLTestMixin, GenericViewTestCase
):
    def test_acl_create_get_view_no_permission(self):
        self._create_acl_test_object()

        acl_count = AccessControlList.objects.count()

        self._clear_events()

        response = self._request_test_acl_create_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(AccessControlList.objects.count(), acl_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_create_get_view_with_access(self):
        self._create_acl_test_object()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )
        acl_count = AccessControlList.objects.count()

        self._clear_events()

        response = self._request_test_acl_create_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(AccessControlList.objects.count(), acl_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_create_view_post_no_permission(self):
        self._create_acl_test_object()

        acl_count = AccessControlList.objects.count()

        self._clear_events()

        response = self._request_test_acl_create_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(AccessControlList.objects.count(), acl_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_create_view_post_with_access(self):
        self._create_acl_test_object()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        acl_count = AccessControlList.objects.count()

        self._clear_events()

        response = self._request_test_acl_create_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(AccessControlList.objects.count(), acl_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_object)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_acl)
        self.assertEqual(events[0].verb, event_acl_created.id)

    def test_acl_delete_view_no_permission(self):
        self._create_acl_test_object()

        self._create_test_acl()

        self._clear_events()

        response = self._request_test_acl_delete_view()
        self.assertNotContains(
            response=response, text=force_text(s=self.test_object),
            status_code=404
        )

        self.assertTrue(
            self.test_object.acls.filter(role=self.test_role).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_delete_view_with_access(self):
        self._create_acl_test_object()

        self._create_test_acl()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        self._clear_events()

        response = self._request_test_acl_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            self.test_object.acls.filter(role=self.test_role).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_object)
        self.assertEqual(events[0].verb, event_acl_deleted.id)

    def test_acl_list_view_no_permission(self):
        self._create_acl_test_object()

        self._create_test_acl()

        self._clear_events()

        response = self._request_test_acl_list_view()
        self.assertNotContains(
            response=response, text=force_text(s=self.test_object),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_list_view_with_access(self):
        self._create_acl_test_object()

        self._create_test_acl()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_view
        )

        self._clear_events()

        response = self._request_test_acl_list_view()
        self.assertContains(
            response=response, text=force_text(s=self.test_object),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class AccessControlListPermissionViewTestCase(
    AccessControlListViewTestMixin, ACLTestMixin, GenericViewTestCase
):
    def test_acl_permission_get_no_permission(self):
        self._create_acl_test_object()

        self._create_test_acl()

        test_acl_permission_count = self.test_acl.permissions.count()

        self._clear_events()

        response = self._request_test_acl_permission_list_get_view()
        self.assertNotContains(
            response=response, text=force_text(s=self.test_object),
            status_code=404
        )

        self.assertEqual(
            self.test_acl.permissions.count(), test_acl_permission_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_permission_get_with_access(self):
        self._create_acl_test_object()

        self._create_test_acl()

        test_acl_permission_count = self.test_acl.permissions.count()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        self._clear_events()

        response = self._request_test_acl_permission_list_get_view()
        self.assertContains(
            response=response, text=force_text(s=self.test_object),
            status_code=200
        )

        self.assertEqual(
            self.test_acl.permissions.count(), test_acl_permission_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_permission_add_view_with_access(self):
        self._create_acl_test_object()

        self._create_test_acl()

        test_acl_permission_count = self.test_acl.permissions.count()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )
        test_acl_permission_count = self.test_acl.permissions.count()

        self._clear_events()

        response = self._request_test_acl_permission_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_acl.permissions.count(), test_acl_permission_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_permission.stored_permission
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_acl)
        self.assertEqual(events[0].verb, event_acl_edited.id)

    def test_acl_permission_remove_view_with_access(self):
        self._create_acl_test_object()

        self._create_test_acl()
        self.test_acl.permissions.add(self.test_permission.stored_permission)

        test_acl_permission_count = self.test_acl.permissions.count()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )
        test_acl_permission_count = self.test_acl.permissions.count()

        self._clear_events()

        response = self._request_test_acl_permission_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_acl.permissions.count(), test_acl_permission_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_permission.stored_permission
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_acl)
        self.assertEqual(events[0].verb, event_acl_edited.id)


class GlobalAccessControlListViewTestCase(
    AccessControlListViewTestMixin, ACLTestMixin, GenericViewTestCase
):

    def test_global_acl_list_view_no_permission(self):
        self._create_acl_test_object()

        self._create_test_acl()

        self._clear_events()

        response = self._request_test_global_acl_list_view()
        self.assertNotContains(
            response=response, text=force_text(s=self.test_object),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_global_acl_list_view_with_access(self):
        self._create_acl_test_object()

        self._create_test_acl()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_view
        )

        self._clear_events()

        response = self._request_test_global_acl_list_view()
        self.assertContains(
            response=response, text=force_text(s=self.test_object),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class OrphanAccessControlListViewTestCase(
    AccessControlListViewTestMixin, ACLTestMixin, GenericViewTestCase
):
    def test_orphan_acl_create_view_with_permission(self):
        """
        Test creating an ACL entry for an object with no model permissions.
        Result: Should display a blank permissions list (no optgroup)
        """
        self._create_acl_test_object(
            create_test_permission=False, register_model_permissions=False
        )
        EventModelRegistry.register(model=self.TestModel)

        self.grant_permission(permission=permission_acl_edit)

        test_acl_count = AccessControlList.objects.count()

        self._clear_events()

        reponse = self._request_test_acl_create_post_view()
        self.assertEqual(reponse.status_code, 302)

        response = self._request_test_acl_create_get_view()
        self.assertNotContains(
            response=response, text='optgroup', status_code=200
        )

        self.assertEqual(
            AccessControlList.objects.count(), test_acl_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_object)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_acl)
        self.assertEqual(events[0].verb, event_acl_created.id)
