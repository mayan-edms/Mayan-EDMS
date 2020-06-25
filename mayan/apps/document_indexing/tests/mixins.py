from ..models import Index

from .literals import (
    TEST_INDEX_LABEL, TEST_INDEX_LABEL_EDITED, TEST_INDEX_SLUG,
    TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION,
    TEST_INDEX_TEMPLATE_NODE_TEMPLATE_EDITED,
    TEST_INDEX_TEMPLATE_NODE_TEMPLATE
)


class DocumentIndexViewTestMixin:
    def _request_test_document_index_list_view(self):
        return self.get(
            viewname='indexing:document_index_list', kwargs={
                'document_id': self.test_document.pk
            }
        )


class IndexInstaceViewTestMixin:
    def _request_test_index_instance_node_view(self, index_instance_node):
        return self.get(
            viewname='indexing:index_instance_node_view', kwargs={
                'index_instance_node_id': index_instance_node.pk
            }
        )


class IndexTemplateNodeViewTestMixin:
    def _request_test_index_node_create_view(self):
        return self.post(
            viewname='indexing:template_node_create', kwargs={
                'index_template_node_id': self.test_index.template_root.pk
            }, data={
                'expression_template': TEST_INDEX_TEMPLATE_NODE_TEMPLATE,
                'index': self.test_index.pk,
                'link_document': True
            }
        )

    def _request_test_index_node_delete_view(self):
        return self.post(
            viewname='indexing:template_node_delete', kwargs={
                'index_template_node_id': self.test_index_template_node.pk
            }
        )

    def _request_test_index_node_edit_view(self):
        return self.post(
            viewname='indexing:template_node_edit', kwargs={
                'index_template_node_id': self.test_index_template_node.pk
            }, data={
                'expression_template': TEST_INDEX_TEMPLATE_NODE_TEMPLATE_EDITED,
                'index': self.test_index.pk
            }
        )

    def _request_test_index_node_list_get_view(self):
        return self.get(
            viewname='indexing:index_setup_view', kwargs={
                'index_template_id': self.test_index.pk
            }
        )


class IndexTestMixin:
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
        self.test_index_template_node = self.test_index.node_templates.create(
            parent=self.test_index.template_root,
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION,
            link_documents=True
        )


class IndexToolsViewTestMixin:
    def _request_indexes_rebuild_get_view(self):
        return self.get(
            viewname='indexing:rebuild_index_instances'
        )

    def _request_indexes_rebuild_post_view(self):
        return self.post(
            viewname='indexing:rebuild_index_instances', data={
                'index_templates': self.test_index.pk
            }
        )

    def _request_indexes_reset_get_view(self):
        return self.get(
            viewname='indexing:index_instances_reset'
        )

    def _request_indexes_reset_post_view(self):
        return self.post(
            viewname='indexing:index_instances_reset', data={
                'index_templates': self.test_index.pk
            }
        )


class IndexViewTestMixin:
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
                'index_template_id': self.test_index.pk
            }
        )

    def _request_test_index_document_type_view(self):
        return self.get(
            viewname='indexing:index_setup_document_types', kwargs={
                'index_template_id': self.test_index.pk
            }
        )

    def _request_test_index_edit_view(self):
        return self.post(
            viewname='indexing:index_setup_edit', kwargs={
                'index_template_id': self.test_index.pk
            }, data={
                'label': TEST_INDEX_LABEL_EDITED, 'slug': TEST_INDEX_SLUG
            }
        )

    def _request_test_index_rebuild_view(self):
        return self.post(
            viewname='indexing:index_setup_rebuild', kwargs={
                'index_template_id': self.test_index.pk
            }
        )
