from __future__ import unicode_literals

from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH

from ..models import Tag

from .literals import (
    TEST_TAG_COLOR, TEST_TAG_COLOR_EDITED, TEST_TAG_LABEL, TEST_TAG_LABEL_2,
    TEST_TAG_LABEL_EDITED
)


class DocumentTagAPIViewTestMixin(object):
    def _request_test_document_tag_attach_api_view(self):
        return self.post(
            viewname='rest_api:document-tag-attach', kwargs={
                'document_id': self.test_document.pk
            }, data={'tag_id': self.test_tag.pk}
        )

    def _request_test_document_tag_list_api_view(self):
        return self.get(
            viewname='rest_api:document-tag-list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_tag_remove_api_view(self):
        return self.post(
            viewname='rest_api:document-tag-remove', kwargs={
                'document_id': self.test_document.pk
            }, data={'tag_id': self.test_tag.pk}
        )


class TagAPIViewTestMixin(object):
    def _request_test_tag_create_api_view(self):
        return self.post(
            viewname='rest_api:tag-list', data={
                'label': TEST_TAG_LABEL, 'color': TEST_TAG_COLOR
            }
        )

    def _request_test_tag_destroy_api_view(self):
        return self.delete(
            viewname='rest_api:tag-detail', kwargs={
                'tag_id': self.test_tag.pk
            }
        )

    def _request_test_tag_edit_api_view(self, extra_data=None, verb='patch'):
        data = {
            'label': TEST_TAG_LABEL_EDITED,
            'color': TEST_TAG_COLOR_EDITED
        }

        if extra_data:
            data.update(extra_data)

        return getattr(self, verb)(
            viewname='rest_api:tag-detail', kwargs={
                'tag_id': self.test_tag.pk
            }, data=data
        )

    def _request_test_tag_list_api_view(self):
        return self.get(viewname='rest_api:tag-list')

    def _request_test_tag_retrieve_api_view(self):
        return self.get(
            viewname='rest_api:tag-detail', kwargs={
                'tag_id': self.test_tag.pk
            }
        )


class TagDocumentAPIViewTestMixin(object):
    def _request_test_tag_document_attach_api_view(self):
        return self.post(
            viewname='rest_api:tag-document-attach', kwargs={
                'tag_id': self.test_tag.pk
            }, data={'document_id': self.test_document.pk}
        )

    def _request_test_tag_document_list_api_view(self):
        return self.get(
            viewname='rest_api:tag-document-list', kwargs={
                'tag_id': self.test_tag.pk
            }
        )

    def _request_test_tag_document_remove_api_view(self):
        return self.post(
            viewname='rest_api:tag-document-remove', kwargs={
                'tag_id': self.test_tag.pk
            }, data={'document_id': self.test_document.pk}
        )


class TagTestMixin(object):
    def _create_test_tag(self):
        self.test_tag = Tag.objects.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL
        )

    def _create_test_tag_2(self):
        self.test_tag_2 = Tag.objects.create(
            color=TEST_TAG_COLOR, label=TEST_TAG_LABEL_2
        )


class TagViewTestMixin(object):
    def _request_test_document_tag_attach_view(self):
        return self.post(
            viewname='tags:document_tag_multiple_attach', kwargs={
                'document_id': self.test_document.pk
            }, data={
                'tags': self.test_tag.pk,
                'user': self._test_case_user.pk
            }
        )

    def _request_test_document_multiple_tag_multiple_attach_view(self):
        return self.post(
            viewname='tags:documents_multiple_tag_multiple_attach', data={
                'id_list': self.test_document.pk, 'tags': self.test_tag.pk,
                'user': self._test_case_user.pk
            }
        )

    def _request_test_document_tag_multiple_remove_view(self):
        return self.post(
            viewname='tags:document_tag_multiple_remove',
            kwargs={'document_id': self.test_document.pk}, data={
                'tags': self.test_tag.pk,
            }
        )

    def _request_test_document_multiple_tag_remove_view(self):
        return self.post(
            viewname='tags:documents_multiple_tag_multiple_remove',
            data={
                'id_list': self.test_document.pk,
                'tags': self.test_tag.pk,
            }
        )

    def _request_test_document_tag_list_view(self):
        return self.get(
            viewname='tags:document_tag_list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_tag_create_view(self):
        return self.post(
            viewname='tags:tag_create', data={
                'label': TEST_TAG_LABEL,
                'color': TEST_TAG_COLOR
            }
        )

    def _request_test_tag_destroy_multiple_view(self):
        return self.post(
            viewname='tags:tag_multiple_delete',
            data={'id_list': self.test_tag.pk},
        )

    def _request_test_tag_destroy_view(self):
        return self.post(
            viewname='tags:tag_delete', kwargs={'tag_id': self.test_tag.pk}
        )

    def _request_test_tag_document_list_view(self):
        return self.get(
            viewname='tags:tag_document_list', kwargs={
                'tag_id': self.test_tag.pk
            }
        )

    def _request_test_tag_edit_view(self):
        return self.post(
            viewname='tags:tag_edit', kwargs={
                'tag_id': self.test_tag.pk
            }, data={
                'label': TEST_TAG_LABEL_EDITED,
                'color': TEST_TAG_COLOR_EDITED
            }
        )

    def _request_test_tag_list_view(self):
        return self.get(viewname='tags:tag_list')


class TaggedDocumentUploadViewTestMixin(object):
    def _request_upload_interactive_document_create_view(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_upload_interactive', kwargs={
                    'source_id': self.test_source.pk
                }, data={
                    'document_type_id': self.test_document_type.pk,
                    'source-file': file_object,
                    'tags': Tag.objects.values_list('pk', flat=True)
                }
            )
