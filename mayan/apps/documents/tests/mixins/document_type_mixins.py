from ..literals import (
    TEST_DOCUMENT_TYPE_DELETE_PERIOD, TEST_DOCUMENT_TYPE_DELETE_TIME_UNIT,
    TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_LABEL_EDITED,
    TEST_DOCUMENT_TYPE_QUICK_LABEL, TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED
)


class DocumentQuickLabelViewTestMixin:
    def _request_test_document_quick_label_edit_view(self, extra_data=None):
        data = {
            'document_type_available_filenames': self.test_document_type_filename.pk,
            'label': ''
            # View needs at least an empty label for quick
            # label to work. Cause is unknown.
        }
        data.update(extra_data or {})

        return self.post(
            viewname='documents:document_properties_edit', kwargs={
                'document_id': self.test_document.pk
            }, data=data
        )


class DocumentTypeAPIViewTestMixin:
    def _request_test_document_type_create_api_view(self):
        return self.post(
            viewname='rest_api:documenttype-list', data={
                'label': TEST_DOCUMENT_TYPE_LABEL
            }
        )

    def _request_test_document_type_delete_api_view(self):
        return self.delete(
            viewname='rest_api:documenttype-detail', kwargs={
                'document_type_id': self.test_document_type.pk,
            }
        )

    def _request_test_document_type_patch_api_view(self):
        return self.patch(
            viewname='rest_api:documenttype-detail', kwargs={
                'document_type_id': self.test_document_type.pk,
            }, data={'label': TEST_DOCUMENT_TYPE_LABEL_EDITED}
        )

    def _request_test_document_type_put_api_view(self):
        return self.put(
            viewname='rest_api:documenttype-detail', kwargs={
                'document_type_id': self.test_document_type.pk,
            }, data={'label': TEST_DOCUMENT_TYPE_LABEL_EDITED}
        )


class DocumentTypeDeletionPoliciesViewTestMixin:
    def _request_test_document_type_policies_get_view(self):
        return self.get(
            viewname='documents:document_type_policies', kwargs={
                'document_type_id': self.test_document_type.pk
            }
        )


class DocumentTypeFilenameGeneratorViewTestMixin:
    def _request_test_document_type_filename_generator_get_view(self):
        return self.get(
            viewname='documents:document_type_filename_generator', kwargs={
                'document_type_id': self.test_document_type.pk
            }
        )


class DocumentTypeQuickLabelViewTestMixin:
    def _request_test_quick_label_create_view(self):
        return self.post(
            viewname='documents:document_type_filename_create', kwargs={
                'document_type_id': self.test_document_type.pk
            }, data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL,
            }
        )

    def _request_test_quick_label_delete_view(self):
        return self.post(
            viewname='documents:document_type_filename_delete', kwargs={
                'document_type_filename_id': self.test_document_type_filename.pk
            }
        )

    def _request_test_quick_label_edit_view(self):
        return self.post(
            viewname='documents:document_type_filename_edit', kwargs={
                'document_type_filename_id': self.test_document_type_filename.pk
            }, data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED,
            }
        )

    def _request_test_quick_label_list_view(self):
        return self.get(
            viewname='documents:document_type_filename_list', kwargs={
                'document_type_id': self.test_document_type.pk
            }
        )


class DocumentTypeQuickLabelTestMixin:
    def _create_test_quick_label(self):
        self.test_document_type_filename = self.test_document_type.filenames.create(
            filename=TEST_DOCUMENT_TYPE_QUICK_LABEL
        )


class DocumentTypeViewTestMixin:
    def _request_test_document_type_create_view(self):
        return self.post(
            viewname='documents:document_type_create',
            data={
                'label': TEST_DOCUMENT_TYPE_LABEL,
                'delete_time_period': TEST_DOCUMENT_TYPE_DELETE_PERIOD,
                'delete_time_unit': TEST_DOCUMENT_TYPE_DELETE_TIME_UNIT
            }
        )

    def _request_test_document_type_delete_view(self):
        return self.post(
            viewname='documents:document_type_delete', kwargs={
                'document_type_id': self.test_document_type.pk
            }
        )

    def _request_test_document_type_edit_view(self):
        return self.post(
            viewname='documents:document_type_edit', kwargs={
                'document_type_id': self.test_document_type.pk
            }, data={
                'label': TEST_DOCUMENT_TYPE_LABEL_EDITED,
            }
        )

    def _request_test_document_type_list_view(self):
        return self.get(viewname='documents:document_type_list')
