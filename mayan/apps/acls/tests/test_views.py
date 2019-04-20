from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType

from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..models import AccessControlList
from ..permissions import permission_acl_edit, permission_acl_view

from .mixins import ACLTestMixin


class AccessControlListViewTestCase(ACLTestMixin, GenericDocumentViewTestCase):
    def setUp(self):
        super(AccessControlListViewTestCase, self).setUp()

        content_type = ContentType.objects.get_for_model(self.test_document)

        self.view_arguments = {
            'app_label': content_type.app_label,
            'model': content_type.model,
            'object_id': self.test_document.pk
        }

        self.test_object = self.test_document

    def _request_test_acl_create_get_view(self):
        return self.get(
            viewname='acls:acl_create', kwargs=self.view_arguments, data={
                'role': self.test_role.pk
            }, follow=True
        )

    def test_acl_create_get_view_no_permission(self):
        acl_count = AccessControlList.objects.count()

        response = self._request_test_acl_create_get_view()
        self.assertEquals(response.status_code, 403)

        self.assertEqual(AccessControlList.objects.count(), acl_count)

    def test_acl_create_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_acl_edit
        )
        acl_count = AccessControlList.objects.count()

        response = self._request_test_acl_create_get_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

        self.assertEqual(AccessControlList.objects.count(), acl_count)

    def _request_test_acl_create_post_view(self):
        return self.post(
            viewname='acls:acl_create', kwargs=self.view_arguments, data={
                'role': self.test_role.pk
            }, follow=True
        )

    def test_acl_create_view_post_no_permission(self):
        acl_count = AccessControlList.objects.count()

        response = self._request_test_acl_create_post_view()
        self.assertEquals(response.status_code, 403)

        self.assertEqual(AccessControlList.objects.count(), acl_count)

    def test_acl_create_view_post_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_acl_edit
        )

        acl_count = AccessControlList.objects.count()

        response = self._request_test_acl_create_post_view()
        self.assertContains(response=response, text='created', status_code=200)
        self.assertEqual(AccessControlList.objects.count(), acl_count + 1)

    def test_orphan_acl_create_view_with_permission(self):
        """
        Test creating an ACL entry for an object with no model permissions.
        Result: Should display a blank permissions list (not optgroup)
        """
        self.grant_permission(permission=permission_acl_edit)

        recent_entry = self.test_document.add_as_recent_document_for_user(
            self._test_case_user
        )

        content_type = ContentType.objects.get_for_model(recent_entry)

        view_arguments = {
            'app_label': content_type.app_label,
            'model': content_type.model,
            'object_id': recent_entry.pk
        }

        response = self.post(
            viewname='acls:acl_create', kwargs=view_arguments, data={
                'role': self.test_role.pk
            }, follow=True
        )
        self.assertNotContains(response, text='optgroup', status_code=200)
        self.assertEqual(AccessControlList.objects.count(), 1)

    def test_acl_list_view_no_permission(self):
        self._create_test_acl()

        response = self.get(
            viewname='acls:acl_list', kwargs=self.view_arguments
        )

        self.assertNotContains(
            response=response, text=self.document.label, status_code=403
        )
        self.assertNotContains(
            response=response, text='otal: 1', status_code=403
        )

    def test_acl_list_view_with_permission(self):
        self.grant_access(
            obj=self.test_document, permission=permission_acl_view
        )

        response = self.get(
            viewname='acls:acl_list', kwargs=self.view_arguments
        )
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
