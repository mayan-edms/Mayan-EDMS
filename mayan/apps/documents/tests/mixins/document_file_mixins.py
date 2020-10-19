import time

from ...literals import PAGE_RANGE_ALL

from ..literals import (
    TEST_DOCUMENT_PATH, TEST_DOCUMENT_FILE_COMMENT_EDITED,
    TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_FILE_COMMENT
)


class DocumentFileAPIViewTestMixin:
    def _request_test_document_file_delete_api_view(self):
        return self.delete(
            viewname='rest_api:documentfile-detail', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document.latest_file.pk
            }
        )

    def _request_test_document_file_download_api_view(self):
        return self.get(
            viewname='rest_api:documentfile-download', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document.latest_file.pk,
            }
        )

    def _request_test_document_file_list_api_view(self):
        return self.get(
            viewname='rest_api:documentfile-list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_file_upload_api_view(self):
        # Artificial delay since MySQL doesn't store microsecond data in
        # timestamps. File timestamp is used to determine which file
        # is the latest.
        time.sleep(1)

        with open(file=TEST_DOCUMENT_PATH, mode='rb') as file_descriptor:
            return self.post(
                viewname='rest_api:documentfile-list', kwargs={
                    'document_id': self.test_document.pk,
                }, data={
                    'comment': '', 'file': file_descriptor,
                }
            )


class DocumentFileTestMixin:
    def _upload_new_file(self):
        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_file(
                comment=TEST_DOCUMENT_FILE_COMMENT, file_object=file_object
            )


class DocumentFileViewTestMixin:
    def _request_test_document_file_delete_view(self, document_file):
        return self.post(
            viewname='documents:document_file_delete', kwargs={
                'document_file_id': document_file.pk
            }
        )

    def _request_test_document_file_download_view(self, data=None):
        data = data or {}
        return self.get(
            viewname='documents:document_file_download', kwargs={
                'document_file_id': self.test_document.latest_file.pk
            }, data=data
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

class DocumentFilePageAPIViewTestMixin:
    def _request_test_document_file_page_image_api_view(self):
        page = self.test_document_file.pages.first()
        return self.get(
            viewname='rest_api:documentfilepage-image', kwargs={
                'document_id': page.document_file.document_id,
                'document_file_id': page.document_file_id,
                'document_file_page_id': page.pk
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
