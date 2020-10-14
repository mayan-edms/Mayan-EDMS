import time

from ..literals import (
    TEST_DOCUMENT_PATH, TEST_DOCUMENT_FILE_COMMENT_EDITED,
    TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_FILE_COMMENT
)


class DocumentFileAPIViewTestMixin:
    def _request_test_document_file_api_download_view(self):
        return self.get(
            viewname='rest_api:documentfile-download', kwargs={
                'pk': self.test_document.pk,
                'file_pk': self.test_document.latest_file.pk,
            }
        )

    def _request_test_document_file_api_edit_via_patch_view(self):
        return self.patch(
            viewname='rest_api:documentfile-detail', kwargs={
                'pk': self.test_document.pk,
                'file_pk': self.test_document.latest_file.pk
            }, data={'comment': TEST_DOCUMENT_FILE_COMMENT_EDITED}
        )

    def _request_test_document_file_api_edit_via_put_view(self):
        return self.put(
            viewname='rest_api:documentfile-detail', kwargs={
                'pk': self.test_document.pk,
                'file_pk': self.test_document.latest_file.pk
            }, data={'comment': TEST_DOCUMENT_FILE_COMMENT_EDITED}
        )

    def _request_test_document_file_api_list_view(self):
        return self.get(
            viewname='rest_api:documentfile-list', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_document_file_api_delete_view(self):
        return self.delete(
            viewname='rest_api:documentfile-detail', kwargs={
                'pk': self.test_document.pk,
                'file_pk': self.test_document.latest_file.pk
            }
        )

    def _request_test_document_file_api_upload_view(self):
        # Artificial delay since MySQL doesn't store microsecond data in
        # timestamps. File timestamp is used to determine which file
        # is the latest.
        time.sleep(1)

        with open(file=TEST_DOCUMENT_PATH, mode='rb') as file_descriptor:
            return self.post(
                viewname='rest_api:documentfile-list', kwargs={
                    'pk': self.test_document.pk,
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


class DocumentFilePageAPIViewTestMixin:
    def _request_document_file_page_image(self):
        page = self.test_document.pages.first()
        return self.get(
            viewname='rest_api:documentpage-image', kwargs={
                'pk': page.document_file.document_id, 'file_pk': page.document_file_id,
                'page_pk': page.pk
            }
        )


class DocumentFilePageDisableViewTestMixin:
    def _disable_test_document_file_page(self):
        self.test_document_file_page.enabled = False
        self.test_document_file_page.save()

    def _request_test_document_file_page_disable_view(self):
        return self.post(
            viewname='documents:document_file_page_disable', kwargs={
                'document_file_page_id': self.test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_enable_view(self):
        return self.post(
            viewname='documents:document_file_page_enable', kwargs={
                'document_file_page_id': self.test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_multiple_disable_view(self):
        return self.post(
            viewname='documents:document_file_page_multiple_disable', data={
                'id_list': self.test_document_file_page.pk
            }
        )

    def _request_test_document_file_page_multiple_enable_view(self):
        return self.post(
            viewname='documents:document_file_page_multiple_enable', data={
                'id_list': self.test_document_file_page.pk
            }
        )


class DocumentFilePageViewTestMixin:
    def _request_test_document_file_page_count_update_view(self):
        return self.post(
            viewname='documents:document_file_page_count_update',
            kwargs={'document_file_id': self.test_document_file.pk}
        )

    def _request_test_document_multiple_page_count_update_view(self):
        return self.post(
            viewname='documents:document_file_multiple_page_count_update',
            data={'id_list': self.test_document_file.pk}
        )

    def _request_test_document_file_page_list_view(self):
        return self.get(
            viewname='documents:document_file_pages', kwargs={
                'document_id': self.test_document.pk
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
