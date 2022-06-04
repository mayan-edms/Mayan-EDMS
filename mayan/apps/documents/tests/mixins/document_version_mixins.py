from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from mayan.apps.converter.layers import layer_saved_transformations

from ...document_version_modifications import (
    DocumentVersionModificationPagesAppend,
    DocumentVersionModificationPagesReset
)
from ...literals import PAGE_RANGE_ALL
from ...models.document_version_models import DocumentVersion
from ...models.document_version_page_models import DocumentVersionPage

from ..literals import (
    TEST_DOCUMENT_VERSION_COMMENT_EDITED, TEST_TRANSFORMATION_ARGUMENT,
    TEST_TRANSFORMATION_CLASS
)


class DocumentVersionAPIViewTestMixin:
    def _request_test_document_version_create_api_view(self):
        pk_list = list(DocumentVersion.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='rest_api:documentversion-list', kwargs={
                'document_id': self._test_document.pk
            }
        )

        try:
            self._test_document_version = DocumentVersion.objects.get(
                ~Q(pk__in=pk_list)
            )
        except DocumentVersion.DoesNotExist:
            self._test_document_version = None

        return response

    def _request_test_document_version_delete_api_view(self):
        return self.delete(
            viewname='rest_api:documentversion-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document.version_active.pk
            }
        )

    def _request_test_document_version_detail_api_view(self):
        return self.get(
            viewname='rest_api:documentversion-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document.version_active.pk
            }
        )

    def _request_test_document_version_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:documentversion-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document.version_active.pk
            }, data={'comment': TEST_DOCUMENT_VERSION_COMMENT_EDITED}
        )

    def _request_test_document_version_edit_via_put_api_view(self):
        return self.put(
            viewname='rest_api:documentversion-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document.version_active.pk
            }, data={
                'active': True,
                'comment': TEST_DOCUMENT_VERSION_COMMENT_EDITED
            }
        )

    def _request_test_document_version_export_api_view_via_get(self):
        return self.get(
            viewname='rest_api:documentversion-export', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document.version_active.pk,
            }
        )

    def _request_test_document_version_export_api_view_via_post(self):
        return self.post(
            viewname='rest_api:documentversion-export', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document.version_active.pk,
            }
        )

    def _request_test_document_version_list_api_view(self):
        return self.get(
            viewname='rest_api:documentversion-list', kwargs={
                'document_id': self._test_document.pk
            }
        )


class DocumentVersionLinkTestMixin:
    def _resolve_test_document_version_link(self, test_link):
        self.add_test_view(test_object=self._test_document_version)
        context = self.get_test_view()
        return test_link.resolve(context=context)


class DocumentVersionModificationAPIViewTestMixin:
    def _request_test_document_version_action_page_append_api_view(self):
        return self.post(
            viewname='rest_api:documentversion-modify', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document_version.pk
            }, data={
                'backend_id': DocumentVersionModificationPagesAppend.backend_id
            }
        )

    def _request_test_document_version_action_page_reset_api_view(self):
        return self.post(
            viewname='rest_api:documentversion-modify', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document_version.pk
            }, data={
                'backend_id': DocumentVersionModificationPagesReset.backend_id
            }
        )


class DocumentVersionModificationViewTestMixin:
    def _request_test_document_version_action_page_append_view(self):
        return self.post(
            viewname='documents:document_version_modify', kwargs={
                'document_version_id': self._test_document_version.pk
            }, data={
                'backend': DocumentVersionModificationPagesAppend.backend_id
            }
        )

    def _request_test_document_version_action_page_reset_view(self):
        return self.post(
            viewname='documents:document_version_modify', kwargs={
                'document_version_id': self._test_document_version.pk
            }, data={
                'backend': DocumentVersionModificationPagesReset.backend_id
            }
        )


class DocumentVersionPageAPIViewTestMixin:
    def _request_test_document_version_page_create_api_view(self):
        pk_list = list(DocumentVersionPage.objects.values_list('pk', flat=True))

        content_type = ContentType.objects.get_for_model(
            model=self._test_document_file_page
        )

        response = self.post(
            viewname='rest_api:documentversionpage-list', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document_version.pk
            }, data={
                'content_type_id': content_type.pk,
                'object_id': self._test_document_file_page.pk,
                'page_number': self._test_document_file_page.page_number + 2
            }
        )

        try:
            self._test_document_version_page = DocumentVersionPage.objects.get(
                ~Q(pk__in=pk_list)
            )
        except DocumentVersionPage.DoesNotExist:
            self._test_document_version_page = None

        return response

    def _request_test_document_version_page_delete_api_view(self):
        return self.delete(
            viewname='rest_api:documentversionpage-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document_version.pk,
                'document_version_page_id': self._test_document_version_page.pk
            }
        )

    def _request_test_document_version_page_detail_api_view(self):
        return self.get(
            viewname='rest_api:documentversionpage-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document_version.pk,
                'document_version_page_id': self._test_document_version_page.pk
            }
        )

    def _request_test_document_version_page_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:documentversionpage-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document_version.pk,
                'document_version_page_id': self._test_document_version_page.pk
            }, data={
                'content_type_id': self._test_document_version_page.content_type.pk,
                'page_number': self._test_document_version_page.page_number + 1
            }
        )

    def _request_test_document_version_page_edit_via_put_api_view(self):
        return self.put(
            viewname='rest_api:documentversionpage-detail', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document_version.pk,
                'document_version_page_id': self._test_document_version_page.pk
            }, data={
                'content_type_id': self._test_document_version_page.content_type.pk,
                'object_id': self._test_document_version_page.object_id,
                'page_number': self._test_document_version_page.page_number + 1
            }
        )

    def _request_test_document_version_page_image_api_view(self):
        return self.get(
            viewname='rest_api:documentversionpage-image', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document_version.pk,
                'document_version_page_id': self._test_document_version_page.pk
            }
        )

    def _request_test_document_version_page_list_api_view(self):
        return self.get(
            viewname='rest_api:documentversionpage-list', kwargs={
                'document_id': self._test_document.pk,
                'document_version_id': self._test_document_version.pk,
            }
        )


class DocumentVersionTestMixin:
    auto_create_test_document_version = False

    def setUp(self):
        super().setUp()
        self._test_document_versions = []
        if self.auto_create_test_document_version:
            self._create_test_document_version()

    def _create_test_document_version(self):
        self._test_document_version = self._test_document.versions.create()
        self._test_document_versions.append(self._test_document_version)

        self._document_version_page_source_object = self._test_document
        content_type = ContentType.objects.get_for_model(
            model=self._document_version_page_source_object
        )

        self._test_document_version_page = DocumentVersionPage.objects.create(
            content_type=content_type,
            document_version=self._test_document_version,
            object_id=self._document_version_page_source_object.pk
        )


class DocumentVersionViewTestMixin:
    def _request_test_document_version_active_view(self):
        return self.post(
            viewname='documents:document_version_active', kwargs={
                'document_version_id': self._test_document_version.pk
            }
        )

    def _request_test_document_version_single_delete_view(self):
        return self.post(
            viewname='documents:document_version_single_delete', kwargs={
                'document_version_id': self._test_document_version.pk
            }
        )

    def _request_test_document_version_multiple_delete_view(self):
        return self.post(
            viewname='documents:document_version_multiple_delete', data={
                'id_list': self._test_document_version.pk
            }
        )

    def _request_test_document_version_edit_view(self):
        return self.post(
            viewname='documents:document_version_edit', kwargs={
                'document_version_id': self._test_document_version.pk
            }, data={
                'comment': TEST_DOCUMENT_VERSION_COMMENT_EDITED
            }
        )

    def _request_test_document_version_export_view(self):
        return self.post(
            viewname='documents:document_version_export', kwargs={
                'document_version_id': self._test_document_version.pk
            }
        )

    def _request_test_document_version_list_view(self):
        return self.get(
            viewname='documents:document_version_list', kwargs={
                'document_id': self._test_document.pk
            }
        )

    def _request_test_document_version_preview_view(self):
        return self.get(
            viewname='documents:document_version_preview', kwargs={
                'document_version_id': self._test_document_version.pk
            }
        )

    def _request_test_document_version_print_form_view(self):
        return self.get(
            viewname='documents:document_version_print_form', kwargs={
                'document_version_id': self._test_document_version.pk,
            }, data={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_version_print_view(self):
        return self.get(
            viewname='documents:document_version_print_view', kwargs={
                'document_version_id': self._test_document_version.pk,
            }, query={
                'page_group': PAGE_RANGE_ALL
            }
        )


class DocumentVersionPageViewTestMixin:
    def _request_test_document_version_page_delete_view(self):
        return self.post(
            viewname='documents:document_version_page_delete', kwargs={
                'document_version_page_id': self._test_document_version_page.pk,
            }
        )

    def _request_test_document_version_page_list_view(self):
        return self.get(
            viewname='documents:document_version_page_list', kwargs={
                'document_version_id': self._test_document_version.pk
            }
        )

    def _request_test_document_version_page_rotate_left_view(self):
        return self.post(
            viewname='documents:document_version_page_rotate_left', kwargs={
                'document_version_page_id': self._test_document_version_page.pk
            }
        )

    def _request_test_document_version_page_rotate_right_view(self):
        return self.post(
            viewname='documents:document_version_page_rotate_right', kwargs={
                'document_version_page_id': self._test_document_version_page.pk
            }
        )

    def _request_test_document_version_page_view(self, document_version_page):
        return self.get(
            viewname='documents:document_version_page_view', kwargs={
                'document_version_page_id': document_version_page.pk,
            }
        )

    def _request_test_document_version_page_zoom_in_view(self):
        return self.post(
            viewname='documents:document_version_page_zoom_in', kwargs={
                'document_version_page_id': self._test_document_version_page.pk
            }
        )

    def _request_test_document_version_page_zoom_out_view(self):
        return self.post(
            viewname='documents:document_version_page_zoom_out', kwargs={
                'document_version_page_id': self._test_document_version_page.pk
            }
        )


class DocumentVersionPageRemapViewTestMixin:
    def _request_test_document_version_page_list_remap_view(self, data):
        return self.post(
            viewname='documents:document_version_page_list_remap', kwargs={
                'document_version_id': self._test_document_version.pk
            }, data=data
        )


class DocumentVersionTransformationTestMixin:
    def _create_document_version_transformation(self):
        layer_saved_transformations.add_transformation_to(
            obj=self._test_document_version.pages.first(),
            transformation_class=TEST_TRANSFORMATION_CLASS,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )


class DocumentVersionTransformationViewTestMixin:
    def _request_test_document_version_transformations_clear_view(self):
        return self.post(
            viewname='documents:document_version_transformations_clear',
            kwargs={'document_version_id': self._test_document_version.pk}
        )

    def _request_test_document_version_multiple_transformations_clear_view(self):
        return self.post(
            viewname='documents:document_version_multiple_transformations_clear',
            data={'id_list': self._test_document_version.pk}
        )

    def _request_test_document_version_transformations_clone_view(self):
        return self.post(
            viewname='documents:document_version_transformations_clone',
            kwargs={'document_version_id': self._test_document_version.pk}, data={
                'page': self._test_document_version.pages.first().pk
            }
        )
