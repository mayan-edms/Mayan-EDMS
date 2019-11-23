from __future__ import unicode_literals

from ..models import Index

from .literals import (
    TEST_INDEX_LABEL, TEST_INDEX_LABEL_EDITED, TEST_INDEX_SLUG,
    TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION
)


class IndexTestMixin(object):
    def _create_test_index(self, rebuild=False):
        # Create empty index
        self.test_index = Index.objects.create(label=TEST_INDEX_LABEL)

        # Add our document type to the new index
        if hasattr(self, 'test_document_type'):
            self.test_index.document_types.add(self.test_document_type)

        # Rebuild indexes
        if rebuild:
            Index.objects.rebuild()

    def _create_test_index_template_node(self):
        self.test_index.node_templates.create(
            parent=self.test_index.template_root,
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION,
            link_documents=True
        )


class IndexViewTestMixin(object):
    def _request_test_index_create_view(self):
        # Typecast to list to force queryset evaluation
        values = list(Index.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='indexing:index_setup_create', data={
                'label': TEST_INDEX_LABEL, 'slug': TEST_INDEX_SLUG
            }
        )

        self.test_index = Index.objects.exclude(pk__in=values).first()

        return response

    def _request_test_index_delete_view(self):
        return self.post(
            viewname='indexing:index_setup_delete', kwargs={
                'pk': self.test_index.pk
            }
        )

    def _request_test_index_edit_view(self):
        return self.post(
            viewname='indexing:index_setup_edit', kwargs={
                'pk': self.test_index.pk
            }, data={
                'label': TEST_INDEX_LABEL_EDITED, 'slug': TEST_INDEX_SLUG
            }
        )

    def _request_test_index_rebuild_view(self):
        return self.post(
            viewname='indexing:index_setup_rebuild', kwargs={
                'pk': self.test_index.pk
            }
        )
