from ..models import Index, IndexTemplateNode

from .literals import (
    TEST_INDEX_LABEL, TEST_INDEX_LABEL_EDITED, TEST_INDEX_SLUG,
    TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION,
    TEST_INDEX_TEMPLATE_NODE_EXPRESSION_EDITED,
    TEST_INDEX_TEMPLATE_NODE_EXPRESSION
)


class DocumentIndexAPIViewTestMixin:
    def _request_test_document_index_instance_list_api_view(self):
        return self.get(
            viewname='rest_api:document-index-list', kwargs={
                'document_id': self.test_document.pk
            }
        )


class DocumentIndexViewTestMixin:
    def _request_test_document_index_list_view(self):
        return self.get(
            viewname='indexing:document_index_list', kwargs={
                'document_id': self.test_document.pk
            }
        )


class IndexInstanceAPIViewTestMixin:
    def _request_test_index_instance_list_api_view(self):
        return self.get(viewname='rest_api:indexinstance-list')

    def _request_test_index_instance_detail_api_view(self):
        return self.get(
            viewname='rest_api:indexinstance-detail', kwargs={
                'index_instance_id': self.test_index.pk
            }
        )


class IndexInstanceNodeAPIViewTestMixin:
    def _request_test_index_instance_node_list_api_view(self):
        return self.get(
            viewname='rest_api:indexinstancenode-list', kwargs={
                'index_instance_id': self.test_index.pk
            }
        )

    def _request_test_index_instance_node_detail_api_view(self):
        return self.get(
            viewname='rest_api:indexinstancenode-detail', kwargs={
                'index_instance_id': self.test_index.pk,
                'index_instance_node_id': self.test_index_instance_node.pk
            }
        )

    def _request_test_index_instance_node_document_list_api_view(self):
        return self.get(
            viewname='rest_api:indexinstancenode-document-list', kwargs={
                'index_instance_id': self.test_index.pk,
                'index_instance_node_id': self.test_index_instance_node.pk
            }
        )


class IndexInstaceViewTestMixin(object):
    def _request_test_index_instance_node_view(self, index_instance_node):
        return self.get(
            viewname='indexing:index_instance_node_view', kwargs={
                'index_instance_node_id': index_instance_node.pk
            }
        )


class IndexTemplateNodeViewTestMixin(object):
    def _request_test_index_node_create_view(self):
        return self.post(
            viewname='indexing:template_node_create', kwargs={
                'index_template_node_id': self.test_index.template_root.pk
            }, data={
                'expression_template': TEST_INDEX_TEMPLATE_NODE_EXPRESSION,
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
                'expression_template': TEST_INDEX_TEMPLATE_NODE_EXPRESSION_EDITED,
                'index': self.test_index.pk
            }
        )

    def _request_test_index_node_list_get_view(self):
        return self.get(
            viewname='indexing:index_setup_view', kwargs={
                'index_template_id': self.test_index.pk
            }
        )


class IndexTestMixin(object):
    def setUp(self):
        super().setUp()
        self.test_indexes = []
        self._test_indexes_data = [
            {'label': TEST_INDEX_LABEL, 'slug': TEST_INDEX_SLUG},
            {
                'label': '{}_1'.format(TEST_INDEX_LABEL),
                'slug': '{}_1'.format(TEST_INDEX_SLUG)
            },
        ]

    def _create_test_index(self, extra_data=None, rebuild=False):
        data = self._test_indexes_data[len(self.test_indexes)]

        if extra_data:
            data.update(extra_data)

        # Create empty index
        self.test_index = Index.objects.create(**data)

        self.test_indexes.append(self.test_index)

        # Add our document type to the new index
        if hasattr(self, 'test_document_type'):
            self.test_index.document_types.add(self.test_document_type)

        # Rebuild indexes
        if rebuild:
            Index.objects.rebuild()

    def _create_test_index_template_node(self, rebuild=False):
        self.test_index_template_node = self.test_index.node_templates.create(
            parent=self.test_index.template_root,
            expression=TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION,
            link_documents=True
        )

        if rebuild:
            Index.objects.rebuild()
            self.test_index_instance_node = self.test_index.instance_root.get_children().first()


class IndexTemplateAPIViewTestMixin(object):
    def _request_test_index_template_create_api_view(self):
        return self.post(
            viewname='rest_api:indextemplate-list', data={
                'label': TEST_INDEX_LABEL, 'slug': TEST_INDEX_SLUG,
                'document_types': self.test_document_type.pk
            }
        )

    def _request_test_index_template_delete_api_view(self):
        return self.delete(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': self.test_index.pk
            }
        )

    def _request_test_index_template_detail_api_view(self):
        return self.get(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': self.test_index.pk
            }
        )

    def _request_test_index_template_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': self.test_index.pk
            }, data={'label': TEST_INDEX_LABEL_EDITED}
        )

    def _request_test_index_template_list_api_view(self):
        return self.get(viewname='rest_api:indextemplate-list')


class IndexTemplateNodeAPITestMixin:
    def _request_test_index_template_node_create_api_view(self, extra_data=None):
        data = {
            'expression': TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION
        }

        if extra_data:
            data.update(extra_data)

        values = list(IndexTemplateNode.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='rest_api:indextemplatenode-list', kwargs={
                'index_template_id': self.test_index.pk
            }, data=data
        )
        self.test_index_template_node = IndexTemplateNode.objects.exclude(
            pk__in=values
        ).first()

        return response

    def _request_test_index_template_node_delete_api_view(self):
        return self.delete(
            viewname='rest_api:indextemplatenode-detail', kwargs={
                'index_template_id': self.test_index.pk,
                'index_template_node_id': self.test_index_template_node.pk,
            }
        )

    def _request_test_index_template_node_detail_api_view(self):
        return self.get(
            viewname='rest_api:indextemplatenode-detail', kwargs={
                'index_template_id': self.test_index.pk,
                'index_template_node_id': self.test_index_template_node.pk,
            }
        )

    def _request_test_index_template_node_edit_via_patch_api_view(self):
        data = {
            'enabled': self.test_index_template_node.enabled,
            'expression': self.test_index_template_node.expression,
            'index': self.test_index.pk,
            'link_documents': self.test_index_template_node.link_documents,
            'parent': self.test_index_template_node.parent.pk,
        }
        data['expression'] = TEST_INDEX_TEMPLATE_NODE_EXPRESSION_EDITED

        return self.patch(
            viewname='rest_api:indextemplatenode-detail', kwargs={
                'index_template_id': self.test_index.pk,
                'index_template_node_id': self.test_index_template_node.pk,
            }, data=data
        )

    def _request_test_index_template_node_list_api_view(self):
        return self.get(
            viewname='rest_api:indextemplatenode-list', kwargs={
                'index_template_id': self.test_index.pk,
            }
        )


class IndexToolsViewTestMixin(object):
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
