from __future__ import unicode_literals

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.documents.models import DocumentType
from mayan.apps.documents.permissions import (
    permission_document_properties_edit, permission_document_type_edit,
    permission_document_view
)
from mayan.apps.documents.tests import (
    DocumentTestMixin, GenericDocumentViewTestCase, TEST_DOCUMENT_TYPE_2_LABEL
)

from ..models import MetadataType
from ..permissions import (
    permission_document_metadata_add, permission_document_metadata_remove,
    permission_document_metadata_edit, permission_metadata_type_create,
    permission_metadata_type_delete, permission_metadata_type_edit,
    permission_metadata_type_view
)

from .literals import (
    TEST_DOCUMENT_METADATA_VALUE_2, TEST_METADATA_TYPE_LABEL,
    TEST_METADATA_TYPE_LABEL_2, TEST_METADATA_TYPE_NAME,
    TEST_METADATA_TYPE_NAME_2, TEST_METADATA_VALUE_EDITED
)
from .mixins import MetadataTypeTestMixin, MetadataTestMixin


class DocumentMetadataTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentMetadataTestCase, self).setUp()

        self.test_metadata_type = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
        )

        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

    def _request_test_document_metadata_add_post_view(self):
        return self.post(
            viewname='metadata:metadata_add', kwargs={
                'pk': self.test_document.pk
            }, data={'metadata_type': self.test_metadata_type.pk}
        )

    def test_document_metadata_add_post_view_no_permission(self):
        response = self._request_test_document_metadata_add_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document.metadata.count(), 0)

    def test_document_metadata_add_post_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_metadata_add
        )

        response = self._request_test_document_metadata_add_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document.metadata.count(), 1)

    def _request_test_document_multiple_metadata_add_post_view(self):
        return self.post(
            viewname='metadata:metadata_multiple_add', data={
                'id_list': '{},{}'.format(
                    self.test_documents[0].pk, self.test_documents[1].pk
                ),
                'metadata_type': self.test_metadata_type.pk
            }
        )

    def test_document_multiple_metadata_add_post_view_with_document_access(self):
        self.upload_document()

        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_metadata_add
        )

        response = self._request_test_document_multiple_metadata_add_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_documents[0].metadata.count(), 1)
        self.assertEqual(self.test_documents[1].metadata.count(), 1)

    def test_single_document_multiple_metadata_add_view(self):
        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_document_metadata_add)
        self.grant_permission(permission=permission_document_metadata_edit)

        metadata_type_2 = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME_2, label=TEST_METADATA_TYPE_LABEL_2
        )

        self.test_document_type.metadata.create(
            metadata_type=metadata_type_2
        )

        self.post(
            viewname='metadata:metadata_add', kwargs={
                'pk': self.test_document.pk
            }, data={
                'metadata_type': [self.test_metadata_type.pk, metadata_type_2.pk],
            }
        )

        document_metadata_types = self.test_document.metadata.values_list(
            'metadata_type', flat=True
        )
        self.assertTrue(
            self.test_metadata_type.pk in document_metadata_types
        )
        self.assertTrue(
            metadata_type_2.pk in document_metadata_types
        )

    def test_metadata_edit_after_document_type_change(self):
        # Gitlab issue #204
        # Problems to add required metadata after changing the document type

        self.grant_permission(permission=permission_document_properties_edit)
        self.grant_permission(permission=permission_document_metadata_edit)

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        metadata_type_2 = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME_2, label=TEST_METADATA_TYPE_LABEL_2
        )

        document_metadata_2 = document_type_2.metadata.create(
            metadata_type=metadata_type_2, required=True
        )

        self.test_document.set_document_type(document_type=document_type_2)

        response = self.get(
            viewname='metadata:metadata_edit', kwargs={
                'pk': self.test_document.pk
            }, follow=True
        )
        self.assertContains(response=response, text='Edit', status_code=200)

        response = self.post(
            'metadata:metadata_edit', kwargs={'pk': self.test_document.pk},
            data={
                'form-0-id': document_metadata_2.metadata_type.pk,
                'form-0-update': True,
                'form-0-value': TEST_DOCUMENT_METADATA_VALUE_2,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }, follow=True
        )
        self.assertContains(
            response=response, text='Metadata for document', status_code=200
        )

        self.assertEqual(
            self.test_document.metadata.get(metadata_type=metadata_type_2).value,
            TEST_DOCUMENT_METADATA_VALUE_2
        )

    def _request_document_metadata_remove_get_view(self):
        return self.get(
            viewname='metadata:metadata_remove',
            kwargs={'pk': self.test_document.pk}
        )

    def _create_test_document_metadata(self):
        self.test_document_metadata = self.test_document.metadata.create(
            metadata_type=self.test_metadata_type, value=''
        )

    def test_document_metadata_remove_get_view_no_permission(self):
        self._create_test_document_metadata()

        response = self._request_document_metadata_remove_get_view()

        self.assertNotContains(
            response=response, text=self.test_metadata_type.label, status_code=404
        )
        self.assertTrue(
            self.test_document_metadata in self.test_document.metadata.all()
        )

    def test_document_metadata_remove_get_view_with_full_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document, permission=permission_document_metadata_remove,
        )

        # Silence unrelated logging
        self._silence_logger(name='mayan.apps.navigation.classes')

        response = self._request_document_metadata_remove_get_view()
        self.assertContains(
            response, text=self.test_metadata_type.label, status_code=200
        )
        self.assertTrue(
            self.test_document_metadata in self.test_document.metadata.all()
        )

    def _request_document_metadata_remove_post_view(self):
        return self.post(
            viewname='metadata:metadata_remove',
            kwargs={'pk': self.test_document.pk}, data={
                'form-0-id': self.test_document_metadata.metadata_type.pk,
                'form-0-update': True,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }
        )

    def test_document_metadata_remove_post_view_no_permission(self):
        self._create_test_document_metadata()

        response = self._request_document_metadata_remove_post_view()
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label, status_code=404
        )

        self.assertTrue(
            self.test_document_metadata in self.test_document.metadata.all()
        )

    def test_document_metadata_remove_post_view_with_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        response = self._request_document_metadata_remove_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_document_metadata not in self.test_document.metadata.all()
        )

    def test_document_multiple_metadata_remove_view_with_access(self):
        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_document_metadata_remove)

        self.upload_document()

        document_metadata = self.test_documents[0].metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.test_documents[1].metadata.create(metadata_type=self.test_metadata_type)

        response = self.get(
            viewname='metadata:metadata_multiple_remove', data={
                'id_list': '{},{}'.format(
                    self.test_documents[0].pk, self.test_documents[0].pk
                )
            }
        )
        self.assertEquals(response.status_code, 200)

        # Test post to metadata removal view
        response = self.post(
            viewname='metadata:metadata_multiple_remove', data={
                'id_list': '{},{}'.format(
                    self.test_documents[0].pk, self.test_documents[1].pk
                ),
                'form-0-id': document_metadata.metadata_type.pk,
                'form-0-update': True,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_documents[0].metadata.count(), 0)
        self.assertEqual(self.test_documents[1].metadata.count(), 0)

    def test_multiple_document_metadata_edit(self):
        self.upload_document()

        self.grant_permission(permission=permission_document_view)
        self.grant_permission(permission=permission_document_metadata_add)
        self.grant_permission(permission=permission_document_metadata_edit)

        document_metadata = self.test_documents[0].metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.test_documents[1].metadata.create(
            metadata_type=self.test_metadata_type
        )

        response = self.get(
            viewname='metadata:metadata_multiple_edit', data={
                'id_list': '{},{}'.format(
                    self.test_documents[0].pk, self.test_documents[1].pk
                )
            }
        )
        self.assertContains(response=response, text='Edit', status_code=200)

        # Test post to metadata removal view
        response = self.post(
            viewname='metadata:metadata_multiple_edit', data={
                'id_list': '{},{}'.format(
                    self.test_documents[0].pk, self.test_documents[1].pk
                ),
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
            self.test_documents[0].metadata.first().value, TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.test_documents[1].metadata.first().value, TEST_METADATA_VALUE_EDITED
        )


class MetadataTypeViewTestCase(
    DocumentTestMixin, MetadataTestMixin, MetadataTypeTestMixin,
    GenericViewTestCase
):
    auto_create_document_type = False
    auto_upload_document = False

    def test_metadata_type_create_view_no_permission(self):
        metadata_type_count = MetadataType.objects.count()

        response = self._request_test_metadata_type_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count
        )

    def test_metadata_type_create_view_with_access(self):
        self.grant_permission(permission=permission_metadata_type_create)
        metadata_type_count = MetadataType.objects.count()

        response = self._request_test_metadata_type_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count + 1
        )

    def test_metadata_type_delete_view_no_permission(self):
        self._create_test_metadata_type()
        metadata_type_count = MetadataType.objects.count()

        response = self._request_test_metadata_type_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count
        )

    def test_metadata_type_delete_view_with_access(self):
        self._create_test_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_delete
        )
        metadata_type_count = MetadataType.objects.count()

        response = self._request_test_metadata_type_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            MetadataType.objects.count(), metadata_type_count - 1
        )

    def test_metadata_type_edit_view_no_permission(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )

        response = self._request_test_metadata_type_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

    def test_metadata_type_edit_view_with_access(self):
        self._create_test_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )

        response = self._request_test_metadata_type_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_metadata_type.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

    def test_metadata_type_list_view_no_permission(self):
        self._create_test_metadata_type()

        response = self._request_metadata_type_list_view()
        self.assertNotContains(
            response=response, text=self.test_metadata_type, status_code=200
        )

    def test_metadata_type_list_view_with_access(self):
        self._create_test_metadata_type()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        response = self._request_metadata_type_list_view()
        self.assertContains(
            response=response, text=self.test_metadata_type, status_code=200
        )

    def test_metadata_type_relationship_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_document_type()
        self.upload_document()

        response = self._request_test_metadata_type_relationship_edit_view()
        self.assertEqual(response.status_code, 403)

        self.test_document_type.refresh_from_db()
        self.assertEqual(self.test_document_type.metadata.count(), 0)

    def test_metadata_type_relationship_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_document_type()
        self.upload_document()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_metadata_type_relationship_edit_view()
        self.assertEqual(response.status_code, 403)

        self.test_document_type.refresh_from_db()
        self.assertEqual(self.test_document_type.metadata.count(), 0)

    def test_metadata_type_relationship_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_document_type()
        self.upload_document()

        self.grant_access(
            obj=self.test_metadata_type, permission=permission_metadata_type_edit
        )

        response = self._request_test_metadata_type_relationship_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertEqual(self.test_document_type.metadata.count(), 0)

    def test_metadata_type_relationship_view_with_metadata_type_and_document_type_access(self):
        self._create_test_metadata_type()
        self._create_document_type()
        self.upload_document()

        self.grant_access(
            obj=self.test_metadata_type, permission=permission_metadata_type_edit
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_test_metadata_type_relationship_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_type.refresh_from_db()
        self.assertQuerysetEqual(
            qs=self.test_document_type.metadata.values('metadata_type', 'required'),
            values=[
                {
                    'metadata_type': self.test_metadata_type.pk,
                    'required': True,
                }
            ], transform=dict
        )
