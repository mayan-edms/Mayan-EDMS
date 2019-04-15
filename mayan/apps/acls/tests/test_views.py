from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType

from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..models import AccessControlList
from ..permissions import permission_acl_edit, permission_acl_view


class AccessControlListViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(AccessControlListViewTestCase, self).setUp()

        content_type = ContentType.objects.get_for_model(self.document)

        self.view_arguments = {
            'app_label': content_type.app_label,
            'model': content_type.model,
            'object_id': self.document.pk
        }
        self.login_user()

    def test_acl_create_view_no_permission(self):
        response = self.get(
            viewname='acls:acl_create', kwargs=self.view_arguments, data={
                'role': self.role.pk
            }
        )

        self.assertEquals(response.status_code, 403)
        self.assertEqual(AccessControlList.objects.count(), 0)

    def test_acl_create_view_with_permission(self):
        self.role.permissions.add(
            permission_acl_edit.stored_permission
        )

        response = self.get(
            viewname='acls:acl_create', kwargs=self.view_arguments, data={
                'role': self.role.pk
            }, follow=True
        )

        self.assertContains(
            response, text=self.document.label, status_code=200
        )

    def test_acl_create_view_post_no_permission(self):
        response = self.post(
            viewname='acls:acl_create', kwargs=self.view_arguments, data={
                'role': self.role.pk
            }
        )

        self.assertEquals(response.status_code, 403)
        self.assertEqual(AccessControlList.objects.count(), 0)

    def test_acl_create_view_with_post_permission(self):
        self.role.permissions.add(
            permission_acl_edit.stored_permission
        )

        response = self.post(
            viewname='acls:acl_create', kwargs=self.view_arguments, data={
                'role': self.role.pk
            }, follow=True
        )

        self.assertContains(response, text='created', status_code=200)
        self.assertEqual(AccessControlList.objects.count(), 1)

    def test_orphan_acl_create_view_with_permission(self):
        """
        Test creating an ACL entry for an object with no model permissions.
        Result: Should display a blank permissions list (not optgroup)
        """
        self.role.permissions.add(
            permission_acl_edit.stored_permission
        )

        recent_entry = self.document.add_as_recent_document_for_user(self.user)

        content_type = ContentType.objects.get_for_model(recent_entry)

        view_arguments = {
            'app_label': content_type.app_label,
            'model': content_type.model,
            'object_id': recent_entry.pk
        }

        response = self.post(
            viewname='acls:acl_create', kwargs=view_arguments, data={
                'role': self.role.pk
            }, follow=True
        )

        self.assertNotContains(response, text='optgroup', status_code=200)
        self.assertEqual(AccessControlList.objects.count(), 1)

    def test_acl_list_view_no_permission(self):
        document = self.document.add_as_recent_document_for_user(
            self.user
        ).document

        acl = AccessControlList.objects.create(
            content_object=document, role=self.role
        )
        acl.permissions.add(permission_acl_edit.stored_permission)

        content_type = ContentType.objects.get_for_model(document)

        view_arguments = {
            'app_label': content_type.app_label,
            'model': content_type.model,
            'object_id': document.pk
        }

        response = self.get(
            viewname='acls:acl_list', kwargs=view_arguments
        )

        self.assertNotContains(response, text=document.label, status_code=403)
        self.assertNotContains(response, text='otal: 1', status_code=403)

    def test_acl_list_view_with_permission(self):
        self.role.permissions.add(
            permission_acl_view.stored_permission
        )

        document = self.document.add_as_recent_document_for_user(
            self.user
        ).document

        acl = AccessControlList.objects.create(
            content_object=document, role=self.role
        )
        acl.permissions.add(permission_acl_view.stored_permission)

        content_type = ContentType.objects.get_for_model(document)

        view_arguments = {
            'app_label': content_type.app_label,
            'model': content_type.model,
            'object_id': document.pk
        }

        response = self.get(
            viewname='acls:acl_list', kwargs=view_arguments
        )
        self.assertContains(response, text=document.label, status_code=200)
