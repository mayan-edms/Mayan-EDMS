from __future__ import absolute_import, unicode_literals

from mayan.apps.common.tests.base import GenericViewTestCase

from ..models import AccessControlList
from ..permissions import permission_acl_edit, permission_acl_view

from .mixins import ACLTestMixin


class AccessControlListViewTestMixin(object):
    def _request_test_acl_create_get_view(self):
        return self.get(
            viewname='acls:acl_create',
            kwargs=self.test_content_object_view_kwargs, data={
                'role': self.test_role.pk
            }
        )

    def _request_test_acl_create_post_view(self):
        return self.post(
            viewname='acls:acl_create',
            kwargs=self.test_content_object_view_kwargs, data={
                'role': self.test_role.pk
            }
        )


class AccessControlListViewTestCase(
    AccessControlListViewTestMixin, ACLTestMixin, GenericViewTestCase
):
    def test_acl_create_get_view_no_permission(self):
        self._setup_test_object()

        acl_count = AccessControlList.objects.count()

        response = self._request_test_acl_create_get_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(AccessControlList.objects.count(), acl_count)

    def test_acl_create_get_view_with_access(self):
        self._setup_test_object()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )
        acl_count = AccessControlList.objects.count()

        response = self._request_test_acl_create_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(AccessControlList.objects.count(), acl_count)

    def test_acl_create_view_post_no_permission(self):
        self._setup_test_object()

        acl_count = AccessControlList.objects.count()

        response = self._request_test_acl_create_post_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(AccessControlList.objects.count(), acl_count)

    def test_acl_create_view_post_with_access(self):
        self._setup_test_object()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        acl_count = AccessControlList.objects.count()

        response = self._request_test_acl_create_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(AccessControlList.objects.count(), acl_count + 1)

    def test_orphan_acl_create_view_with_permission(self):
        """
        Test creating an ACL entry for an object with no model permissions.
        Result: Should display a blank permissions list (not optgroup)
        """
        self._setup_test_object(register_model_permissions=False)

        self.grant_permission(permission=permission_acl_edit)

        response = self.post(
            viewname='acls:acl_create',
            kwargs=self.test_content_object_view_kwargs, data={
                'role': self.test_role.pk
            }, follow=True
        )
        self.assertNotContains(
            response=response, text='optgroup', status_code=200
        )

        self.assertEqual(AccessControlList.objects.count(), 1)

    def test_acl_list_view_no_permission(self):
        self._setup_test_object()

        self._create_test_acl()

        response = self.get(
            viewname='acls:acl_list',
            kwargs=self.test_content_object_view_kwargs
        )
        self.assertEqual(response.status_code, 403)

    def test_acl_list_view_with_permission(self):
        self._setup_test_object()

        self.grant_access(
            obj=self.test_object, permission=permission_acl_view
        )

        response = self.get(
            viewname='acls:acl_list',
            kwargs=self.test_content_object_view_kwargs
        )
        self.assertEqual(response.status_code, 200)
