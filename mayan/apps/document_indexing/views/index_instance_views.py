from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import SingleObjectListView
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..html_widgets import node_tree
from ..icons import icon_index
from ..links import link_index_template_create
from ..models import (
    DocumentIndexInstanceNode, IndexInstance, IndexInstanceNode
)
from ..permissions import permission_index_instance_view

__all__ = (
    'DocumentIndexInstanceNodeListView', 'IndexInstanceListView',
    'IndexInstanceNodeView'
)


class IndexInstanceListView(SingleObjectListView):
    object_permission = permission_index_instance_view

    def get_extra_context(self):
        return {
            'hide_links': True,
            'hide_object': True,
            'no_results_icon': icon_index,
            'no_results_main_link': link_index_template_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'This could mean that no index templates have been '
                'created or that there are index templates '
                'but they are no properly defined.'
            ),
            'no_results_title': _('There are no index instances available.'),
            'title': _('Indexes'),
        }

    def get_source_queryset(self):
        queryset = IndexInstance.objects.filter(enabled=True)
        return queryset.filter(
            node_templates__index_instance_nodes__isnull=False
        ).distinct()


class IndexInstanceNodeView(DocumentListView):
    template_name = 'document_indexing/node_details.html'

    def dispatch(self, request, *args, **kwargs):
        self.index_instance_node = self.get_index_instance_node()

        if self.index_instance_node:
            if self.index_instance_node.index_template_node.link_documents:
                return super().dispatch(request=request, *args, **kwargs)

        return SingleObjectListView.dispatch(
            self, request=request, *args, **kwargs
        )

    def get_document_queryset(self):
        if self.index_instance_node:
            if self.index_instance_node.index_template_node.link_documents:
                return self.index_instance_node.get_documents()

        return Document.valid.none()

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'column_class': 'col-xs-12 col-sm-6 col-md-4 col-lg-3',
                'navigation': mark_safe(
                    _('Navigation: %s') % node_tree(
                        node=self.index_instance_node, user=self.request.user
                    )
                ),
                'object': self.index_instance_node,
                'title': _(
                    'Contents for index: %s'
                ) % self.index_instance_node.get_full_path(),
            }
        )

        if self.index_instance_node and not self.index_instance_node.index_template_node.link_documents:
            context.update(
                {
                    'hide_object': True,
                    'list_as_items': False,
                }
            )

        return context

    def get_index_instance_node(self):
        instance = get_object_or_404(
            klass=IndexInstanceNode, pk=self.kwargs['index_instance_node_id']
        )
        AccessControlList.objects.check_access(
            obj=instance, permissions=(
                permission_index_instance_view,
            ), user=self.request.user
        )
        return instance

    def get_source_queryset(self):
        if self.index_instance_node:
            if self.index_instance_node.index_template_node.link_documents:
                return super().get_source_queryset()
            else:
                self.object_permission = None
                return self.index_instance_node.get_children().order_by(
                    'value'
                )
        else:
            self.object_permission = None
            return IndexInstanceNode.objects.none()


class DocumentIndexInstanceNodeListView(ExternalObjectViewMixin, SingleObjectListView):
    """
    Show a list of indexes where the current document can be found
    """
    external_object_permission = permission_index_instance_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid
    object_permission = permission_index_instance_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_index,
            'no_results_text': _(
                'Assign the document type of this document '
                'to an index to have it appear in instances of '
                'those indexes organization units. '
            ),
            'no_results_title': _(
                'This document is not in any index'
            ),
            'object': self.external_object,
            'title': _(
                'Indexes nodes containing document: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return DocumentIndexInstanceNode.objects.get_for(
            document=self.external_object
        )
