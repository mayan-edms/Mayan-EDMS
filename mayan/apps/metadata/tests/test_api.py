from __future__ import unicode_literals

from django.test import override_settings

from rest_framework import status

from documents.models import DocumentType
from documents.permissions import (
    permission_document_type_edit, permission_document_type_view
)
from documents.tests import TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_PATH
from rest_api.tests import BaseAPITestCase

from ..models import DocumentTypeMetadataType, MetadataType
from ..permissions import (
    permission_metadata_document_add, permission_metadata_document_edit,
    permission_metadata_document_remove, permission_metadata_document_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)

from .literals import (
    TEST_METADATA_TYPE_LABEL, TEST_METADATA_TYPE_LABEL_2,
    TEST_METADATA_TYPE_NAME, TEST_METADATA_TYPE_NAME_2, TEST_METADATA_VALUE,
    TEST_METADATA_VALUE_EDITED
)


class MetadataTypeAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(MetadataTypeAPITestCase, self).setUp()
        self.login_user()

    def _create_metadata_type(self):
        self.metadata_type = MetadataType.objects.create(
            label=TEST_METADATA_TYPE_LABEL, name=TEST_METADATA_TYPE_NAME
        )

    def _request_metadata_type_create_view(self):
        return self.post(
            viewname='rest_api:metadatatype-list', data={
                'label': TEST_METADATA_TYPE_LABEL,
                'name': TEST_METADATA_TYPE_NAME
            }
        )

    def test_metadata_type_create_no_permission(self):
        response = self._request_metadata_type_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MetadataType.objects.count(), 0)

    def test_metadata_type_create_with_permission(self):
        self.grant_permission(permission=permission_metadata_type_create)
        response = self._request_metadata_type_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        metadata_type = MetadataType.objects.first()
        self.assertEqual(response.data['id'], metadata_type.pk)
        self.assertEqual(response.data['label'], TEST_METADATA_TYPE_LABEL)
        self.assertEqual(response.data['name'], TEST_METADATA_TYPE_NAME)

        self.assertEqual(metadata_type.label, TEST_METADATA_TYPE_LABEL)
        self.assertEqual(metadata_type.name, TEST_METADATA_TYPE_NAME)

    def _request_metadata_type_delete_view(self):
        return self.delete(
            viewname='rest_api:metadatatype-detail',
            args=(self.metadata_type.pk,)
        )

    def test_metadata_type_delete_no_access(self):
        self._create_metadata_type()
        response = self._request_metadata_type_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MetadataType.objects.count(), 1)

    def test_metadata_type_delete_with_access(self):
        self._create_metadata_type()
        self.grant_access(
            permission=permission_metadata_type_delete, obj=self.metadata_type
        )
        response = self._request_metadata_type_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MetadataType.objects.count(), 0)

    def _request_metadata_type_detail_view(self):
        return self.get(
            viewname='rest_api:metadatatype-detail',
            args=(self.metadata_type.pk,)
        )

    def test_metadata_type_detail_view_no_access(self):
        self._create_metadata_type()
        response = self._request_metadata_type_detail_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_metadata_type_detail_view_with_access(self):
        self._create_metadata_type()
        self.grant_access(
            permission=permission_metadata_type_view, obj=self.metadata_type
        )
        response = self._request_metadata_type_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['label'], TEST_METADATA_TYPE_LABEL
        )

    def _request_metadata_type_edit_view_via_patch(self):
        return self.patch(
            viewname='rest_api:metadatatype-detail',
            args=(self.metadata_type.pk,), data={
                'label': TEST_METADATA_TYPE_LABEL_2,
                'name': TEST_METADATA_TYPE_NAME_2
            }
        )

    def test_metadata_type_patch_view_no_access(self):
        self._create_metadata_type()
        response = self._request_metadata_type_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.metadata_type.refresh_from_db()
        self.assertEqual(self.metadata_type.label, TEST_METADATA_TYPE_LABEL)
        self.assertEqual(self.metadata_type.name, TEST_METADATA_TYPE_NAME)

    def test_metadata_type_patch_view_with_access(self):
        self._create_metadata_type()
        self.grant_access(
            permission=permission_metadata_type_edit, obj=self.metadata_type
        )
        response = self._request_metadata_type_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.metadata_type.refresh_from_db()
        self.assertEqual(self.metadata_type.label, TEST_METADATA_TYPE_LABEL_2)
        self.assertEqual(self.metadata_type.name, TEST_METADATA_TYPE_NAME_2)

    def _request_metadata_type_edit_view_via_put(self):
        return self.put(
            viewname='rest_api:metadatatype-detail',
            args=(self.metadata_type.pk,), data={
                'label': TEST_METADATA_TYPE_LABEL_2,
                'name': TEST_METADATA_TYPE_NAME_2
            }
        )

    def test_metadata_type_put_view_no_access(self):
        self._create_metadata_type()
        response = self._request_metadata_type_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.metadata_type.refresh_from_db()
        self.assertEqual(self.metadata_type.label, TEST_METADATA_TYPE_LABEL)
        self.assertEqual(self.metadata_type.name, TEST_METADATA_TYPE_NAME)

    def test_metadata_type_put_view_with_access(self):
        self._create_metadata_type()
        self.grant_access(
            permission=permission_metadata_type_edit, obj=self.metadata_type
        )
        response = self._request_metadata_type_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.metadata_type.refresh_from_db()
        self.assertEqual(self.metadata_type.label, TEST_METADATA_TYPE_LABEL_2)
        self.assertEqual(self.metadata_type.name, TEST_METADATA_TYPE_NAME_2)

    def _request_metadata_type_list_view(self):
        return self.get(viewname='rest_api:metadatatype-list')

    def test_metadata_type_list_view_no_access(self):
        self._create_metadata_type()
        response = self._request_metadata_type_list_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_metadata_type_list_view_with_access(self):
        self._create_metadata_type()
        self.grant_access(
            permission=permission_metadata_type_view, obj=self.metadata_type
        )
        response = self._request_metadata_type_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], TEST_METADATA_TYPE_LABEL
        )


class DocumentTypeMetadataTypeAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(DocumentTypeMetadataTypeAPITestCase, self).setUp()
        self.login_user()

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        self.metadata_type = MetadataType.objects.create(
            label=TEST_METADATA_TYPE_LABEL, name=TEST_METADATA_TYPE_NAME
        )

    def tearDown(self):
        self.document_type.delete()
        super(DocumentTypeMetadataTypeAPITestCase, self).tearDown()

    def _create_document_type_metadata_type(self):
        self.document_type_metadata_type = self.document_type.metadata.create(
            metadata_type=self.metadata_type, required=False
        )

    def _request_document_type_metadata_type_create_view(self):
        return self.post(
            viewname='rest_api:documenttypemetadatatype-list',
            args=(self.document_type.pk,), data={
                'metadata_type_pk': self.metadata_type.pk, 'required': False
            }
        )

    def test_document_type_metadata_type_create_view_no_access(self):
        response = self._request_document_type_metadata_type_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.document_type.metadata.count(), 0)

    def test_document_type_metadata_type_create_view_with_access(self):
        self.grant_access(
            permission=permission_document_type_edit, obj=self.document_type
        )
        response = self._request_document_type_metadata_type_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertEqual(response.data['id'], document_type_metadata_type.pk)

    def test_document_type_metadata_type_create_dupicate_view(self):
        self._create_document_type_metadata_type()
        self.grant_permission(permission=permission_document_type_edit)
        response = self._request_document_type_metadata_type_create_view()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys()[0], 'non_field_errors')

    def _request_document_type_metadata_type_delete_view(self):
        return self.delete(
            viewname='rest_api:documenttypemetadatatype-detail',
            args=(
                self.document_type.pk, self.document_type_metadata_type.pk,
            ),
        )

    def test_document_type_metadata_type_delete_view_no_access(self):
        self._create_document_type_metadata_type()
        response = self._request_document_type_metadata_type_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.document_type.metadata.count(), 1)

    def test_document_type_metadata_type_delete_view_with_access(self):
        self._create_document_type_metadata_type()
        self.grant_access(permission=permission_document_type_edit, obj=self.document_type)
        response = self._request_document_type_metadata_type_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.document_type.metadata.all().count(), 0)

    def _request_document_type_metadata_type_list_view(self):
        return self.get(
            viewname='rest_api:documenttypemetadatatype-list',
            args=(
                self.document_type.pk,
            ),
        )

    def test_document_type_metadata_type_list_view_no_access(self):
        self._create_document_type_metadata_type()
        response = self._request_document_type_metadata_type_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_type_metadata_type_list_view_with_access(self):
        self._create_document_type_metadata_type()
        self.grant_access(permission=permission_document_type_view, obj=self.document_type)
        response = self._request_document_type_metadata_type_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['id'],
            self.document_type_metadata_type.pk
        )

    def _request_document_type_metadata_type_edit_view_via_patch(self):
        return self.patch(
            viewname='rest_api:documenttypemetadatatype-detail',
            args=(
                self.document_type.pk, self.document_type_metadata_type.pk,
            ), data={
                'required': True
            }
        )

    def test_document_type_metadata_type_patch_view_no_access(self):
        self._create_document_type_metadata_type()
        response = self._request_document_type_metadata_type_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

    def test_document_type_metadata_type_patch_view_with_access(self):
        self._create_document_type_metadata_type()
        self.grant_access(permission=permission_document_type_edit, obj=self.document_type)
        response = self._request_document_type_metadata_type_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertEqual(document_type_metadata_type.required, True)

    def _request_document_type_metadata_type_edit_view_via_put(self):
        return self.put(
            viewname='rest_api:documenttypemetadatatype-detail',
            args=(
                self.document_type.pk, self.document_type_metadata_type.pk,
            ), data={
                'required': True
            }
        )

    def test_document_type_metadata_type_put_view_no_access(self):
        self._create_document_type_metadata_type()
        response = self._request_document_type_metadata_type_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

    def test_document_type_metadata_type_put_view_with_access(self):
        self._create_document_type_metadata_type()
        self.grant_access(permission=permission_document_type_edit, obj=self.document_type)
        response = self._request_document_type_metadata_type_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertEqual(document_type_metadata_type.required, True)


class DocumentMetadataAPITestCase(BaseAPITestCase):
    @override_settings(OCR_AUTO_OCR=False)
    def setUp(self):
        super(DocumentMetadataAPITestCase, self).setUp()
        self.login_user()

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        self.metadata_type = MetadataType.objects.create(
            label=TEST_METADATA_TYPE_LABEL, name=TEST_METADATA_TYPE_NAME
        )

        self.document_type.metadata.create(
            metadata_type=self.metadata_type, required=False
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object,
            )

    def tearDown(self):
        self.document_type.delete()
        super(DocumentMetadataAPITestCase, self).tearDown()

    def _create_document_metadata(self):
        self.document_metadata = self.document.metadata.create(
            metadata_type=self.metadata_type, value=TEST_METADATA_VALUE
        )

    def _request_document_metadata_create_view(self):
        return self.post(
            viewname='rest_api:documentmetadata-list',
            args=(self.document.pk,), data={
                'metadata_type_pk': self.metadata_type.pk,
                'value': TEST_METADATA_VALUE
            }
        )

    def test_document_metadata_create_view_no_access(self):
        response = self._request_document_metadata_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.document.metadata.count(), 0)

    def test_document_metadata_create_view_with_access(self):
        self.grant_access(permission=permission_metadata_document_add, obj=self.document)
        response = self._request_document_metadata_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        document_metadata = self.document.metadata.first()
        self.assertEqual(response.data['id'], document_metadata.pk)
        self.assertEqual(document_metadata.metadata_type, self.metadata_type)
        self.assertEqual(document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_create_duplicate_view(self):
        self._create_document_metadata()
        self.grant_permission(permission=permission_metadata_document_add)
        response = self._request_document_metadata_create_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys()[0], 'non_field_errors')

    def test_document_metadata_create_invalid_lookup_value_view(self):
        self.metadata_type.lookup = 'invalid,lookup,values,on,purpose'
        self.metadata_type.save()
        self.grant_permission(permission=permission_metadata_document_add)
        response = self._request_document_metadata_create_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys()[0], 'non_field_errors')

    def _request_document_metadata_delete_view(self):
        return self.delete(
            viewname='rest_api:documentmetadata-detail',
            args=(self.document.pk, self.document_metadata.pk,)
        )

    def test_document_metadata_delete_view_no_access(self):
        self._create_document_metadata()
        response = self._request_document_metadata_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.document.metadata.all().count(), 1)

    def test_document_metadata_delete_view_with_access(self):
        self._create_document_metadata()
        self.grant_access(
            permission=permission_metadata_document_remove, obj=self.document
        )
        response = self._request_document_metadata_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.document.metadata.all().count(), 0)

    def _request_document_metadata_list_view(self):
        return self.get(
            viewname='rest_api:documentmetadata-list', args=(
                self.document.pk,
            )
        )

    def test_document_metadata_list_view_no_access(self):
        self._create_document_metadata()
        response = self._request_document_metadata_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_metadata_list_view_with_access(self):
        self._create_document_metadata()
        self.grant_access(
            permission=permission_metadata_document_view, obj=self.document
        )
        response = self._request_document_metadata_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['document']['id'], self.document.pk
        )
        self.assertEqual(
            response.data['results'][0]['metadata_type']['id'],
            self.metadata_type.pk
        )
        self.assertEqual(
            response.data['results'][0]['value'], TEST_METADATA_VALUE
        )
        self.assertEqual(
            response.data['results'][0]['id'], self.document_metadata.pk
        )

    def _request_document_metadata_edit_view_via_patch(self):
        return self.patch(
            viewname='rest_api:documentmetadata-detail',
            args=(self.document.pk, self.document_metadata.pk,), data={
                'value': TEST_METADATA_VALUE_EDITED
            }
        )

    def test_document_metadata_patch_view_no_access(self):
        self._create_document_metadata()
        response = self._request_document_metadata_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.document_metadata.refresh_from_db()
        self.assertEqual(self.document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_patch_view_with_access(self):
        self._create_document_metadata()
        self.grant_access(
            permission=permission_metadata_document_edit, obj=self.document
        )
        response = self._request_document_metadata_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document_metadata.refresh_from_db()
        self.assertEqual(
            response.data['value'], TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.document_metadata.value, TEST_METADATA_VALUE_EDITED
        )

    def _request_document_metadata_edit_view_via_put(self):
        return self.put(
            viewname='rest_api:documentmetadata-detail',
            args=(self.document.pk, self.document_metadata.pk,), data={
                'value': TEST_METADATA_VALUE_EDITED
            }
        )

    def test_document_metadata_put_view_no_access(self):
        self._create_document_metadata()
        response = self._request_document_metadata_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.document_metadata.refresh_from_db()
        self.assertEqual(self.document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_put_view_with_access(self):
        self._create_document_metadata()
        self.grant_access(
            permission=permission_metadata_document_edit, obj=self.document
        )
        response = self._request_document_metadata_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document_metadata.refresh_from_db()
        self.assertEqual(
            response.data['value'], TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.document_metadata.value, TEST_METADATA_VALUE_EDITED
        )
