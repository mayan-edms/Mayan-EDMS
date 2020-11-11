import os
import time

from django.conf import settings

from mayan.apps.converter.classes import Layer
from mayan.apps.converter.layers import layer_saved_transformations

from ..literals import PAGE_RANGE_ALL
from ..models import Document, DocumentType, FavoriteDocument

from .literals import (
    TEST_DOCUMENT_DESCRIPTION_EDITED, TEST_DOCUMENT_PATH,
    TEST_DOCUMENT_TYPE_DELETE_PERIOD, TEST_DOCUMENT_TYPE_DELETE_TIME_UNIT,
    TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_LABEL_EDITED,
    TEST_DOCUMENT_TYPE_QUICK_LABEL, TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED,
    TEST_DOCUMENT_VERSION_COMMENT_EDITED, TEST_SMALL_DOCUMENT_FILENAME,
    TEST_SMALL_DOCUMENT_PATH, TEST_TRANSFORMATION_ARGUMENT,
    TEST_TRANSFORMATION_CLASS, TEST_VERSION_COMMENT
)


class DocumentAPIViewTestMixin:
    def _request_test_document_api_download_view(self):
        return self.get(
            viewname='rest_api:document-download', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_document_api_upload_view(self):
        with open(file=TEST_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='rest_api:document-list', data={
                    'document_type': self.test_document_type.pk,
                    'file': file_object
                }
            )

    def _request_test_document_description_api_edit_via_patch_view(self):
        return self.patch(
            viewname='rest_api:document-detail', kwargs={
                'pk': self.test_document.pk
            }, data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def _request_test_document_description_api_edit_via_put_view(self):
        return self.put(
            viewname='rest_api:document-detail', kwargs={
                'pk': self.test_document.pk
            }, data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def _request_test_document_document_type_change_api_view(self):
        return self.post(
            viewname='rest_api:document-type-change', kwargs={
                'pk': self.test_document.pk
            }, data={'new_document_type': self.test_document_type_2.pk}
        )


class DocumentPageAPIViewTestMixin:
    def _request_document_page_image(self):
        page = self.test_document.pages.first()
        return self.get(
            viewname='rest_api:documentpage-image', kwargs={
                'pk': page.document_version.document_id, 'version_pk': page.document_version_id,
                'page_pk': page.pk
            }
        )


class DocumentPageDisableViewTestMixin:
    def _disable_test_document_page(self):
        self.test_document_page.enabled = False
        self.test_document_page.save()

    def _request_test_document_page_disable_view(self):
        return self.post(
            viewname='documents:document_page_disable', kwargs={
                'document_page_id': self.test_document_page.pk
            }
        )

    def _request_test_document_page_enable_view(self):
        return self.post(
            viewname='documents:document_page_enable', kwargs={
                'document_page_id': self.test_document_page.pk
            }
        )

    def _request_test_document_page_multiple_disable_view(self):
        return self.post(
            viewname='documents:document_page_multiple_disable', data={
                'id_list': self.test_document_page.pk
            }
        )

    def _request_test_document_page_multiple_enable_view(self):
        return self.post(
            viewname='documents:document_page_multiple_enable', data={
                'id_list': self.test_document_page.pk
            }
        )


class DocumentPageViewTestMixin:
    def _request_test_document_page_list_view(self):
        return self.get(
            viewname='documents:document_pages', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_page_rotate_left_view(self):
        return self.post(
            viewname='documents:document_page_rotate_left', kwargs={
                'document_page_id': self.test_document_page.pk
            }
        )

    def _request_test_document_page_rotate_right_view(self):
        return self.post(
            viewname='documents:document_page_rotate_right', kwargs={
                'document_page_id': self.test_document_page.pk
            }
        )

    def _request_test_document_page_view(self, document_page):
        return self.get(
            viewname='documents:document_page_view', kwargs={
                'document_page_id': document_page.pk,
            }
        )

    def _request_test_document_page_zoom_in_view(self):
        return self.post(
            viewname='documents:document_page_zoom_in', kwargs={
                'document_page_id': self.test_document_page.pk
            }
        )

    def _request_test_document_page_zoom_out_view(self):
        return self.post(
            viewname='documents:document_page_zoom_out', kwargs={
                'document_page_id': self.test_document_page.pk
            }
        )


class DocumentQuickLabelViewTestMixin:
    def _request_document_quick_label_edit_view(self, extra_data=None):
        data = {
            'document_type_available_filenames': self.test_document_type_filename.pk,
            'label': ''
            # View needs at least an empty label for quick
            # label to work. Cause is unknown.
        }
        data.update(extra_data or {})

        return self.post(
            viewname='documents:document_edit', kwargs={
                'document_id': self.test_document.pk
            }, data=data
        )


class DocumentTestMixin:
    auto_create_test_document_type = True
    auto_upload_test_document = True
    test_document_filename = TEST_SMALL_DOCUMENT_FILENAME
    test_document_path = None

    def setUp(self):
        super(DocumentTestMixin, self).setUp()
        Layer.invalidate_cache()

        self.test_documents = []

        if self.auto_create_test_document_type:
            self._create_test_document_type()

            if self.auto_upload_test_document:
                self._upload_test_document()

    def tearDown(self):
        for document_type in DocumentType.objects.all():
            document_type.delete()
        super(DocumentTestMixin, self).tearDown()

    def _create_test_document_stub(self):
        self.test_document_stub = Document.objects.create(
            document_type=self.test_document_type, label='document_stub'
        )

    def _create_test_document_type(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def _calculate_test_document_path(self):
        if not self.test_document_path:
            self.test_document_path = os.path.join(
                settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
                'sample_documents', self.test_document_filename
            )

    def _upload_test_document(self, label=None, _user=None):
        self._calculate_test_document_path()

        if not label:
            label = self.test_document_filename

        with open(file=self.test_document_path, mode='rb') as file_object:
            self.test_document, self.test_document_version = self.test_document_type.new_document(
                file_object=file_object, label=label, _user=_user
            )

        self.test_documents.append(self.test_document)
        self.test_document_page = self.test_document_version.pages.first()


class DocumentTypeAPIViewTestMixin:
    def _request_test_document_type_api_create_view(self):
        return self.post(
            viewname='rest_api:documenttype-list', data={
                'label': TEST_DOCUMENT_TYPE_LABEL
            }
        )

    def _request_test_document_type_api_delete_view(self):
        return self.delete(
            viewname='rest_api:documenttype-detail', kwargs={
                'pk': self.test_document_type.pk,
            }
        )

    def _request_test_document_type_api_patch_view(self):
        return self.patch(
            viewname='rest_api:documenttype-detail', kwargs={
                'pk': self.test_document_type.pk,
            }, data={'label': TEST_DOCUMENT_TYPE_LABEL_EDITED}
        )

    def _request_test_document_type_api_put_view(self):
        return self.put(
            viewname='rest_api:documenttype-detail', kwargs={
                'pk': self.test_document_type.pk,
            }, data={'label': TEST_DOCUMENT_TYPE_LABEL_EDITED}
        )


class DocumentTypeDeletionPoliciesViewTestMixin:
    def _request_document_type_filename_generator_get_view(self):
        return self.get(
            viewname='documents:document_type_policies', kwargs={
                'document_type_id': self.test_document_type.pk
            }
        )


class DocumentTypeFilenameGeneratorViewTestMixin:
    def _request_document_type_filename_generator_get_view(self):
        return self.get(
            viewname='documents:document_type_filename_generator', kwargs={
                'document_type_id': self.test_document_type.pk
            }
        )


class DocumentTypeQuickLabelViewTestMixin:
    def _request_quick_label_create(self):
        return self.post(
            viewname='documents:document_type_filename_create', kwargs={
                'document_type_id': self.test_document_type.pk
            }, data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL,
            }
        )

    def _request_quick_label_delete(self):
        return self.post(
            viewname='documents:document_type_filename_delete', kwargs={
                'document_type_filename_id': self.test_document_type_filename.pk
            }
        )

    def _request_quick_label_edit(self):
        return self.post(
            viewname='documents:document_type_filename_edit', kwargs={
                'document_type_filename_id': self.test_document_type_filename.pk
            }, data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED,
            }
        )

    def _request_quick_label_list_view(self):
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


class DocumentVersionAPIViewTestMixin:
    def _request_test_document_version_api_download_view(self):
        return self.get(
            viewname='rest_api:documentversion-download', kwargs={
                'pk': self.test_document.pk,
                'version_pk': self.test_document.latest_version.pk,
            }
        )

    def _request_test_document_version_api_edit_via_patch_view(self):
        return self.patch(
            viewname='rest_api:documentversion-detail', kwargs={
                'pk': self.test_document.pk,
                'version_pk': self.test_document.latest_version.pk
            }, data={'comment': TEST_DOCUMENT_VERSION_COMMENT_EDITED}
        )

    def _request_test_document_version_api_edit_via_put_view(self):
        return self.put(
            viewname='rest_api:documentversion-detail', kwargs={
                'pk': self.test_document.pk,
                'version_pk': self.test_document.latest_version.pk
            }, data={'comment': TEST_DOCUMENT_VERSION_COMMENT_EDITED}
        )

    def _request_test_document_version_api_list_view(self):
        return self.get(
            viewname='rest_api:document-version-list', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_document_version_api_revert_view(self):
        return self.delete(
            viewname='rest_api:documentversion-detail', kwargs={
                'pk': self.test_document.pk,
                'version_pk': self.test_document.latest_version.pk
            }
        )

    def _request_test_document_version_api_upload_view(self):
        # Artificial delay since MySQL doesn't store microsecond data in
        # timestamps. Version timestamp is used to determine which version
        # is the latest.
        time.sleep(1)

        with open(file=TEST_DOCUMENT_PATH, mode='rb') as file_descriptor:
            return self.post(
                viewname='rest_api:document-version-list', kwargs={
                    'pk': self.test_document.pk,
                }, data={
                    'comment': '', 'file': file_descriptor,
                }
            )


class DocumentVersionTestMixin:
    def _upload_new_version(self):
        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_version(
                comment=TEST_VERSION_COMMENT, file_object=file_object
            )


class DocumentVersionViewTestMixin:
    def _request_document_version_download(self, data=None):
        data = data or {}
        return self.get(
            viewname='documents:document_version_download', kwargs={
                'document_version_id': self.test_document.latest_version.pk
            }, data=data
        )

    def _request_document_version_list_view(self):
        return self.get(
            viewname='documents:document_version_list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_document_version_revert_view(self, document_version):
        return self.post(
            viewname='documents:document_version_revert', kwargs={
                'document_version_id': document_version.pk
            }
        )


class DocumentViewTestMixin:
    def _create_document_transformation(self):
        layer_saved_transformations.add_transformation_to(
            obj=self.test_document.pages.first(),
            transformation_class=TEST_TRANSFORMATION_CLASS,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )

    def _request_test_document_clear_transformations_view(self):
        return self.post(
            viewname='documents:document_clear_transformations',
            kwargs={'document_id': self.test_document.pk}
        )

    def _request_test_document_download_form_get_view(self):
        return self.get(
            viewname='documents:document_download_form', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_download_form_post_view(self):
        return self.post(
            viewname='documents:document_download_form', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_download_view(self):
        return self.get(
            viewname='documents:document_download', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_multiple_download_view(self):
        return self.get(
            viewname='documents:document_multiple_download',
            data={'id_list': self.test_document.pk}
        )

    def _request_test_document_list_view(self):
        return self.get(viewname='documents:document_list')

    def _request_test_document_preview_view(self):
        return self.get(
            viewname='documents:document_preview', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_print_view(self):
        return self.get(
            viewname='documents:document_print', kwargs={
                'document_id': self.test_document.pk,
            }, data={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_properties_view(self):
        return self.get(
            viewname='documents:document_properties', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_properties_edit_get_view(self):
        return self.get(
            viewname='documents:document_edit', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_type_edit_get_view(self):
        return self.get(
            viewname='documents:document_document_type_edit', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_type_edit_post_view(self, document_type):
        return self.post(
            viewname='documents:document_document_type_edit', kwargs={
                'document_id': self.test_document.pk
            }, data={'document_type': document_type.pk}
        )

    def _request_test_document_multiple_type_edit(self, document_type):
        return self.post(
            viewname='documents:document_multiple_document_type_edit',
            data={
                'id_list': self.test_document.pk,
                'document_type': document_type.pk
            }
        )

    def _request_test_document_update_page_count_view(self):
        return self.post(
            viewname='documents:document_update_page_count',
            kwargs={'document_id': self.test_document.pk}
        )

    def _request_test_document_multiple_update_page_count_view(self):
        return self.post(
            viewname='documents:document_multiple_update_page_count',
            data={'id_list': self.test_document.pk}
        )

    def _request_test_document_multiple_clear_transformations(self):
        return self.post(
            viewname='documents:document_multiple_clear_transformations',
            data={'id_list': self.test_document.pk}
        )

    def _request_empty_trash_view(self):
        return self.post(viewname='documents:trash_can_empty')


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


class DuplicatedDocumentsViewsTestMixin:
    def _request_document_duplicates_list_view(self):
        return self.get(
            viewname='documents:document_duplicates_list', kwargs={
                'document_id': self.test_documents[0].pk
            }
        )

    def _request_duplicated_document_list_view(self):
        return self.get(viewname='documents:duplicated_document_list')

    def _upload_duplicate_document(self):
        self._upload_test_document()


class FavoriteDocumentsTestMixin:
    def _request_document_add_to_favorites_view(self):
        return self.post(
            viewname='documents:document_add_to_favorites',
            kwargs={'document_id': self.test_document.pk}
        )

    def _document_add_to_favorites(self):
        FavoriteDocument.objects.add_for_user(
            document=self.test_document, user=self._test_case_user
        )

    def _request_document_list_favorites(self):
        return self.get(
            viewname='documents:document_list_favorites',
        )

    def _request_document_remove_from_favorites(self):
        return self.post(
            viewname='documents:document_remove_from_favorites',
            kwargs={'document_id': self.test_document.pk}
        )


class TrashedDocumentAPIViewTestMixin:
    def _request_test_document_api_trash_view(self):
        return self.delete(
            viewname='rest_api:document-detail', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_trashed_document_api_delete_view(self):
        return self.delete(
            viewname='rest_api:trasheddocument-detail', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_trashed_document_api_detail_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-detail', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_trashed_document_api_image_view(self):
        latest_version = self.test_document.latest_version

        return self.get(
            viewname='rest_api:documentpage-image', kwargs={
                'pk': latest_version.document_id,
                'version_pk': latest_version.pk,
                'page_pk': latest_version.pages.first().pk
            }
        )

    def _request_test_trashed_document_api_list_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-list'
        )

    def _request_test_trashed_document_api_restore_view(self):
        return self.post(
            viewname='rest_api:trasheddocument-restore', kwargs={
                'pk': self.test_document.pk
            }
        )


class TrashedDocumentViewTestMixin:
    def _request_document_trash_get_view(self):
        return self.get(
            viewname='documents:document_trash', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_document_trash_post_view(self):
        return self.post(
            viewname='documents:document_trash', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_trashed_document_restore_get_view(self):
        return self.get(
            viewname='documents:document_restore', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_trashed_document_restore_post_view(self):
        return self.post(
            viewname='documents:document_restore', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_trashed_document_delete_get_view(self):
        return self.get(
            viewname='documents:document_delete', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_trashed_document_delete_post_view(self):
        return self.post(
            viewname='documents:document_delete', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_trashed_document_list_view(self):
        return self.get(viewname='documents:document_list_deleted')
