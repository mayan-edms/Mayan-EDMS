from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.documents.tests import GenericDocumentViewTestCase
from mayan.apps.metadata.permissions import permission_document_metadata_edit
from mayan.apps.metadata.tests.mixins import MetadataTypeTestMixin

from ..permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)

from .mixins import GroupTestMixin, GroupViewTestMixin, UserViewTestMixin


class GroupViewsTestCase(GroupTestMixin, GroupViewTestMixin, GenericViewTestCase):
    def test_group_create_view_no_permission(self):
        group_count = Group.objects.count()

        response = self._request_test_group_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Group.objects.count(), group_count)

    def test_group_create_view_with_permission(self):
        self.grant_permission(permission=permission_group_create)

        group_count = Group.objects.count()

        response = self._request_test_group_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Group.objects.count(), group_count + 1)

    def test_group_delete_view_no_permission(self):
        self._create_test_group()

        group_count = Group.objects.count()

        response = self._request_test_group_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Group.objects.count(), group_count)

    def test_group_delete_view_with_access(self):
        self._create_test_group()
        self.grant_access(
            obj=self.test_group, permission=permission_group_delete
        )

        group_count = Group.objects.count()

        response = self._request_test_group_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Group.objects.count(), group_count - 1)

    def test_group_edit_view_no_permission(self):
        self._create_test_group()

        group_name = self.test_group.name

        response = self._request_test_group_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_group.refresh_from_db()
        self.assertEqual(self.test_group.name, group_name)

    def test_group_edit_view_with_access(self):
        self._create_test_group()
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        group_name = self.test_group.name

        response = self._request_test_group_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_group.refresh_from_db()
        self.assertNotEqual(self.test_group.name, group_name)

    def test_group_list_view_no_permission(self):
        self._create_test_group()

        response = self._request_test_group_list_view()
        self.assertNotContains(
            response=response, text=self.test_group.name, status_code=200
        )

    def test_group_list_view_with_permission(self):
        self._create_test_group()

        self.grant_access(
            obj=self.test_group, permission=permission_group_view
        )
        response = self._request_test_group_list_view()
        self.assertContains(
            response=response, text=self.test_group.name, status_code=200
        )

    def test_group_members_view_no_permission(self):
        self._create_test_user()
        self._create_test_group()
        self.test_user.groups.add(self.test_group)

        response = self._request_test_group_members_view()
        self.assertEqual(response.status_code, 404)

    def test_group_members_view_with_group_access(self):
        self._create_test_user()
        self._create_test_group()
        self.test_user.groups.add(self.test_group)
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        response = self._request_test_group_members_view()
        self.assertContains(
            response=response, text=self.test_group.name, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_user.username, status_code=200
        )

    def test_group_members_view_with_user_access(self):
        self._create_test_user()
        self._create_test_group()
        self.test_user.groups.add(self.test_group)
        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        response = self._request_test_group_members_view()
        self.assertNotContains(
            response=response, text=self.test_group.name, status_code=404
        )

    def test_group_members_view_with_full_access(self):
        self._create_test_user()
        self._create_test_group()
        self.test_user.groups.add(self.test_group)
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        response = self._request_test_group_members_view()
        self.assertContains(
            response=response, text=self.test_user.username, status_code=200
        )
        self.assertContains(
            response=response, text=self.test_group.name, status_code=200
        )


class SuperUserViewTestCase(UserViewTestMixin, GenericViewTestCase):
    def setUp(self):
        super(SuperUserViewTestCase, self).setUp()
        self._create_test_superuser()

    def test_superuser_delete_view_with_access(self):
        superuser_count = get_user_model().objects.filter(is_superuser=True).count()
        self.grant_access(
            obj=self.test_superuser, permission=permission_user_delete
        )
        response = self._request_test_superuser_delete_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            get_user_model().objects.filter(is_superuser=True).count(),
            superuser_count
        )

    def test_superuser_detail_view_with_access(self):
        self.grant_access(
            obj=self.test_superuser, permission=permission_user_view
        )
        response = self._request_test_superuser_detail_view()
        self.assertEqual(response.status_code, 404)

    def _request_test_user_detail_view(self):
        return self.get(
            viewname='user_management:user_details', kwargs={
                'pk': self.test_user.pk
            }
        )

    def test_superuser_normal_user_detail_view_with_access(self):
        self.grant_access(
            obj=self.test_superuser, permission=permission_user_view
        )

        self.test_user = self.test_superuser
        response = self._request_test_user_detail_view()
        self.assertEqual(response.status_code, 404)


class UserViewTestCase(UserViewTestMixin, GenericViewTestCase):
    def test_user_create_view_no_permission(self):
        user_count = get_user_model().objects.count()

        response = self._request_test_user_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(get_user_model().objects.count(), user_count)

    def test_user_create_view_with_permission(self):
        self.grant_permission(permission=permission_user_create)

        user_count = get_user_model().objects.count()

        response = self._request_test_user_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(get_user_model().objects.count(), user_count + 1)

    def test_user_delete_view_no_access(self):
        self._create_test_user()

        user_count = get_user_model().objects.count()

        response = self._request_test_user_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(get_user_model().objects.count(), user_count)

    def test_user_delete_view_with_access(self):
        self._create_test_user()

        user_count = get_user_model().objects.count()

        self.grant_access(obj=self.test_user, permission=permission_user_delete)

        response = self._request_test_user_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(get_user_model().objects.count(), user_count - 1)

    def test_user_multiple_delete_view_no_access(self):
        self._create_test_user()

        user_count = get_user_model().objects.count()

        response = self._request_test_user_delete_multiple_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(get_user_model().objects.count(), user_count)

    def test_user_multiple_delete_view_with_access(self):
        self._create_test_user()

        user_count = get_user_model().objects.count()

        self.grant_access(obj=self.test_user, permission=permission_user_delete)

        response = self._request_test_user_delete_multiple_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(get_user_model().objects.count(), user_count - 1)


class UserGroupViewTestCase(
    GroupTestMixin, UserViewTestMixin, GenericViewTestCase
):
    def test_user_groups_view_no_permission(self):
        self._create_test_user()
        self._create_test_group()
        self.test_user.groups.add(self.test_group)

        response = self._request_test_user_groups_view()
        self.assertEqual(response.status_code, 404)

    def test_user_groups_view_with_group_access(self):
        self._create_test_user()
        self._create_test_group()
        self.test_user.groups.add(self.test_group)
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        response = self._request_test_user_groups_view()
        self.assertNotContains(
            response=response, text=self.test_user.username, status_code=404
        )

    def test_user_groups_view_with_user_access(self):
        self._create_test_user()
        self._create_test_group()
        self.test_user.groups.add(self.test_group)
        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        response = self._request_test_user_groups_view()
        self.assertContains(
            response=response, text=self.test_user.username, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_group.name, status_code=200
        )

    def test_user_groups_view_with_full_access(self):
        self._create_test_user()
        self._create_test_group()
        self.test_user.groups.add(self.test_group)
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        response = self._request_test_user_groups_view()
        self.assertContains(
            response=response, text=self.test_user.username, status_code=200
        )
        self.assertContains(
            response=response, text=self.test_group.name, status_code=200
        )


class MetadataLookupIntegrationTestCase(
    MetadataTypeTestMixin, GenericDocumentViewTestCase
):
    def setUp(self):
        super(MetadataLookupIntegrationTestCase, self).setUp()
        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

    def test_user_list_lookup_render(self):
        self.test_metadata_type.lookup = '{{ users }}'
        self.test_metadata_type.save()
        self.test_document.metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_metadata_edit
        )

        response = self.get(
            viewname='metadata:metadata_edit', kwargs={
                'pk': self.test_document.pk
            }
        )
        self.assertContains(
            response=response, text='<option value="{}">{}</option>'.format(
                self._test_case_user.username, self._test_case_user.username
            ), status_code=200
        )

    def test_group_list_lookup_render(self):
        self.test_metadata_type.lookup = '{{ groups }}'
        self.test_metadata_type.save()
        self.test_document.metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_metadata_edit
        )

        response = self.get(
            viewname='metadata:metadata_edit', kwargs={
                'pk': self.test_document.pk
            }
        )

        self.assertContains(
            response=response, text='<option value="{}">{}</option>'.format(
                self._test_case_group.name, self._test_case_group.name
            ), status_code=200
        )
