from django.db.models import Q

from mayan.apps.converter.layers import layer_saved_transformations

from ...literals import PAGE_RANGE_ALL
from ...models.document_file_models import DocumentFile

from ..literals import (
    TEST_DOCUMENT_FILE_ACTION, TEST_DOCUMENT_FILE_COMMENT,
    TEST_DOCUMENT_FILE_COMMENT_EDITED, TEST_DOCUMENT_FILE_FILENAME_EDITED,
    TEST_SMALL_DOCUMENT_PATH, TEST_TRANSFORMATION_ARGUMENT,
    TEST_TRANSFORMATION_CLASS
)


class DocumentFileAPIViewTestMixin:
    def _request_test_document_file_delete_api_view(self):
        return self.delete(
            viewname='rest_api:documentfile-detail', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document.file_latest.pk
            }
        )

    def _request_test_document_file_detail_api_view(self):
        return self.get(
            viewname='rest_api:documentfile-detail', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document.file_latest.pk
            }
        )

    def _request_test_document_file_download_api_view(self):
        return self.get(
            viewname='rest_api:documentfile-download', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document.file_latest.pk,
            }
        )

    def _request_test_document_file_list_api_view(self):
        return self.get(
            viewname='rest_api:documentfile-list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_file_upload_api_view(self):
        pk_list = list(DocumentFile.objects.values_list('pk', flat=True))

        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_descriptor:
            response = self.post(
                viewname='rest_api:documentfile-list', kwargs={
                    'document_id': self.test_document.pk,
                }, data={
                    'action': TEST_DOCUMENT_FILE_ACTION, 'comment': '',
                    'file_new': file_descriptor,
                }
            )

        try:
            self.test_document_file = DocumentFile.objects.get(
                ~Q(pk__in=pk_list)
            )
        except DocumentFile.DoesNotExist:
            self.test_document_file = None

        return response


class DocumentFileLinkTestMixin:
    def _resolve_test_document_file_link(self, test_link):
        self.add_test_view(test_object=self.test_document_file)
        context = self.get_test_view()
        return test_link.resolve(context=context)


class DocumentFileTestMixin:
    def _upload_new_file(self):
        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.file_new(
                comment=TEST_DOCUMENT_FILE_COMMENT, file_object=file_object
            )


class DocumentFileViewTestMixin:
    def _request_test_document_file_delete_view(self, document_file):
        return self.post(
            viewname='documents:document_file_delete', kwargs={
                'document_file_id': document_file.pk
            }
        )

    def _request_test_document_file_delete_multiple_view(self):
        return self.post(
            viewname='documents:document_file_delete_multiple', data={
                'id_list': self.test_document_file.pk
            }
        )

    def _request_test_document_file_download_view(self, data=None):
        data = data or {}
        return self.get(
            viewname='documents:document_file_download', kwargs={
                'document_file_id': self.test_document.file_latest.pk
            }, data=data
        )

    def _request_test_document_file_edit_view(self):
        return self.post(
            viewname='documents:document_file_edit', kwargs={
                'document_file_id': self.test_document_file.pk
            }, data={
                'comment': TEST_DOCUMENT_FILE_COMMENT_EDITED,
                'filename': TEST_DOCUMENT_FILE_FILENAME_EDITED
            }
        )

    def _request_test_document_file_list_view(self):
        return self.get(
            viewname='documents:document_file_list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_file_preview_view(self):
        return self.get(
            viewname='documents:document_file_preview', kwargs={
                'document_file_id': self.test_document_file.pk
            }
        )

    def _request_test_document_file_print_form_view(self):
        return self.get(
            viewname='documents:document_file_print_form', kwargs={
                'document_file_id': self.test_document_file.pk,
            }, data={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_file_print_view(self):
        return self.get(
            viewname='documents:document_file_print_view', kwargs={
                'document_file_id': self.test_document_file.pk,
            }, query={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_file_properties_view(self):
        return self.get(
            viewname='documents:document_file_properties', kwargs={
                'document_file_id': self.test_document_file.pk
            }
        )


class DocumentFilePageAPIViewTestMixin:
    def _request_test_document_file_page_detail_api_view(self):
        return self.get(
            viewname='rest_api:documentfilepage-detail', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk,
                'document_file_page_id': self.test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_image_api_view(self):
        return self.get(
            viewname='rest_api:documentfilepage-image', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk,
                'document_file_page_id': self.test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_list_api_view(self):
        return self.get(
            viewname='rest_api:documentfilepage-list', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk,
            }
        )


class DocumentFilePageViewTestMixin:
    def _request_test_document_file_page_count_update_view(self):
        return self.post(
            viewname='documents:document_file_page_count_update',
            kwargs={'document_file_id': self.test_document_file.pk}
        )

    def _request_test_document_file_multiple_page_count_update_view(self):
        return self.post(
            viewname='documents:document_file_multiple_page_count_update',
            data={'id_list': self.test_document_file.pk}
        )

    def _request_test_document_file_page_list_view(self):
        return self.get(
            viewname='documents:document_file_page_list', kwargs={
                'document_file_id': self.test_document_file.pk
            }
        )

    def _request_test_document_file_page_rotate_left_view(self):
        return self.post(
            viewname='documents:document_file_page_rotate_left', kwargs={
                'document_file_page_id': self.test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_rotate_right_view(self):
        return self.post(
            viewname='documents:document_file_page_rotate_right', kwargs={
                'document_file_page_id': self.test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_view(self, document_file_page):
        return self.get(
            viewname='documents:document_file_page_view', kwargs={
                'document_file_page_id': document_file_page.pk,
            }
        )

    def _request_test_document_file_page_zoom_in_view(self):
        return self.post(
            viewname='documents:document_file_page_zoom_in', kwargs={
                'document_file_page_id': self.test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_zoom_out_view(self):
        return self.post(
            viewname='documents:document_file_page_zoom_out', kwargs={
                'document_file_page_id': self.test_document_file_page.pk
            }
        )


class DocumentFileTransformationTestMixin:
    def _create_document_file_transformation(self):
        layer_saved_transformations.add_transformation_to(
            obj=self.test_document_file.pages.first(),
            transformation_class=TEST_TRANSFORMATION_CLASS,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )


class DocumentFileTransformationViewTestMixin:
    def _request_test_document_file_transformations_clear_view(self):
        return self.post(
            viewname='documents:document_file_transformations_clear',
            kwargs={'document_file_id': self.test_document_file.pk}
        )

    def _request_test_document_file_multiple_transformations_clear_view(self):
        return self.post(
            viewname='documents:document_file_multiple_transformations_clear',
            data={'id_list': self.test_document_file.pk}
        )

    def _request_test_document_file_transformations_clone_view(self):
        return self.post(
            viewname='documents:document_file_transformations_clone',
            kwargs={'document_file_id': self.test_document_file.pk}, data={
                'page': self.test_document_file.pages.first().pk
            }
        )
