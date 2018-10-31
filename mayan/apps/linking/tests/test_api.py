from __future__ import unicode_literals

from django.test import override_settings

from rest_framework import status

from documents.models import DocumentType
from documents.permissions import permission_document_view
from documents.tests import DocumentTestMixin
from documents.tests.literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_PATH
)
from rest_api.tests import BaseAPITestCase

from ..models import SmartLink, SmartLinkCondition
from ..permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)

from .literals import (
    TEST_SMART_LINK_CONDITION_FOREIGN_DOCUMENT_DATA,
    TEST_SMART_LINK_CONDITION_EXPRESSION,
    TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED,
    TEST_SMART_LINK_CONDITION_OPERATOR, TEST_SMART_LINK_DYNAMIC_LABEL,
    TEST_SMART_LINK_LABEL_EDITED, TEST_SMART_LINK_LABEL
)


@override_settings(OCR_AUTO_OCR=False)
class SmartLinkAPITestCase(DocumentTestMixin, BaseAPITestCase):
    auto_create_document_type = False
    auto_upload_document = False

    def setUp(self):
        super(SmartLinkAPITestCase, self).setUp()
        self.login_user()

    def _create_smart_link(self):
        return SmartLink.objects.create(
            label=TEST_SMART_LINK_LABEL,
            dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
        )

    def _request_smartlink_create_view(self):
        return self.post(
            viewname='rest_api:smartlink-list', data={
                'label': TEST_SMART_LINK_LABEL
            }
        )

    def test_smart_link_create_view_no_permission(self):
        response = self._request_smartlink_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(SmartLink.objects.count(), 0)

    def test_smart_link_create_view_with_permission(self):
        self.grant_permission(permission=permission_smart_link_create)
        response = self._request_smartlink_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        smart_link = SmartLink.objects.first()
        self.assertEqual(response.data['id'], smart_link.pk)
        self.assertEqual(response.data['label'], TEST_SMART_LINK_LABEL)

        self.assertEqual(SmartLink.objects.count(), 1)
        self.assertEqual(smart_link.label, TEST_SMART_LINK_LABEL)

    def _request_smart_link_create_with_document_type_view(self):
        return self.post(
            viewname='rest_api:smartlink-list', data={
                'label': TEST_SMART_LINK_LABEL,
                'document_types_pk_list': self.document_type.pk
            },
        )

    def test_smart_link_create_with_document_types_view_no_permission(self):
        self._create_document_type()
        response = self._request_smart_link_create_with_document_type_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(SmartLink.objects.count(), 0)

    def test_smart_link_create_with_document_types_view_with_permission(self):
        self._create_document_type()
        self.grant_permission(permission=permission_smart_link_create)
        response = self._request_smart_link_create_with_document_type_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        smart_link = SmartLink.objects.first()
        self.assertEqual(response.data['id'], smart_link.pk)
        self.assertEqual(response.data['label'], TEST_SMART_LINK_LABEL)

        self.assertEqual(SmartLink.objects.count(), 1)
        self.assertEqual(smart_link.label, TEST_SMART_LINK_LABEL)
        self.assertQuerysetEqual(
            smart_link.document_types.all(), (repr(self.document_type),)
        )

    def _request_smart_link_delete_view(self):
        return self.delete(
            viewname='rest_api:smartlink-detail', args=(self.smart_link.pk,)
        )

    def test_smart_link_delete_view_no_access(self):
        self.smart_link = self._create_smart_link()
        response = self._request_smart_link_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(SmartLink.objects.count(), 1)

    def test_smart_link_delete_view_with_access(self):
        self.smart_link = self._create_smart_link()
        self.grant_access(permission=permission_smart_link_delete, obj=self.smart_link)
        response = self._request_smart_link_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SmartLink.objects.count(), 0)

    def _request_smart_link_detail_view(self):
        return self.get(
            viewname='rest_api:smartlink-detail', args=(self.smart_link.pk,)
        )

    def test_smart_link_detail_view_no_access(self):
        self.smart_link = self._create_smart_link()
        response = self._request_smart_link_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('label' in response.data)

    def test_smart_link_detail_view_with_access(self):
        self.smart_link = self._create_smart_link()
        self.grant_access(permission=permission_smart_link_view, obj=self.smart_link)
        response = self._request_smart_link_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['label'], TEST_SMART_LINK_LABEL
        )

    def _request_smart_link_edit_view_via_patch(self):
        return self.patch(
            viewname='rest_api:smartlink-detail',
            args=(self.smart_link.pk,), data={
                'label': TEST_SMART_LINK_LABEL_EDITED,
                'document_types_pk_list': self.document_type.pk
            }
        )

    def test_smart_link_edit_view_via_patch_no_access(self):
        self._create_document_type()
        self.smart_link = self._create_smart_link()
        response = self._request_smart_link_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.smart_link.refresh_from_db()
        self.assertEqual(self.smart_link.label, TEST_SMART_LINK_LABEL)

    def test_smart_link_edit_view_via_patch_with_access(self):
        self._create_document_type()
        self.smart_link = self._create_smart_link()
        self.grant_access(
            permission=permission_smart_link_edit, obj=self.smart_link
        )
        response = self._request_smart_link_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.smart_link.refresh_from_db()
        self.assertEqual(self.smart_link.label, TEST_SMART_LINK_LABEL_EDITED)

    def _request_smart_link_edit_view_via_put(self):
        return self.put(
            viewname='rest_api:smartlink-detail',
            args=(self.smart_link.pk,), data={
                'label': TEST_SMART_LINK_LABEL_EDITED,
                'document_types_pk_list': self.document_type.pk
            }
        )

    def test_smart_link_edit_view_via_put_no_access(self):
        self._create_document_type()
        self.smart_link = self._create_smart_link()
        response = self._request_smart_link_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.smart_link.refresh_from_db()
        self.assertEqual(self.smart_link.label, TEST_SMART_LINK_LABEL)

    def test_smart_link_edit_view_via_put_with_access(self):
        self._create_document_type()
        self.smart_link = self._create_smart_link()
        self.grant_access(
            permission=permission_smart_link_edit, obj=self.smart_link
        )
        response = self._request_smart_link_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.smart_link.refresh_from_db()
        self.assertEqual(self.smart_link.label, TEST_SMART_LINK_LABEL_EDITED)


@override_settings(OCR_AUTO_OCR=False)
class SmartLinkConditionAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(SmartLinkConditionAPITestCase, self).setUp()
        self.login_user()

    def tearDown(self):
        if hasattr(self, 'document_type'):
            self.document_type.delete()
        super(SmartLinkConditionAPITestCase, self).tearDown()

    def _create_document_type(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def _create_document(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def _create_smart_link(self):
        self.smart_link = SmartLink.objects.create(
            label=TEST_SMART_LINK_LABEL,
            dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
        )
        self.smart_link.document_types.add(self.document_type)

    def _create_smart_link_condition(self):
        self.smart_link_condition = SmartLinkCondition.objects.create(
            smart_link=self.smart_link,
            foreign_document_data=TEST_SMART_LINK_CONDITION_FOREIGN_DOCUMENT_DATA,
            expression=TEST_SMART_LINK_CONDITION_EXPRESSION,
            operator=TEST_SMART_LINK_CONDITION_OPERATOR
        )

    def _request_resolved_smart_link_detail_view(self):
        return self.get(
            viewname='rest_api:resolvedsmartlink-detail',
            args=(self.document.pk, self.smart_link.pk)
        )

    def test_resolved_smart_link_detail_view_no_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        response = self._request_resolved_smart_link_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('label' in response.data)

    def test_resolved_smart_link_detail_view_with_document_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        self.grant_access(permission=permission_document_view, obj=self.document)
        response = self._request_resolved_smart_link_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('label' in response.data)

    def test_resolved_smart_link_detail_view_with_smart_link_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        self.grant_access(permission=permission_smart_link_view, obj=self.smart_link)
        response = self._request_resolved_smart_link_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('label' in response.data)

    def test_resolved_smart_link_detail_view_with_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        self.grant_access(permission=permission_smart_link_view, obj=self.smart_link)
        self.grant_access(permission=permission_document_view, obj=self.document)
        response = self._request_resolved_smart_link_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['label'], TEST_SMART_LINK_LABEL
        )

    def _request_resolved_smart_link_list_view(self):
        return self.get(
            viewname='rest_api:resolvedsmartlink-list', args=(self.document.pk,)
        )

    def test_resolved_smart_link_list_view_no_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        response = self._request_resolved_smart_link_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_resolved_smart_link_list_view_with_document_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        self.grant_access(permission=permission_document_view, obj=self.document)
        response = self._request_resolved_smart_link_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_resolved_smart_link_list_view_with_smart_link_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        self.grant_access(permission=permission_smart_link_view, obj=self.smart_link)
        response = self._request_resolved_smart_link_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_resolved_smart_link_list_view_with_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        self.grant_access(permission=permission_smart_link_view, obj=self.smart_link)
        self.grant_access(permission=permission_document_view, obj=self.document)
        response = self._request_resolved_smart_link_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], TEST_SMART_LINK_LABEL
        )

    def _request_resolved_smart_link_document_list_view(self):
        return self.get(
            viewname='rest_api:resolvedsmartlinkdocument-list',
            args=(self.document.pk, self.smart_link.pk)
        )

    def test_resolved_smart_link_document_list_view_no_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        response = self._request_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_resolved_smart_link_document_list_view_with_smart_link_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        self.grant_access(permission=permission_smart_link_view, obj=self.smart_link)
        response = self._request_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_resolved_smart_link_document_list_view_with_document_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        self.grant_access(permission=permission_document_view, obj=self.document)
        response = self._request_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_resolved_smart_link_document_list_view_with_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self._create_document()
        self.grant_access(permission=permission_document_view, obj=self.document)
        self.grant_access(permission=permission_smart_link_view, obj=self.smart_link)
        response = self._request_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], self.document.label
        )

    def _request_smart_link_condition_create_view(self):
        return self.post(
            viewname='rest_api:smartlinkcondition-list',
            args=(self.smart_link.pk,), data={
                'foreign_document_data': TEST_SMART_LINK_CONDITION_FOREIGN_DOCUMENT_DATA,
                'expression': TEST_SMART_LINK_CONDITION_EXPRESSION,
                'operator': TEST_SMART_LINK_CONDITION_OPERATOR
            }
        )

    def test_smart_link_condition_create_view_no_access(self):
        self._create_document_type()
        self._create_smart_link()
        response = self._request_smart_link_condition_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('id' in response.data)

    def test_smart_link_condition_create_view_with_access(self):
        self._create_document_type()
        self._create_smart_link()
        self.grant_access(
            permission=permission_smart_link_edit, obj=self.smart_link
        )
        response = self._request_smart_link_condition_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        smart_link_condition = SmartLinkCondition.objects.first()
        self.assertEqual(response.data['id'], smart_link_condition.pk)
        self.assertEqual(
            response.data['operator'], TEST_SMART_LINK_CONDITION_OPERATOR
        )

        self.assertEqual(SmartLinkCondition.objects.count(), 1)
        self.assertEqual(
            smart_link_condition.operator, TEST_SMART_LINK_CONDITION_OPERATOR
        )

    def _request_smart_link_condition_delete_view(self):
        return self.delete(
            viewname='rest_api:smartlinkcondition-detail',
            args=(self.smart_link.pk, self.smart_link_condition.pk)
        )

    def test_smart_link_condition_delete_view_no_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        response = self._request_smart_link_condition_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(SmartLinkCondition.objects.count(), 1)

    def test_smart_link_condition_delete_view_with_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self.grant_access(
            permission=permission_smart_link_edit, obj=self.smart_link
        )
        response = self._request_smart_link_condition_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SmartLinkCondition.objects.count(), 0)

    def _request_smart_link_condition_detail_view(self):
        return self.get(
            viewname='rest_api:smartlinkcondition-detail',
            args=(self.smart_link.pk, self.smart_link_condition.pk)
        )

    def test_smart_link_condition_detail_view_no_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        response = self._request_smart_link_condition_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('id' in response.data)

    def test_smart_link_condition_detail_view_with_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self.grant_access(
            permission=permission_smart_link_view, obj=self.smart_link
        )
        response = self._request_smart_link_condition_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['operator'], TEST_SMART_LINK_CONDITION_OPERATOR
        )

    def _request_smart_link_condition_edit_view_via_patch(self):
        return self.patch(
            viewname='rest_api:smartlinkcondition-detail',
            args=(self.smart_link.pk, self.smart_link_condition.pk), data={
                'expression': TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED,
            }
        )

    def test_smart_link_condition_patch_view_no_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        response = self._request_smart_link_condition_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.smart_link_condition.refresh_from_db()
        self.assertEqual(
            self.smart_link_condition.expression,
            TEST_SMART_LINK_CONDITION_EXPRESSION
        )

    def test_smart_link_condition_patch_view_with_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self.grant_access(
            permission=permission_smart_link_edit, obj=self.smart_link
        )
        response = self._request_smart_link_condition_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.smart_link_condition.refresh_from_db()
        self.assertEqual(
            self.smart_link_condition.expression,
            TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED
        )

    def _request_smart_link_condition_edit_view_via_put(self):
        return self.put(
            viewname='rest_api:smartlinkcondition-detail',
            args=(self.smart_link.pk, self.smart_link_condition.pk), data={
                'expression': TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED,
                'foreign_document_data': TEST_SMART_LINK_CONDITION_FOREIGN_DOCUMENT_DATA,
                'operator': TEST_SMART_LINK_CONDITION_OPERATOR

            }
        )

    def test_smart_link_condition_put_view_no_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        response = self._request_smart_link_condition_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.smart_link_condition.refresh_from_db()
        self.assertEqual(
            self.smart_link_condition.expression,
            TEST_SMART_LINK_CONDITION_EXPRESSION
        )

    def test_smart_link_condition_put_view_with_access(self):
        self._create_document_type()
        self._create_smart_link()
        self._create_smart_link_condition()
        self.grant_access(
            permission=permission_smart_link_edit, obj=self.smart_link
        )
        response = self._request_smart_link_condition_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.smart_link_condition.refresh_from_db()
        self.assertEqual(
            self.smart_link_condition.expression,
            TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED
        )
