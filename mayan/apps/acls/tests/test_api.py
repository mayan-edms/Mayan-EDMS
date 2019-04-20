from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType

from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests import DocumentTestMixin
from mayan.apps.permissions.tests.literals import TEST_ROLE_LABEL
from mayan.apps.rest_api.tests import BaseAPITestCase

from ..models import AccessControlList
from ..permissions import permission_acl_edit, permission_acl_view

from .mixins import ACLTestMixin


class ACLAPITestCase(ACLTestMixin, DocumentTestMixin, BaseAPITestCase):
    def setUp(self):
        super(ACLAPITestCase, self).setUp()
        self.test_object = self.test_document
        self.test_object_content_type = ContentType.objects.get_for_model(
            self.test_object
        )

    def test_acl_list_api_view_with_access(self):
        self._create_test_acl()

        self.grant_access(obj=self.test_object, permission=permission_acl_view)

        response = self.get(
            viewname='rest_api:accesscontrollist-list',
            args=(
                self.test_object_content_type.app_label,
                self.test_object_content_type.model,
                self.test_object.pk
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
            response=response, text=self.test_object_content_type.app_label,
            status_code=200
        )
        self.assertContains(
            response=response, text=self.test_acl.role.label,
            status_code=200
        )

    def _request_test_acl_delete_api_view(self):
        return self.delete(
            viewname='rest_api:accesscontrollist-detail',
            args=(
                self.test_object_content_type.app_label,
                self.test_object_content_type.model,
                self.test_object.pk, self.test_acl.pk
            )
        )

    def test_acl_delete_api_view_with_access(self):
        self.expected_content_type = None
        self._create_test_acl()

        self.grant_access(self.test_object, permission=permission_acl_edit)

        acl_count = AccessControlList.objects.count()

        response = self._request_test_acl_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(AccessControlList.objects.count(), acl_count - 1)

    def _request_test_acl_detail_api_view(self):
        return self.get(
            viewname='rest_api:accesscontrollist-detail',
            args=(
                self.test_object_content_type.app_label,
                self.test_object_content_type.model,
                self.test_object.pk, self.test_acl.pk
            )
        )


    def test_acl_detail_api_view_with_access(self):
        self._create_test_acl()

        self.grant_access(obj=self.test_object, permission=permission_acl_view)

        response = self._request_test_acl_detail_api_view()

        self.assertEqual(
            response.data['content_type']['app_label'],
            self.test_object_content_type.app_label
        )
        self.assertEqual(
            response.data['role']['label'], TEST_ROLE_LABEL
        )

    def _request_test_acl_permission_delete_api_view(self):
        return self.delete(
            viewname='rest_api:accesscontrollist-permission-detail',
            args=(
                self.test_object_content_type.app_label,
                self.test_object_content_type.model,
                self.test_object.pk, self.test_acl.pk,
                self.test_permission.stored_permission.pk
            )
        )


    def test_acl_permission_delete_view_with_access(self):
        self.expected_content_type = None
        self.test_permission = permission_document_view
        self._create_test_acl()
        self.test_acl.permissions.add(self.test_permission.stored_permission)

        self.grant_access(obj=self.test_object, permission=permission_acl_edit)

        response = self._request_test_acl_permission_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.test_acl.permissions.count(), 0)

    def _request_test_acl_permission_detail_api_view(self):
        return self.get(
            viewname='rest_api:accesscontrollist-permission-detail',
            args=(
                self.test_object_content_type.app_label,
                self.test_object_content_type.model,
                self.test_object.pk, self.test_acl.pk,
                self.test_acl.permissions.first().pk
            )
        )

    def test_acl_permission_detail_api_view_with_access(self):
        self._create_test_acl()
        self.test_acl.permissions.add(permission_document_view.stored_permission)

        self.grant_access(obj=self.test_object, permission=permission_acl_view)

        response = self._request_test_acl_permission_detail_api_view()
        self.assertEqual(
            response.data['pk'], permission_document_view.pk
        )

    def _request_test_acl_permission_list_api_get_view(self):
        return self.get(
            viewname='rest_api:accesscontrollist-permission-list',
            args=(
                self.test_object_content_type.app_label,
                self.test_object_content_type.model,
                self.test_object.pk, self.test_acl.pk
            )
        )

    def test_acl_permission_list_api_get_view_with_access(self):
        self._create_test_acl()
        self.test_acl.permissions.add(permission_document_view.stored_permission)

        self.grant_access(obj=self.test_object, permission=permission_acl_view)

        response = self._request_test_acl_permission_list_api_get_view()
        self.assertEqual(
            response.data['results'][0]['pk'],
            permission_document_view.pk
        )

    def _request_acl_permssion_list_api_post_view(self):
        return self.post(
            viewname='rest_api:accesscontrollist-permission-list',
            args=(
                self.test_object_content_type.app_label,
                self.test_object_content_type.model,
                self.test_object.pk, self.test_acl.pk
            ), data={'permission_pk': self.test_permission.pk}
        )

    def test_acl_permission_list_api_post_view_with_access(self):
        self._create_test_acl()
        self.test_permission = permission_document_view

        self.grant_access(obj=self.test_object, permission=permission_acl_edit)

        response = self._request_acl_permssion_list_api_post_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            self.test_permission.stored_permission in self.test_acl.permissions.all()
        )

    def _request_acl_create_api_view(self, extra_data=None):
        data = {'role_pk': self.test_role.pk}

        if extra_data:
            data.update(extra_data)

        return self.post(
            viewname='rest_api:accesscontrollist-list',
            args=(
                self.test_object_content_type.app_label,
                self.test_object_content_type.model,
                self.test_object.pk
            ), data=data
        )

    def test_acl_create_api_api_view_with_access(self):
        self.grant_access(obj=self.test_object, permission=permission_acl_edit)

        response = self._request_acl_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = response.data['id']

        test_object_acl = self.test_object.acls.get(pk=pk)
        self.assertEqual(
            test_object_acl.role, self.test_role
        )
        self.assertEqual(
            test_object_acl.content_object, self.test_object
        )
        self.assertEqual(
            test_object_acl.permissions.count(), 0
        )

    def test_acl_create_post_api_extra_data_view_with_access(self):
        self.grant_access(obj=self.test_object, permission=permission_acl_edit)

        response = self._request_acl_create_api_view(
            extra_data={'permissions_pk_list': permission_acl_view.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = response.data['id']

        test_object_acl = self.test_object.acls.get(pk=pk)

        self.assertEqual(
            test_object_acl.content_object, self.test_object
        )
        self.assertEqual(
            test_object_acl.role, self.test_role
        )
        self.assertEqual(
            test_object_acl.permissions.first(),
            permission_acl_view.stored_permission
        )
