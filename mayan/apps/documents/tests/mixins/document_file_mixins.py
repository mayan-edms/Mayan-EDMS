from django.db.models import Q

from mayan.apps.converter.layers import layer_saved_transformations

from ...document_file_actions import DocumentFileActionUseNewPages
from ...literals import PAGE_RANGE_ALL
from ...models.document_file_models import DocumentFile

from ..literals import (
    TEST_DOCUMENT_FILE_COMMENT, TEST_DOCUMENT_FILE_COMMENT_EDITED,
    TEST_DOCUMENT_FILE_FILENAME_EDITED, TEST_FILE_SMALL_PATH,
    TEST_TRANSFORMATION_ARGUMENT, TEST_TRANSFORMATION_CLASS
)


class DocumentFileAPIViewTestMixin:
    def _request_test_document_file_delete_api_view(self):
        return self.delete(
            viewname='rest_api:documentfile-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_file_id': self._test_document.file_latest.pk
            }
        )

    def _request_test_document_file_detail_api_view(self):
        return self.get(
            viewname='rest_api:documentfile-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_file_id': self._test_document.file_latest.pk
            }
        )

    def _request_test_document_file_download_api_view(self):
        return self.get(
            viewname='rest_api:documentfile-download', kwargs={
                'document_id': self._test_document.pk,
                'document_file_id': self._test_document.file_latest.pk,
            }
        )

    def _request_test_document_file_list_api_view(self):
        return self.get(
            viewname='rest_api:documentfile-list', kwargs={
                'document_id': self._test_document.pk
            }
        )

    def _request_test_document_file_upload_api_view(self):
        pk_list = list(DocumentFile.objects.values_list('pk', flat=True))

        with open(file=TEST_FILE_SMALL_PATH, mode='rb') as file_descriptor:
            response = self.post(
                viewname='rest_api:documentfile-list', kwargs={
                    'document_id': self._test_document.pk,
                }, data={
                    'action': DocumentFileActionUseNewPages.backend_id,
                    'comment': '', 'file_new': file_descriptor,
                }
            )

        try:
            self._test_document_file = DocumentFile.objects.get(
                ~Q(pk__in=pk_list)
            )
        except DocumentFile.DoesNotExist:
            self._test_document_file = None

        return response


class DocumentFileLinkTestMixin:
    def _resolve_test_document_file_link(self, test_link):
        self.add_test_view(test_object=self._test_document_file)
        context = self.get_test_view()
        return test_link.resolve(context=context)


class DocumentFileTestMixin:
    def _upload_test_document_file(self, action=None, _user=None):
        self._calculate_test_document_file_path()

        if not action:
            action = DocumentFileActionUseNewPages.backend_id

        with open(file=self._test_document_path, mode='rb') as file_object:
            self._test_document_file = self._test_document.file_new(
                action=action, comment=TEST_DOCUMENT_FILE_COMMENT,
                file_object=file_object, _user=_user
            )

        self._test_document_file_page = self._test_document_file.pages.first()
        self._test_document_file_pages.extend(
            list(self._test_document_file.pages.all())
        )
        self._test_document_files.append(self._test_document_file)
        self._test_document_version = self._test_document.version_active


class DocumentFileViewTestMixin:
    def _request_test_document_file_delete_view(self, document_file):
        return self.post(
            viewname='documents:document_file_delete', kwargs={
                'document_file_id': document_file.pk
            }
        )

    def _request_test_document_file_multiple_delete_view(self):
        return self.post(
            viewname='documents:document_file_multiple_delete', data={
                'id_list': self._test_document_file.pk
            }
        )

    def _request_test_document_file_download_view(self, data=None):
        data = data or {}
        return self.get(
            viewname='documents:document_file_download', kwargs={
                'document_file_id': self._test_document.file_latest.pk
            }, data=data
        )

    def _request_test_document_file_edit_view(self):
        return self.post(
            viewname='documents:document_file_edit', kwargs={
                'document_file_id': self._test_document_file.pk
            }, data={
                'comment': TEST_DOCUMENT_FILE_COMMENT_EDITED,
                'filename': TEST_DOCUMENT_FILE_FILENAME_EDITED
            }
        )

    def _request_test_document_file_list_view(self):
        return self.get(
            viewname='documents:document_file_list', kwargs={
                'document_id': self._test_document.pk
            }
        )

    def _request_test_document_file_preview_view(self):
        return self.get(
            viewname='documents:document_file_preview', kwargs={
                'document_file_id': self._test_document_file.pk
            }
        )

    def _request_test_document_file_print_form_view(self):
        return self.get(
            viewname='documents:document_file_print_form', kwargs={
                'document_file_id': self._test_document_file.pk,
            }, data={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_file_print_view(self):
        return self.get(
            viewname='documents:document_file_print_view', kwargs={
                'document_file_id': self._test_document_file.pk,
            }, query={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_file_properties_view(self):
        return self.get(
            viewname='documents:document_file_properties', kwargs={
                'document_file_id': self._test_document_file.pk
            }
        )


class DocumentFilePageAPIViewTestMixin:
    def _request_test_document_file_page_detail_api_view(self):
        return self.get(
            viewname='rest_api:documentfilepage-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_file_id': self._test_document_file.pk,
                'document_file_page_id': self._test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_image_api_view(
        self, maximum_layer_order=None
    ):
        return self.get(
            viewname='rest_api:documentfilepage-image', kwargs={
                'document_id': self._test_document.pk,
                'document_file_id': self._test_document_file.pk,
                'document_file_page_id': self._test_document_file_page.pk
            }, query={'maximum_layer_order': maximum_layer_order}
        )

    def _request_test_document_file_page_list_api_view(self):
        return self.get(
            viewname='rest_api:documentfilepage-list', kwargs={
                'document_id': self._test_document.pk,
                'document_file_id': self._test_document_file.pk,
            }
        )


class DocumentFilePageViewTestMixin:
    def _request_test_document_file_page_count_update_view(self):
        return self.post(
            viewname='documents:document_file_page_count_update',
            kwargs={'document_file_id': self._test_document_file.pk}
        )

    def _request_test_document_file_multiple_page_count_update_view(self):
        return self.post(
            viewname='documents:document_file_multiple_page_count_update',
            data={'id_list': self._test_document_file.pk}
        )

    def _request_test_document_file_page_list_view(self):
        return self.get(
            viewname='documents:document_file_page_list', kwargs={
                'document_file_id': self._test_document_file.pk
            }
        )

    def _request_test_document_file_page_rotate_left_view(self):
        return self.post(
            viewname='documents:document_file_page_rotate_left', kwargs={
                'document_file_page_id': self._test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_rotate_right_view(self):
        return self.post(
            viewname='documents:document_file_page_rotate_right', kwargs={
                'document_file_page_id': self._test_document_file_page.pk
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
                'document_file_page_id': self._test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_zoom_out_view(self):
        return self.post(
            viewname='documents:document_file_page_zoom_out', kwargs={
                'document_file_page_id': self._test_document_file_page.pk
            }
        )


class DocumentFileTransformationTestMixin:
    def _create_document_file_transformation(self):
        layer_saved_transformations.add_transformation_to(
            obj=self._test_document_file.pages.first(),
            transformation_class=TEST_TRANSFORMATION_CLASS,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )


class DocumentFileTransformationViewTestMixin:
    def _request_test_document_file_transformations_clear_view(self):
        return self.post(
            viewname='documents:document_file_transformations_clear',
            kwargs={'document_file_id': self._test_document_file.pk}
        )

    def _request_test_document_file_multiple_transformations_clear_view(self):
        return self.post(
            viewname='documents:document_file_multiple_transformations_clear',
            data={'id_list': self._test_document_file.pk}
        )

    def _request_test_document_file_transformations_clone_view(self):
        return self.post(
            viewname='documents:document_file_transformations_clone',
            kwargs={'document_file_id': self._test_document_file.pk}, data={
                'page': self._test_document_file.pages.first().pk
            }
        )
