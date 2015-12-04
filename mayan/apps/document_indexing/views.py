from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.views import (
    AssignRemoveView, ConfirmView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from documents.models import Document, DocumentType
from documents.permissions import permission_document_view
from documents.views import DocumentListView
from permissions import Permission

from .forms import IndexTemplateNodeForm
from .models import (
    DocumentIndexInstanceNode, Index, IndexInstance, IndexInstanceNode,
    IndexTemplateNode
)
from .permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_edit,
    permission_document_indexing_rebuild_indexes,
    permission_document_indexing_setup, permission_document_indexing_view
)
from .tasks import task_do_rebuild_all_indexes
from .widgets import get_breadcrumbs


# Setup views
class SetupIndexCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create index')}
    fields = ('label', 'slug', 'enabled')
    model = Index
    post_action_redirect = reverse_lazy('indexing:index_setup_list')
    view_permission = permission_document_indexing_create


class SetupIndexListView(SingleObjectListView):
    model = Index
    view_permission = permission_document_indexing_setup

    def get_extra_context(self):
        return {
            'hide_object': True,
            'title': _('Indexes'),
        }


class SetupIndexEditView(SingleObjectEditView):
    fields = ('label', 'slug', 'enabled')
    model = Index
    post_action_redirect = reverse_lazy('indexing:index_setup_list')
    view_permission = permission_document_indexing_edit

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit index: %s') % self.get_object(),
        }


class SetupIndexDeleteView(SingleObjectDeleteView):
    model = Index
    post_action_redirect = reverse_lazy('indexing:index_setup_list')
    view_permission = permission_document_indexing_delete

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Delete the index: %s?') % self.get_object(),
        }


class SetupIndexTreeTemplateListView(SingleObjectListView):
    view_permission = permission_document_indexing_setup

    def get_index(self):
        return get_object_or_404(Index, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_index().template_root.get_descendants(
            include_self=True
        )

    def get_extra_context(self):
        return {
            'hide_object': True,
            'index': self.get_index(),
            'navigation_object_list': ('index',),
            'title': _('Tree template nodes for index: %s') % self.get_index(),
        }


class SetupIndexDocumentTypesView(AssignRemoveView):
    decode_content_type = True
    object_permission = permission_document_indexing_edit
    left_list_title = _('Available document types')
    right_list_title = _('Document types linked')

    def add(self, item):
        self.get_object().document_types.add(item)

    def get_object(self):
        return get_object_or_404(Index, pk=self.kwargs['pk'])

    def left_list(self):
        return AssignRemoveView.generate_choices(
            DocumentType.objects.exclude(
                pk__in=self.get_object().document_types.all()
            )
        )

    def right_list(self):
        return AssignRemoveView.generate_choices(
            self.get_object().document_types.all()
        )

    def remove(self, item):
        self.get_object().document_types.remove(item)

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _(
                'Document types linked to index: %s'
            ) % self.get_object()
        }


# Node views
def template_node_create(request, parent_pk):
    parent_node = get_object_or_404(IndexTemplateNode, pk=parent_pk)

    try:
        Permission.check_permissions(
            request.user, (permission_document_indexing_edit,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_document_indexing_edit, request.user, parent_node.index
        )

    if request.method == 'POST':
        form = IndexTemplateNodeForm(request.POST)
        if form.is_valid():
            node = form.save()
            messages.success(
                request, _('Index template node created successfully.')
            )
            return HttpResponseRedirect(
                reverse('indexing:index_setup_view', args=(node.index.pk,))
            )
    else:
        form = IndexTemplateNodeForm(
            initial={'index': parent_node.index, 'parent': parent_node}
        )

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'index': parent_node.index,
        'navigation_object_list': ('index',),
        'title': _('Create child node'),
    }, context_instance=RequestContext(request))


def template_node_edit(request, node_pk):
    node = get_object_or_404(IndexTemplateNode, pk=node_pk)

    try:
        Permission.check_permissions(
            request.user, (permission_document_indexing_edit,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_document_indexing_edit, request.user, node.index
        )

    if request.method == 'POST':
        form = IndexTemplateNodeForm(request.POST, instance=node)
        if form.is_valid():
            form.save()
            messages.success(
                request, _('Index template node edited successfully')
            )
            return HttpResponseRedirect(
                reverse('indexing:index_setup_view', args=(node.index.pk,))
            )
    else:
        form = IndexTemplateNodeForm(instance=node)

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'index': node.index,
        'navigation_object_list': ('index', 'node'),
        'node': node,
        'title': _('Edit index template node: %s') % node,
    }, context_instance=RequestContext(request))


class TemplateNodeDeleteView(SingleObjectDeleteView):
    model = IndexTemplateNode
    view_permission = permission_document_indexing_edit

    def get_extra_context(self):
        return {
            'index': self.get_object().index,
            'navigation_object_list': ('index', 'node'),
            'node': self.get_object(),
            'title': _(
                'Delete the index template node: %s?'
            ) % self.get_object(),
        }

    def get_post_action_redirect(self):
        return reverse(
            'indexing:index_setup_view', args=(self.get_object().index.pk,)
        )


class IndexListView(SingleObjectListView):
    object_permission = permission_document_indexing_view
    queryset = IndexInstance.objects.filter(enabled=True)

    def get_extra_context(self):
        return {
            'hide_links': True,
            'title': _('Indexes'),
        }


class IndexInstanceNodeView(DocumentListView, SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        self.index_instance = get_object_or_404(
            IndexInstanceNode, pk=self.kwargs['pk']
        )

        try:
            Permission.check_permissions(
                request.user, (permission_document_indexing_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_indexing_view,
                request.user, self.index_instance.index
            )

        if self.index_instance:
            if self.index_instance.index_template_node.link_documents:
                return DocumentListView.dispatch(
                    self, request, *args, **kwargs
                )

        return SingleObjectListView.dispatch(self, request, *args, **kwargs)

    def get_queryset(self):
        if self.index_instance:
            if self.index_instance.index_template_node.link_documents:
                return DocumentListView.get_queryset(self)
            else:
                self.object_permission = None
                return self.index_instance.get_children().order_by('value')
        else:
            self.object_permission = None
            return IndexInstanceNode.objects.none()

    def get_document_queryset(self):
        if self.index_instance:
            if self.index_instance.index_template_node.link_documents:
                return self.index_instance.documents.all()

    def get_extra_context(self):
        context = {
            'hide_links': True,
            'object': self.index_instance,
            'title': mark_safe(
                _(
                    'Contents for index: %s'
                ) % get_breadcrumbs(self.index_instance)
            )
        }

        if self.index_instance and not self.index_instance.index_template_node.link_documents:
            context.update({'hide_object': True})

        return context


class DocumentIndexNodeListView(SingleObjectListView):
    """
    Show a list of indexes where the current document can be found
    """

    object_permission = permission_document_indexing_view
    object_permission_related = 'index'

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, request.user, self.get_document()
            )

        return super(
            DocumentIndexNodeListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.get_document(),
            'title': _(
                'Indexes nodes containing document: %s'
            ) % self.get_document(),
        }

    def get_queryset(self):
        return DocumentIndexInstanceNode.objects.get_for(self.get_document())


class RebuildIndexesConfirmView(ConfirmView):
    extra_context = {
        'message': _('On large databases this operation may take some time to execute.'),
        'title': _('Rebuild all indexes?'),
    }
    view_permission = permission_document_indexing_rebuild_indexes

    def get_post_action_redirect(self):
        return reverse('common:tools_list')

    def view_action(self):
        task_do_rebuild_all_indexes.apply_async()
        messages.success(self.request, _('Index rebuild queued successfully.'))
