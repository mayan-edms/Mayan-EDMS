from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH

from ..models import Cabinet

from .literals import (
    TEST_CABINET_CHILD_LABEL, TEST_CABINET_LABEL, TEST_CABINET_LABEL_EDITED
)


class CabinetAPIViewTestMixin:
    def _request_test_cabinet_create_api_view(self, extra_data=None):
        data = {'label': TEST_CABINET_LABEL, 'parent': ''}

        if extra_data:
            data.update(extra_data)

        # Typecast to list to force queryset evaluation
        values = list(Cabinet.objects.values_list('pk', flat=True))

        response = self.post(viewname='rest_api:cabinet-list', data=data)

        self.test_cabinet = Cabinet.objects.exclude(pk__in=values).first()

        return response

    def _request_test_cabinet_delete_api_view(self):
        return self.delete(
            viewname='rest_api:cabinet-detail', kwargs={
                'cabinet_id': self.test_cabinet.pk
            }
        )

    def _request_test_cabinet_edit_api_patch_view(self):
        return self.patch(
            data={'label': TEST_CABINET_LABEL_EDITED}, kwargs={
                'cabinet_id': self.test_cabinet.pk
            }, viewname='rest_api:cabinet-detail'
        )

    def _request_test_cabinet_edit_api_put_view(self):
        return self.put(
            data={'label': TEST_CABINET_LABEL_EDITED}, kwargs={
                'cabinet_id': self.test_cabinet.pk
            }, viewname='rest_api:cabinet-detail'
        )

    def _request_test_cabinet_list_api_view(self):
        return self.get(viewname='rest_api:cabinet-list')


class CabinetDocumentAPIViewTestMixin:
    def _request_test_cabinet_document_add_api_view(self):
        return self.post(
            viewname='rest_api:cabinet-document-add', kwargs={
                'cabinet_id': self.test_cabinet.pk
            }, data={
                'document': self.test_document.pk
            }
        )

    def _request_test_cabinet_document_list_api_view(self):
        return self.get(
            viewname='rest_api:cabinet-document-list', kwargs={
                'cabinet_id': self.test_cabinet.pk
            }
        )

    def _request_test_cabinet_document_remove_api_view(self):
        return self.post(
            viewname='rest_api:cabinet-document-remove', kwargs={
                'cabinet_id': self.test_cabinet.pk
            }, data={
                'document': self.test_document.pk
            }
        )


class CabinetDocumentUploadWizardStepTestMixin:
    def _request_upload_interactive_document_create_view(self):
        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_upload_interactive', kwargs={
                    'source_id': self.test_source.pk
                }, data={
                    'document_type_id': self.test_document_type.pk,
                    'source-file': file_object,
                    'cabinets': Cabinet.objects.values_list('pk', flat=True)
                }
            )

    def _request_wizard_view(self):
        return self.get(viewname='sources:document_create_multiple')


class CabinetTestMixin:
    def setUp(self):
        super().setUp()
        if not hasattr(self, 'test_cabinets'):
            self.test_cabinets = []

    def _create_test_cabinet(self):
        self.test_cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)
        self.test_cabinets.append(self.test_cabinet)

    def _create_test_cabinet_child(self):
        self.test_cabinet_child = Cabinet.objects.create(
            label=TEST_CABINET_CHILD_LABEL, parent=self.test_cabinet
        )


class CabinetViewTestMixin:
    def setUp(self):
        super().setUp()
        if not hasattr(self, 'test_cabinets'):
            self.test_cabinets = []

    def _request_test_cabinet_create_view(self):
        # Typecast to list to force queryset evaluation
        values = list(Cabinet.objects.values_list('pk', flat=True))

        response = self.post(
            'cabinets:cabinet_create', data={
                'label': TEST_CABINET_LABEL
            }
        )

        self.test_cabinet = Cabinet.objects.exclude(pk__in=values).first()
        self.test_cabinets.append(self.test_cabinet)

        return response

    def _request_test_cabinet_delete_view(self):
        return self.post(
            viewname='cabinets:cabinet_delete', kwargs={
                'cabinet_id': self.test_cabinet.pk
            }
        )

    def _request_test_cabinet_edit_view(self):
        return self.post(
            viewname='cabinets:cabinet_edit', kwargs={
                'cabinet_id': self.test_cabinet.pk
            }, data={
                'label': TEST_CABINET_LABEL_EDITED
            }
        )

    def _request_test_cabinet_child_create_view(self):
        # Typecast to list to force queryset evaluation
        values = list(Cabinet.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='cabinets:cabinet_child_add', kwargs={
                'cabinet_id': self.test_cabinet.pk
            }, data={'label': TEST_CABINET_CHILD_LABEL}
        )

        self.test_cabinet = Cabinet.objects.exclude(pk__in=values).first()
        self.test_cabinets.append(self.test_cabinet)

        return response

    def _request_test_cabinet_child_delete_view(self):
        return self.post(
            viewname='cabinets:cabinet_delete', kwargs={
                'cabinet_id': self.test_cabinet_child.pk
            }
        )

    def _request_test_cabinet_document_list_view(self):
        return self.get(
            viewname='cabinets:cabinet_view', kwargs={
                'cabinet_id': self.test_cabinet.pk
            }
        )

    def _request_test_cabinet_list_view(self):
        return self.get(viewname='cabinets:cabinet_list')

    def _request_test_document_cabinet_add_view(self):
        return self.post(
            viewname='cabinets:document_cabinet_add', kwargs={
                'document_id': self.test_document.pk
            }, data={
                'cabinets': self.test_cabinet.pk
            }
        )

    def _request_test_document_cabinet_multiple_remove_view(self):
        return self.post(
            viewname='cabinets:document_cabinet_remove', kwargs={
                'document_id': self.test_document.pk
            }, data={
                'cabinets': (self.test_cabinet.pk,),
            }
        )

    def _request_test_document_multiple_cabinet_multiple_add_view_cabinet(self):
        return self.post(
            viewname='cabinets:document_multiple_cabinet_add', data={
                'id_list': (self.test_document.pk,),
                'cabinets': self.test_cabinet.pk
            }
        )


class DocumentCabinetAPIViewTestMixin:
    def _request_test_document_cabinet_list_api_view(self):
        return self.get(
            viewname='rest_api:document-cabinet-list', kwargs={
                'document_id': self.test_document.pk
            }
        )


class DocumentCabinetViewTestMixin:
    def _request_test_document_cabinet_list_view(self):
        return self.get(
            viewname='cabinets:document_cabinet_list', kwargs={
                'document_id': self.test_document.pk
            }
        )
