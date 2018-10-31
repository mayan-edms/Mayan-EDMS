from __future__ import unicode_literals

import logging

from django.core.files.base import File

from common.tests import GenericViewTestCase
from documents.models import DocumentType
from documents.permissions import (
    permission_document_properties_edit, permission_document_type_edit,
    permission_document_view
)
from documents.tests import (
    DocumentTestMixin, GenericDocumentViewTestCase,
    TEST_DOCUMENT_TYPE_2_LABEL, TEST_SMALL_DOCUMENT_PATH,
)

from ..models import MetadataType
from ..permissions import (
    permission_metadata_document_add, permission_metadata_document_remove,
    permission_metadata_document_edit, permission_metadata_type_create,
    permission_metadata_type_delete, permission_metadata_type_edit,
    permission_metadata_type_view
)

from .literals import (
    TEST_DOCUMENT_METADATA_VALUE_2, TEST_METADATA_TYPE_LABEL,
    TEST_METADATA_TYPE_LABEL_2, TEST_METADATA_TYPE_LABEL_EDITED,
    TEST_METADATA_TYPE_NAME, TEST_METADATA_TYPE_NAME_2,
    TEST_METADATA_TYPE_NAME_EDITED, TEST_METADATA_VALUE_EDITED
)
from .mixins import MetadataTestsMixin


class DocumentMetadataTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentMetadataTestCase, self).setUp()

        self.metadata_type = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
        )

        self.document_type.metadata.create(metadata_type=self.metadata_type)

    def test_metadata_add_view_no_permission(self):
        self.login_user()

        self.grant_permission(permission=permission_document_view)

        response = self.post(
            'metadata:metadata_add', args=(self.document.pk,),
            data={'metadata_type': self.metadata_type.pk}
        )
        self.assertNotContains(
            response, text=self.metadata_type.label, status_code=200
        )

        self.assertEqual(len(self.document.metadata.all()), 0)

    def test_metadata_add_view_with_permission(self):
        self.login_user()

        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_metadata_document_add)
        self.grant_permission(permission=permission_metadata_document_edit)

        response = self.post(
            'metadata:metadata_add', args=(self.document.pk,),
            data={'metadata_type': self.metadata_type.pk}, follow=True
        )
        self.assertContains(response, 'successfully', status_code=200)

        self.assertEqual(len(self.document.metadata.all()), 1)

    def test_metadata_edit_after_document_type_change(self):
        # Gitlab issue #204
        # Problems to add required metadata after changing the document type

        self.login_user()

        self.grant_permission(permission=permission_document_properties_edit)
        self.grant_permission(permission=permission_metadata_document_edit)

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        metadata_type_2 = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME_2, label=TEST_METADATA_TYPE_LABEL_2
        )

        document_metadata_2 = document_type_2.metadata.create(
            metadata_type=metadata_type_2, required=True
        )

        self.document.set_document_type(document_type=document_type_2)

        response = self.get(
            'metadata:metadata_edit', args=(self.document.pk,), follow=True
        )

        self.assertContains(response, 'Edit', status_code=200)

        response = self.post(
            'metadata:metadata_edit', args=(self.document.pk,), data={
                'form-0-id': document_metadata_2.metadata_type.pk,
                'form-0-update': True,
                'form-0-value': TEST_DOCUMENT_METADATA_VALUE_2,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }, follow=True
        )

        self.assertContains(response, 'Metadata for document', status_code=200)

        self.assertEqual(
            self.document.metadata.get(metadata_type=metadata_type_2).value,
            TEST_DOCUMENT_METADATA_VALUE_2
        )

    def test_metadata_remove_view_no_permission(self):
        self.login_user()

        document_metadata = self.document.metadata.create(
            metadata_type=self.metadata_type, value=''
        )

        self.assertEqual(len(self.document.metadata.all()), 1)

        self.grant_permission(permission=permission_document_view)

        # Test display of metadata removal form
        response = self.get(
            'metadata:metadata_remove', args=(self.document.pk,),
        )

        self.assertNotContains(
            response, text=self.metadata_type.label, status_code=200
        )

        # Test post to metadata removal view
        response = self.post(
            'metadata:metadata_remove', args=(self.document.pk,), data={
                'form-0-id': document_metadata.metadata_type.pk,
                'form-0-update': True,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }, follow=True
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(self.document.metadata.all()), 1)

    def test_metadata_remove_view_with_permission(self):
        # Silence unrelated logging
        logging.getLogger('navigation.classes').setLevel(logging.CRITICAL)

        self.login_user()

        document_metadata = self.document.metadata.create(
            metadata_type=self.metadata_type, value=''
        )

        self.assertEqual(len(self.document.metadata.all()), 1)

        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_metadata_document_remove)

        # Test display of metadata removal form
        response = self.get(
            'metadata:metadata_remove', args=(self.document.pk,),
        )

        self.assertContains(
            response, text=self.metadata_type.label, status_code=200
        )

        self.assertContains(response, 'emove', status_code=200)

        # Test post to metadata removal view
        response = self.post(
            'metadata:metadata_remove', args=(self.document.pk,), data={
                'form-0-id': document_metadata.metadata_type.pk,
                'form-0-update': True,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }, follow=True
        )

        self.assertContains(response, 'Success', status_code=200)

        self.assertEqual(len(self.document.metadata.all()), 0)

    def test_multiple_document_metadata_edit(self):
        self.login_user()

        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_metadata_document_add)
        self.grant_permission(permission=permission_metadata_document_edit)

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            document_2 = self.document_type.new_document(
                file_object=File(file_object)
            )

        document_metadata = self.document.metadata.create(
            metadata_type=self.metadata_type
        )
        document_2.metadata.create(metadata_type=self.metadata_type)

        response = self.get(
            'metadata:metadata_multiple_edit', data={
                'id_list': '{},{}'.format(self.document.pk, document_2.pk)
            }
        )

        self.assertContains(response, 'Edit', status_code=200)

        # Test post to metadata removal view
        response = self.post(
            'metadata:metadata_multiple_edit', data={
                'id_list': '{},{}'.format(self.document.pk, document_2.pk),
                'form-0-id': document_metadata.metadata_type.pk,
                'form-0-value': TEST_METADATA_VALUE_EDITED,
                'form-0-update': True,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.document.metadata.first().value, TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            document_2.metadata.first().value, TEST_METADATA_VALUE_EDITED
        )

    def test_multiple_document_metadata_remove(self):
        self.login_user()

        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_metadata_document_remove)

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            document_2 = self.document_type.new_document(
                file_object=File(file_object)
            )

        document_metadata = self.document.metadata.create(
            metadata_type=self.metadata_type
        )
        document_2.metadata.create(metadata_type=self.metadata_type)

        response = self.get(
            'metadata:metadata_multiple_remove', data={
                'id_list': '{},{}'.format(self.document.pk, document_2.pk)
            }
        )

        self.assertEquals(response.status_code, 200)

        # Test post to metadata removal view
        response = self.post(
            'metadata:metadata_multiple_remove', data={
                'id_list': '{},{}'.format(self.document.pk, document_2.pk),
                'form-0-id': document_metadata.metadata_type.pk,
                'form-0-update': True,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }, follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.document.metadata.count(), 0)
        self.assertEqual(document_2.metadata.count(), 0)

    def test_multiple_document_metadata_add(self):
        self.login_user()

        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_metadata_document_add)
        self.grant_permission(permission=permission_metadata_document_edit)

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            document_2 = self.document_type.new_document(
                file_object=File(file_object)
            )

        response = self.post(
            'metadata:metadata_multiple_add', data={
                'id_list': '{},{}'.format(self.document.pk, document_2.pk),
                'metadata_type': self.metadata_type.pk
            }, follow=True
        )

        self.assertContains(response, 'Edit', status_code=200)

    def test_single_document_multiple_metadata_add_view(self):
        self.login_user()

        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_metadata_document_add)
        self.grant_permission(permission=permission_metadata_document_edit)

        metadata_type_2 = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME_2, label=TEST_METADATA_TYPE_LABEL_2
        )

        self.document_type.metadata.create(
            metadata_type=metadata_type_2
        )

        self.post(
            'metadata:metadata_add', args=(self.document.pk,), data={
                'metadata_type': [self.metadata_type.pk, metadata_type_2.pk],
            }
        )

        document_metadata_types = self.document.metadata.values_list(
            'metadata_type', flat=True
        )
        self.assertTrue(
            self.metadata_type.pk in document_metadata_types and
            metadata_type_2.pk in document_metadata_types
        )


class MetadataTypeViewTestCase(DocumentTestMixin, MetadataTestsMixin, GenericViewTestCase):
    auto_create_document_type = False
    auto_upload_document = False

    def test_metadata_type_create_view_no_permission(self):
        self.login_user()

        response = self._request_metadata_type_create_view()

        self.assertEqual(response.status_code, 403)

    def test_metadata_type_create_view_with_access(self):
        self.login_user()

        self.grant_permission(permission=permission_metadata_type_create)
        response = self._request_metadata_type_create_view()

        self.assertEqual(response.status_code, 302)

        self.assertQuerysetEqual(
            qs=MetadataType.objects.values('label', 'name'),
            values=[
                {
                    'label': TEST_METADATA_TYPE_LABEL,
                    'name': TEST_METADATA_TYPE_NAME
                }
            ], transform=dict
        )

    def test_metadata_type_delete_view_no_permission(self):
        self.login_user()
        self._create_metadata_type()

        response = self._request_metadata_type_delete_view()

        self.assertEqual(response.status_code, 403)
        self.assertQuerysetEqual(
            qs=MetadataType.objects.values('label', 'name'),
            values=[
                {
                    'label': TEST_METADATA_TYPE_LABEL,
                    'name': TEST_METADATA_TYPE_NAME
                }
            ], transform=dict
        )

    def test_metadata_type_delete_view_with_access(self):
        self.login_user()
        self._create_metadata_type()

        self.grant_access(
            permission=permission_metadata_type_delete,
            obj=self.metadata_type
        )
        response = self._request_metadata_type_delete_view()

        self.assertEqual(response.status_code, 302)

        self.assertEqual(MetadataType.objects.count(), 0)

    def test_metadata_type_edit_view_no_permission(self):
        self.login_user()
        self._create_metadata_type()

        response = self._request_metadata_type_edit_view()

        self.assertEqual(response.status_code, 403)
        self.assertQuerysetEqual(
            qs=MetadataType.objects.values('label', 'name'),
            values=[
                {
                    'label': TEST_METADATA_TYPE_LABEL,
                    'name': TEST_METADATA_TYPE_NAME
                }
            ], transform=dict
        )

    def test_metadata_type_edit_view_with_access(self):
        self.login_user()
        self._create_metadata_type()

        self.grant_access(
            permission=permission_metadata_type_edit,
            obj=self.metadata_type
        )
        response = self._request_metadata_type_edit_view()

        self.assertEqual(response.status_code, 302)

        self.assertQuerysetEqual(
            qs=MetadataType.objects.values('label', 'name'),
            values=[
                {
                    'label': TEST_METADATA_TYPE_LABEL_EDITED,
                    'name': TEST_METADATA_TYPE_NAME_EDITED
                }
            ], transform=dict
        )

    def test_metadata_type_list_view_no_permission(self):
        self.login_user()
        self._create_metadata_type()

        response = self._request_metadata_type_list_view()
        self.assertNotContains(
            response=response, text=self.metadata_type, status_code=200
        )

    def test_metadata_type_list_view_with_access(self):
        self.login_user()
        self._create_metadata_type()

        self.grant_access(
            permission=permission_metadata_type_view,
            obj=self.metadata_type
        )
        response = self._request_metadata_type_list_view()
        self.assertContains(
            response=response, text=self.metadata_type, status_code=200
        )

    def test_metadata_type_relationship_view_no_permission(self):
        self.login_user()
        self._create_metadata_type()
        self._create_document_type()
        self.upload_document()

        response = self._request_metadata_type_relationship_edit_view()

        self.assertEqual(response.status_code, 403)

        self.document_type.refresh_from_db()

        self.assertEqual(self.document_type.metadata.count(), 0)

    def test_metadata_type_relationship_view_with_document_type_access(self):
        self.login_user()
        self._create_metadata_type()
        self._create_document_type()
        self.upload_document()

        self.grant_access(
            permission=permission_document_type_edit, obj=self.document_type
        )

        response = self._request_metadata_type_relationship_edit_view()

        self.assertEqual(response.status_code, 403)

        self.document_type.refresh_from_db()

        self.assertEqual(self.document_type.metadata.count(), 0)

    def test_metadata_type_relationship_view_with_metadata_type_access(self):
        self.login_user()
        self._create_metadata_type()
        self._create_document_type()
        self.upload_document()

        self.grant_access(
            permission=permission_metadata_type_edit, obj=self.metadata_type
        )

        response = self._request_metadata_type_relationship_edit_view()

        self.assertEqual(response.status_code, 302)

        self.document_type.refresh_from_db()

        self.assertEqual(self.document_type.metadata.count(), 0)

    def test_metadata_type_relationship_view_with_metadata_type_and_document_type_access(self):
        self.login_user()
        self._create_metadata_type()
        self._create_document_type()
        self.upload_document()

        self.grant_access(
            permission=permission_metadata_type_edit, obj=self.metadata_type
        )
        self.grant_access(
            permission=permission_document_type_edit, obj=self.document_type
        )

        response = self._request_metadata_type_relationship_edit_view()

        self.assertEqual(response.status_code, 302)

        self.document_type.refresh_from_db()

        self.assertQuerysetEqual(
            qs=self.document_type.metadata.values('metadata_type', 'required'),
            values=[
                {
                    'metadata_type': self.metadata_type.pk,
                    'required': True,
                }
            ], transform=dict
        )
