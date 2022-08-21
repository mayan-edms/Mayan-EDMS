from django.db.models import Q
from django.urls import reverse

from mayan.apps.documents.tests.literals import TEST_FILE_SMALL_PATH
from mayan.apps.views.http import URL

from ..models import DocumentMetadata, DocumentTypeMetadataType, MetadataType

from .literals import (
    TEST_METADATA_TYPE_LABEL, TEST_METADATA_TYPE_LABEL_EDITED,
    TEST_METADATA_TYPE_NAME, TEST_METADATA_TYPE_NAME_EDITED,
    TEST_METADATA_VALUE, TEST_METADATA_VALUE_EDITED
)


class DocumentMetadataAPIViewTestMixin:
    def _request_document_metadata_create_api_view(self, extra_data=None):
        pk_list = list(DocumentMetadata.objects.values_list('pk', flat=True))

        data = {
            'metadata_type_id': self._test_metadata_type.pk,
            'value': TEST_METADATA_VALUE
        }
        data.update(extra_data or {})

        response = self.post(
            viewname='rest_api:documentmetadata-list',
            kwargs={'document_id': self._test_document.pk}, data=data
        )

        try:
            self._test_document_metadata = DocumentMetadata.objects.get(
                ~Q(pk__in=pk_list)
            )
        except DocumentMetadata.DoesNotExist:
            self._test_document_metadata = None

        return response

    def _request_document_metadata_delete_api_view(self):
        return self.delete(
            viewname='rest_api:documentmetadata-detail',
            kwargs={
                'document_id': self._test_document.pk,
                'metadata_id': self._test_document_metadata.pk
            }
        )

    def _request_document_metadata_edit_api_view_via_patch(self, extra_data=None):
        data = {
            'value': TEST_METADATA_VALUE_EDITED
        }
        data.update(extra_data or {})

        return self.patch(
            viewname='rest_api:documentmetadata-detail',
            kwargs={
                'document_id': self._test_document.pk,
                'metadata_id': self._test_document_metadata.pk
            }, data=data
        )

    def _request_document_metadata_edit_api_view_via_put(self, extra_data=None):
        data = {
            'value': TEST_METADATA_VALUE_EDITED
        }
        data.update(extra_data or {})

        return self.put(
            viewname='rest_api:documentmetadata-detail',
            kwargs={
                'document_id': self._test_document.pk,
                'metadata_id': self._test_document_metadata.pk
            }, data=data
        )

    def _request_document_metadata_list_api_view(self):
        return self.get(
            viewname='rest_api:documentmetadata-list', kwargs={
                'document_id': self._test_document.pk
            }
        )


class DocumentMetadataMixin:
    def _create_test_document_metadata(self):
        self._test_document_metadata = self._test_document.metadata.create(
            metadata_type=self._test_metadata_type, value=TEST_METADATA_VALUE
        )


class DocumentMetadataViewTestMixin:
    def _request_test_document_metadata_add_get_view(self):
        return self.get(
            viewname='metadata:metadata_add', kwargs={
                'document_id': self._test_document.pk
            }, data={'metadata_type': self._test_metadata_type.pk}
        )

    def _request_test_document_metadata_add_post_view(self):
        return self.post(
            viewname='metadata:metadata_add', kwargs={
                'document_id': self._test_document.pk
            }, data={'metadata_type': self._test_metadata_type.pk}
        )

    def _request_test_document_metadata_multiple_add_post_view(self):
        return self.post(
            viewname='metadata:metadata_add', kwargs={
                'document_id': self._test_document.pk
            }, data={
                'metadata_type': [
                    metadata_type.pk for metadata_type in self._test_metadata_types
                ],
            }
        )

    def _request_test_document_metadata_edit_post_view(
        self, extra_data=None, follow=False
    ):
        data = {
            'form-0-metadata_type_id': self._test_metadata_type.pk,
            'form-0-update': True,
            'form-0-value': TEST_METADATA_VALUE_EDITED,
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }

        if extra_data:
            data.update(extra_data)

        return self.post(
            viewname='metadata:metadata_edit', kwargs={
                'document_id': self._test_document.pk
            }, data=data, follow=follow
        )

    def _request_test_document_metadata_list_view(self):
        return self.get(
            viewname='metadata:metadata_list', kwargs={
                'document_id': self._test_document.pk
            }
        )

    def _request_test_document_metadata_remove_get_view(self):
        return self.get(
            viewname='metadata:metadata_remove', kwargs={
                'document_id': self._test_document.pk
            }
        )

    def _request_test_document_metadata_remove_post_view(self, index=0):
        return self.post(
            viewname='metadata:metadata_remove',
            kwargs={'document_id': self._test_document.pk}, data={
                'form-0-metadata_type_id': self._test_metadata_types[index].pk,
                'form-0-update': True,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }
        )

    def _request_test_document_multiple_metadata_add_post_view(self):
        return self.post(
            viewname='metadata:metadata_multiple_add', data={
                'id_list': '{},{}'.format(
                    self._test_documents[0].pk, self._test_documents[1].pk
                ),
                'metadata_type': self._test_metadata_type.pk
            }
        )

    def _request_test_document_multiple_metadata_edit_get_view(self):
        return self.get(
            viewname='metadata:metadata_multiple_edit', data={
                'id_list': '{},{}'.format(
                    self._test_documents[0].pk, self._test_documents[1].pk
                )
            }
        )

    def _request_test_document_multiple_metadata_edit_post_view(self):
        return self.post(
            viewname='metadata:metadata_multiple_edit', data={
                'id_list': '{},{}'.format(
                    self._test_documents[0].pk, self._test_documents[1].pk
                ),
                'form-0-metadata_type_id': self._test_metadata_type.pk,
                'form-0-update': True,
                'form-0-value': TEST_METADATA_VALUE_EDITED,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }
        )

    def _request_test_document_multiple_metadata_remove_get_view(self):
        return self.get(
            viewname='metadata:metadata_multiple_remove', data={
                'id_list': '{},{}'.format(
                    self._test_documents[0].pk, self._test_documents[0].pk
                )
            }
        )

    def _request_test_document_multiple_metadata_remove_post_view(self):
        return self.post(
            viewname='metadata:metadata_multiple_remove', data={
                'id_list': '{},{}'.format(
                    self._test_documents[0].pk, self._test_documents[1].pk
                ),
                'form-0-metadata_type_id': self._test_metadata_type.pk,
                'form-0-update': True,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }
        )


class DocumentTypeMetadataTypeAPIViewTestMixin:
    def _request_document_type_metadata_type_create_api_view(self):
        pk_list = list(DocumentTypeMetadataType.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='rest_api:documenttypemetadatatype-list',
            kwargs={'document_type_id': self._test_document_type.pk}, data={
                'metadata_type_id': self._test_metadata_type.pk,
                'required': False
            }
        )

        try:
            self._test_document_type_metadata_type = DocumentTypeMetadataType.objects.get(
                ~Q(pk__in=pk_list)
            )
        except DocumentTypeMetadataType.DoesNotExist:
            self._test_document_type_metadata_type = None

        return response

    def _request_document_type_metadata_type_delete_api_view(self):
        return self.delete(
            viewname='rest_api:documenttypemetadatatype-detail',
            kwargs={
                'document_type_id': self._test_document_type.pk,
                'metadata_type_id': self._test_document_type_metadata_type.pk
            }
        )

    def _request_document_type_metadata_type_list_api_view(self):
        return self.get(
            viewname='rest_api:documenttypemetadatatype-list', kwargs={
                'document_type_id': self._test_document_type.pk
            }
        )

    def _request_document_type_metadata_type_edit_api_view_via_patch(self):
        return self.patch(
            viewname='rest_api:documenttypemetadatatype-detail',
            kwargs={
                'document_type_id': self._test_document_type.pk,
                'metadata_type_id': self._test_document_type_metadata_type.pk
            }, data={
                'required': True
            }
        )

    def _request_document_type_metadata_type_edit_api_view_via_put(self):
        return self.put(
            viewname='rest_api:documenttypemetadatatype-detail',
            kwargs={
                'document_type_id': self._test_document_type.pk,
                'metadata_type_id': self._test_document_type_metadata_type.pk
            }, data={
                'required': True
            }
        )


class DocumentTypeMetadataTypeTestMixin:
    def _create_test_document_type_metadata_type(self):
        self._test_document_type_metadata_type = self._test_document_type.metadata.create(
            metadata_type=self._test_metadata_type, required=False
        )


class MetadataDocumentUploadWizardStepTestMixin:
    def _request_upload_interactive_document_create_view(
        self, metadata_value
    ):
        url = URL(
            path=reverse(viewname='sources:document_upload_interactive')
        )
        url.args['metadata0_metadata_type_id'] = self._test_metadata_type.pk
        url.args['metadata0_value'] = metadata_value

        with open(file=TEST_FILE_SMALL_PATH, mode='rb') as file_object:
            return self.post(
                path=url.to_string(), data={
                    'document-language': 'eng', 'source-file': file_object,
                    'document_type_id': self._test_document_type.pk,
                }
            )

    def _request_document_create_view(self):
        return self.post(
            viewname='sources:document_create_multiple', data={
                'document_type_selection-document_type': self._test_document_type.pk,
                'document_create_wizard-current_step': 0
            }
        )


class MetadataTypeAPIViewTestMixin:
    def _request_test_metadata_type_create_api_view(self):
        pk_list = list(MetadataType.objects.values('pk'))

        response = self.post(
            viewname='rest_api:metadatatype-list', data={
                'name': 'test_metadata_type', 'label': 'test metadata type'
            }
        )

        try:
            self._test_metadata_type = MetadataType.objects.get(
                ~Q(pk__in=pk_list)
            )
        except MetadataType.DoesNotExist:
            self._test_metadata_type = None

        return response

    def _request_test_metadata_type_delete_api_view(self):
        return self.delete(
            viewname='rest_api:metadatatype-detail',
            kwargs={'metadata_type_id': self._test_metadata_type.pk}
        )

    def _request_test_metadata_type_detail_api_view(self):
        return self.get(
            viewname='rest_api:metadatatype-detail',
            kwargs={'metadata_type_id': self._test_metadata_type.pk}
        )

    def _request_test_metadata_type_edit_api_view_via_patch(self):
        return self.patch(
            viewname='rest_api:metadatatype-detail',
            kwargs={'metadata_type_id': self._test_metadata_type.pk}, data={
                'label': '{} edited'.format(self._test_metadata_type.label),
                'name': '{}_edited'.format(self._test_metadata_type.name),
            }
        )

    def _request_test_metadata_type_edit_api_view_via_put(self):
        return self.put(
            viewname='rest_api:metadatatype-detail',
            kwargs={'metadata_type_id': self._test_metadata_type.pk}, data={
                'label': '{} edited'.format(self._test_metadata_type.label),
                'name': '{}_edited'.format(self._test_metadata_type.name),
            }
        )

    def _request_test_metadata_type_list_api_view(self):
        return self.get(viewname='rest_api:metadatatype-list')


class MetadataTypeTestMixin:
    auto_add_test_metadata_type_to_test_document_type = True
    auto_create_test_metadata_type = False

    def setUp(self):
        super().setUp()
        self._test_metadata_types = []
        self._test_document_type_metadata_type_relationships = []

        if self.auto_create_test_metadata_type:
            self._create_test_metadata_type(
                add_test_document_type=self.auto_add_test_metadata_type_to_test_document_type
            )

    def _get_test_metadata_type_queryset(self):
        return MetadataType.objects.filter(
            pk__in=[
                metadata_type.pk for metadata_type in self._test_metadata_types
            ]
        )

    def _create_test_metadata_type(
        self, add_test_document_type=False, extra_kwargs=None, required=False
    ):
        total_test_metadata_types = len(self._test_metadata_types)
        name = '{}_{}'.format(
            TEST_METADATA_TYPE_NAME, total_test_metadata_types
        )
        label = '{}_{}'.format(
            TEST_METADATA_TYPE_LABEL, total_test_metadata_types
        )

        kwargs = {'name': name, 'label': label}

        if extra_kwargs:
            kwargs.update(extra_kwargs)

        self._test_metadata_type = MetadataType.objects.create(**kwargs)
        self._test_metadata_types.append(self._test_metadata_type)

        if add_test_document_type:
            self._test_document_type_metadata_type_relationships.append(
                self._test_document_type.metadata.create(
                    metadata_type=self._test_metadata_type, required=required
                )
            )


class MetadataTypeViewTestMixin:
    def _request_test_document_type_relationship_delete_view(self):
        # This request assumes there is only one document type and
        # blindly sets the first form of the formset.

        return self.post(
            viewname='metadata:document_type_metadata_type_relationship',
            kwargs={'document_type_id': self._test_document_type.pk}, data={
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-0-relationship_type': 'none'
            }
        )

    def _request_test_document_type_relationship_edit_view(self):
        # This request assumes there is only one document type and
        # blindly sets the first form of the formset.

        return self.post(
            viewname='metadata:document_type_metadata_type_relationship',
            kwargs={'document_type_id': self._test_document_type.pk}, data={
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-0-relationship_type': 'required'
            }
        )

    def _request_test_metadata_type_create_view(self):
        pk_list = list(MetadataType.objects.values('pk'))

        response = self.post(
            viewname='metadata:metadata_type_create', data={
                'name': 'test_metadata_type', 'label': 'test metadata type'
            }
        )

        try:
            self._test_metadata_type = MetadataType.objects.get(
                ~Q(pk__in=pk_list)
            )
        except MetadataType.DoesNotExist:
            self._test_metadata_type = None

        return response

    def _request_test_metadata_type_single_delete_view(self):
        return self.post(
            viewname='metadata:metadata_type_single_delete', kwargs={
                'metadata_type_id': self._test_metadata_type.pk
            }
        )

    def _request_test_metadata_type_multiple_delete_view(self):
        return self.post(
            viewname='metadata:metadata_type_multiple_delete', data={
                'id_list': self._test_metadata_type.pk
            }
        )

    def _request_test_metadata_type_edit_view(self):
        return self.post(
            viewname='metadata:metadata_type_edit', kwargs={
                'metadata_type_id': self._test_metadata_type.pk
            }, data={
                'label': TEST_METADATA_TYPE_LABEL_EDITED,
                'name': TEST_METADATA_TYPE_NAME_EDITED
            }
        )

    def _request_metadata_type_list_view(self):
        return self.get(
            viewname='metadata:metadata_type_list',
        )

    def _request_test_metadata_type_document_type_relationship_delete_view(self):
        # This request assumes there is only one document type and
        # blindly sets the first form of the formset.

        return self.post(
            viewname='metadata:metadata_type_document_type_relationship',
            kwargs={'metadata_type_id': self._test_metadata_type.pk}, data={
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-0-relationship_type': 'none'
            }
        )

    def _request_test_metadata_type_document_type_relationship_edit_view(self):
        # This request assumes there is only one document type and
        # blindly sets the first form of the formset.

        return self.post(
            viewname='metadata:metadata_type_document_type_relationship',
            kwargs={'metadata_type_id': self._test_metadata_type.pk}, data={
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-0-relationship_type': 'required'
            }
        )
