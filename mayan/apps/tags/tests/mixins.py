from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH

from django.db.models import Q

from ..models import Tag

from .literals import (
    TEST_TAG_COLOR, TEST_TAG_COLOR_EDITED, TEST_TAG_LABEL,
    TEST_TAG_LABEL_EDITED
)


class DocumentTagViewTestMixin:
    def _request_test_document_tag_attach_view(self):
        return self.post(
            viewname='tags:tag_attach', kwargs={
                'document_id': self.test_document.pk
            }, data={
                'tags': self.test_tag.pk,
                'user': self._test_case_user.pk
            }
        )

    def _request_test_document_multiple_tag_multiple_attach_view(self):
        return self.post(
            viewname='tags:multiple_documents_tag_attach', data={
                'id_list': self.test_document.pk, 'tags': self.test_tag.pk,
                'user': self._test_case_user.pk
            }
        )

    def _request_test_document_tag_multiple_remove_view(self):
        return self.post(
            viewname='tags:single_document_multiple_tag_remove', kwargs={
                'document_id': self.test_document.pk
            }, data={
                'tags': self.test_tag.pk,
            }
        )

    def _request_test_document_multiple_tag_remove_view(self):
        return self.post(
            viewname='tags:multiple_documents_selection_tag_remove', data={
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

    def _request_test_tag_document_list_view(self):
        return self.get(
            viewname='tags:tag_document_list', kwargs={
                'tag_id': self.test_tag.pk
            }
        )


class TagAPIViewTestMixin:
    def _request_test_document_tag_attach_api_view(self):
        return self.post(
            viewname='rest_api:document-tag-attach', kwargs={
                'document_id': self.test_document.pk
            }, data={'tag': self.test_tag.pk}
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
            }, data={'tag': self.test_tag.pk}
        )

    def _request_test_tag_create_api_view(self):
        pk_list = list(Tag.objects.values('pk'))

        response = self.post(
            viewname='rest_api:tag-list', data={
                'label': TEST_TAG_LABEL, 'color': TEST_TAG_COLOR
            }
        )

        try:
            self.test_tag = Tag.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Tag.DoesNotExist:
            self.test_tag = None

        return response

    def _request_test_tag_delete_api_view(self):
        return self.delete(
            viewname='rest_api:tag-detail',
            kwargs={'tag_id': self.test_tag.pk}
        )

    def _request_test_tag_detail_api_view(self):
        return self.get(
            viewname='rest_api:tag-detail',
            kwargs={'tag_id': self.test_tag.pk}
        )

    def _request_test_tag_document_list_api_view(self):
        return self.get(
            viewname='rest_api:tag-document-list', kwargs={
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
            viewname='rest_api:tag-detail',
            kwargs={'tag_id': self.test_tag.pk},
            data=data
        )

    def _request_test_tag_list_api_view(self):
        return self.get(viewname='rest_api:tag-list')


class TagTestMixin:
    def setUp(self):
        super().setUp()
        self.test_tags = []

    def _create_test_tag(self, add_test_document=False):
        total_test_labels = len(self.test_tags)
        label = '{}_{}'.format(TEST_TAG_LABEL, total_test_labels)

        self.test_tag = Tag.objects.create(
            color=TEST_TAG_COLOR, label=label
        )

        self.test_tags.append(self.test_tag)

        if add_test_document:
            self.test_tag.documents.add(self.test_document)


class TagViewTestMixin:
    def _request_test_tag_create_view(self):
        pk_list = list(Tag.objects.values('pk'))

        response = self.post(
            viewname='tags:tag_create', data={
                'label': TEST_TAG_LABEL,
                'color': TEST_TAG_COLOR
            }
        )

        try:
            self.test_tag = Tag.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Tag.DoesNotExist:
            self.test_tag = None

        return response

    def _request_test_tag_delete_view(self):
        return self.post(
            viewname='tags:tag_delete', kwargs={'tag_id': self.test_tag.pk}
        )

    def _request_test_tag_delete_multiple_view(self):
        return self.post(
            viewname='tags:tag_multiple_delete', data={
                'id_list': self.test_tag.pk
            },
        )

    def _request_test_tag_edit_view(self):
        return self.post(
            viewname='tags:tag_edit', kwargs={
                'tag_id': self.test_tag.pk
            }, data={
                'label': TEST_TAG_LABEL_EDITED, 'color': TEST_TAG_COLOR_EDITED
            }
        )

    def _request_test_tag_list_view(self):
        return self.get(viewname='tags:tag_list')


class TaggedDocumentUploadWizardStepViewTestMixin:
    def _request_upload_interactive_document_create_view(self):
        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_upload_interactive', kwargs={
                    'source_id': self.test_source.pk
                }, data={
                    'document_type_id': self.test_document_type.pk,
                    'source-file': file_object,
                    'tags': Tag.objects.values_list('pk', flat=True)
                }
            )
