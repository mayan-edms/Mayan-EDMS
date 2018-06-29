from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from common.tests import GenericViewTestCase
from documents.tests import GenericDocumentViewTestCase

from metadata.models import MetadataType
from metadata.permissions import permission_metadata_document_edit

from metadata.tests.literals import (
    TEST_METADATA_TYPE_LABEL, TEST_METADATA_TYPE_NAME,
)

from ..permissions import (
    permission_user_create, permission_user_delete, permission_user_edit
)

from .literals import (
    TEST_USER_PASSWORD_EDITED, TEST_USER_USERNAME, TEST_USER_2_USERNAME
)

TEST_USER_TO_DELETE_USERNAME = 'user_to_delete'


class UserManagementViewTestCase(GenericViewTestCase):
    def setUp(self):
        super(UserManagementViewTestCase, self).setUp()
        self.login_user()

    def _request_user_create_view(self):
        return self.post(
            viewname='user_management:user_add', data={
                'username': TEST_USER_2_USERNAME
            }
        )

    def test_user_create_view_no_permission(self):
        response = self._request_user_create_view()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertFalse(TEST_USER_2_USERNAME in get_user_model().objects.values_list('username', flat=True))

    def test_user_create_view_with_permission(self):
        self.grant_permission(permission=permission_user_create)
        response = self._request_user_create_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 3)
        self.assertTrue(TEST_USER_2_USERNAME in get_user_model().objects.values_list('username', flat=True))

    def _request_set_password(self, password):
        return self.post(
            viewname='user_management:user_set_password', args=(self.user_2.pk,),
            data={
                'new_password1': password, 'new_password2': password
            }
        )

    def _create_test_user_2(self):
        self.user_2 = get_user_model().objects.create(
            username=TEST_USER_2_USERNAME
        )

    def test_user_set_password_view_no_access(self):
        self._create_test_user_2()
        response = self._request_set_password(
            password=TEST_USER_PASSWORD_EDITED
        )

        self.assertEqual(response.status_code, 403)

        self.logout()

        with self.assertRaises(AssertionError):
            self.login(
                username=TEST_USER_2_USERNAME, password=TEST_USER_PASSWORD_EDITED
            )

        response = self.get('common:current_user_details')

        self.assertEqual(response.status_code, 302)

    def test_user_set_password_view_with_access(self):
        self._create_test_user_2()
        self.grant_access(permission=permission_user_edit, obj=self.user_2)

        response = self._request_set_password(
            password=TEST_USER_PASSWORD_EDITED
        )

        self.assertEqual(response.status_code, 302)

        self.logout()
        self.login(
            username=TEST_USER_2_USERNAME, password=TEST_USER_PASSWORD_EDITED
        )
        response = self.get('common:current_user_details')

        self.assertEqual(response.status_code, 200)

    def _request_multiple_user_set_password(self, password):
        return self.post(
            'user_management:user_multiple_set_password', data={
                'id_list': self.user_2.pk,
                'new_password1': password,
                'new_password2': password
            }
        )

    def test_user_multiple_set_password_view_no_access(self):
        self._create_test_user_2()
        response = self._request_multiple_user_set_password(
            password=TEST_USER_PASSWORD_EDITED
        )

        self.assertEqual(response.status_code, 403)

        self.logout()

        with self.assertRaises(AssertionError):
            self.login(
                username=TEST_USER_2_USERNAME, password=TEST_USER_PASSWORD_EDITED
            )

        response = self.get('common:current_user_details')
        self.assertEqual(response.status_code, 302)

    def test_user_multiple_set_password_view_with_access(self):
        self._create_test_user_2()
        self.grant_access(permission=permission_user_edit, obj=self.user_2)

        response = self._request_multiple_user_set_password(
            password=TEST_USER_PASSWORD_EDITED
        )

        self.assertEqual(response.status_code, 302)

        self.logout()
        self.login(
            username=TEST_USER_2_USERNAME, password=TEST_USER_PASSWORD_EDITED
        )
        response = self.get('common:current_user_details')

        self.assertEqual(response.status_code, 200)

    def _request_user_delete(self):
        return self.post(
            viewname='user_management:user_delete', args=(self.user_2.pk,)
        )

    def test_user_delete_view_no_access(self):
        self._create_test_user_2()
        response = self._request_user_delete()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 3)

    def test_user_delete_view_with_access(self):
        self._create_test_user_2()
        self.grant_access(permission=permission_user_delete, obj=self.user_2)
        response = self._request_user_delete()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 2)

    def _request_user_multiple_delete_view(self):
        return self.post(
            viewname='user_management:user_multiple_delete', data={
                'id_list': self.user_2.pk
            }
        )

    def test_user_multiple_delete_view_no_access(self):
        self._create_test_user_2()
        response = self._request_user_multiple_delete_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 3)

    def test_user_multiple_delete_view_with_access(self):
        self._create_test_user_2()
        self.grant_access(permission=permission_user_delete, obj=self.user_2)
        response = self._request_user_multiple_delete_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 2)


class MetadataLookupIntegrationTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(MetadataLookupIntegrationTestCase, self).setUp()

        self.metadata_type = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
        )

        self.document_type.metadata.create(metadata_type=self.metadata_type)

        self.login_user()

    def test_user_list_lookup_render(self):
        self.metadata_type.lookup = '{{ users }}'
        self.metadata_type.save()
        self.document.metadata.create(metadata_type=self.metadata_type)
        self.role.permissions.add(
            permission_metadata_document_edit.stored_permission
        )

        response = self.get(
            viewname='metadata:metadata_edit', args=(self.document.pk,)
        )

        self.assertContains(
            response, text='<option value="{}">{}</option>'.format(
                TEST_USER_USERNAME, TEST_USER_USERNAME
            ), status_code=200
        )

    def test_group_list_lookup_render(self):
        self.metadata_type.lookup = '{{ groups }}'
        self.metadata_type.save()
        self.document.metadata.create(metadata_type=self.metadata_type)
        self.role.permissions.add(
            permission_metadata_document_edit.stored_permission
        )

        response = self.get(
            viewname='metadata:metadata_edit', args=(self.document.pk,)
        )

        self.assertContains(
            response, text='<option value="{}">{}</option>'.format(
                Group.objects.first().name, Group.objects.first().name
            ), status_code=200
        )
