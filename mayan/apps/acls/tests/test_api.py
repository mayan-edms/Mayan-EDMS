from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..classes import ModelPermission
from ..events import event_acl_created, event_acl_deleted, event_acl_edited
from ..models import AccessControlList
from ..permissions import permission_acl_edit, permission_acl_view

from .mixins import ACLAPIViewTestMixin, ACLTestMixin


class ACLAPIViewTestCase(ACLTestMixin, ACLAPIViewTestMixin, BaseAPITestCase):
    auto_create_acl_test_object = True

    def test_acl_create_api_view_no_permission(self):
        acl_count = AccessControlList.objects.count()

        self._clear_events()

        response = self._request_test_acl_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(AccessControlList.objects.count(), acl_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        self._clear_events()

        response = self._request_test_acl_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.test_acl.role, self.test_role)
        self.assertEqual(self.test_acl.content_object, self.test_object)
        self.assertEqual(self.test_acl.permissions.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_object)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_acl)
        self.assertEqual(events[0].verb, event_acl_created.id)

    def test_acl_delete_api_view_no_permission(self):
        self._create_test_acl()

        acl_count = AccessControlList.objects.count()

        self._clear_events()

        response = self._request_test_acl_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(AccessControlList.objects.count(), acl_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_delete_api_view_with_access(self):
        self._create_test_acl()

        self.grant_access(self.test_object, permission=permission_acl_edit)

        acl_count = AccessControlList.objects.count()

        self._clear_events()

        response = self._request_test_acl_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(AccessControlList.objects.count(), acl_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_object)
        self.assertEqual(events[0].verb, event_acl_deleted.id)

    def test_acl_detail_api_view_no_permission(self):
        self._create_test_acl()

        self._clear_events()

        response = self._request_test_acl_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_detail_api_view_with_access(self):
        self._create_test_acl()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_view
        )

        self._clear_events()

        response = self._request_test_acl_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['content_type']['app_label'],
            self.test_object_content_type.app_label
        )
        self.assertEqual(
            response.data['role']['label'], self.test_role.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_list_api_view_no_permission(self):
        self._create_test_acl()

        self._clear_events()

        response = self._request_test_acl_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_list_api_view_with_access(self):
        self._create_test_acl()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_view
        )

        self._clear_events()

        response = self._request_test_acl_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
            response=response, text=self.test_object_content_type.app_label
        )
        self.assertContains(
            response=response, text=self.test_acl.role.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class ACLPermissionAPIViewTestCase(
    ACLTestMixin, ACLAPIViewTestMixin, BaseAPITestCase
):
    auto_create_acl_test_object = True

    def test_acl_permission_add_api_view_no_permission(self):
        self._create_test_acl()

        self._clear_events()

        response = self._request_test_acl_permission_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(
            self.test_permission.stored_permission in self.test_acl.permissions.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_permission_add_api_view_with_access(self):
        self._create_test_acl()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        self._clear_events()

        response = self._request_test_acl_permission_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            self.test_permission.stored_permission in self.test_acl.permissions.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_permission.stored_permission
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_acl)
        self.assertEqual(events[0].verb, event_acl_edited.id)

    def test_acl_permission_list_api_view_no_permission(self):
        self._create_test_acl()
        self.test_acl.permissions.add(self.test_permission.stored_permission)

        self._clear_events()

        response = self._request_test_acl_permission_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_permission_list_api_view_with_access(self):
        self._create_test_acl()
        self.test_acl.permissions.add(self.test_permission.stored_permission)

        self.grant_access(
            obj=self.test_object, permission=permission_acl_view
        )

        self._clear_events()

        response = self._request_test_acl_permission_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['pk'],
            self.test_permission.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_permission_remove_api_view_no_permission(self):
        self._create_test_acl()
        self.test_acl.permissions.add(self.test_permission.stored_permission)

        acl_permission_count = self.test_acl.permissions.count()

        self._clear_events()

        response = self._request_test_acl_permission_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_acl.permissions.count(), acl_permission_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_acl_permission_remove_api_view_with_access(self):
        self._create_test_acl()
        self.test_acl.permissions.add(self.test_permission.stored_permission)

        self.grant_access(obj=self.test_object, permission=permission_acl_edit)

        acl_permission_count = self.test_acl.permissions.count()

        self._clear_events()

        response = self._request_test_acl_permission_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            self.test_acl.permissions.count(), acl_permission_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_permission.stored_permission
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_acl)
        self.assertEqual(events[0].verb, event_acl_edited.id)


class ClassPermissionAPIViewTestCase(
    ACLTestMixin, ACLAPIViewTestMixin, BaseAPITestCase
):
    auto_create_test_object = True

    def test_class_permission_list_api_view(self):
        class_permissions = [
            permission.pk for permission in ModelPermission.get_for_class(
                klass=self.test_object_content_type.model_class()
            )
        ]

        response = self._request_test_class_permission_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_permissions = [
            permission['pk'] for permission in response.data['results']
        ]

        self.assertEqual(class_permissions, response_permissions)
