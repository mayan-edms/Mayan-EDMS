from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.utils import encapsulate
from common.views import AssignRemoveView, SingleObjectListView
from common.widgets import two_state_template
from documents.models import Document, DocumentType
from documents.permissions import permission_document_view
from documents.views import document_list
from permissions import Permission

from .forms import IndexForm, IndexTemplateNodeForm
from .models import Index, IndexInstanceNode, IndexTemplateNode
from .permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_edit,
    permission_document_indexing_rebuild_indexes,
    permission_document_indexing_setup, permission_document_indexing_view
)
from .tasks import task_do_rebuild_all_indexes
from .widgets import index_instance_item_link, get_breadcrumbs, node_level


# Setup views
class SetupIndexListView(SingleObjectListView):
    model = Index
    view_permission = permission_document_indexing_setup

    def get_extra_context(self):
        return {
            'title': _('Indexes'),
            'hide_object': True,
            'extra_columns': [
                {'name': _('Name'), 'attribute': 'name'},
                {'name': _('Title'), 'attribute': 'title'},
                {'name': _('Enabled'), 'attribute': encapsulate(lambda x: two_state_template(x.enabled))},
            ]
        }


def index_setup_create(request):
    Permission.check_permissions(request.user, [permission_document_indexing_create])

    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Index created successfully.'))
            return HttpResponseRedirect(reverse('indexing:index_setup_list'))
    else:
        form = IndexForm()

    return render_to_response('appearance/generic_form.html', {
        'title': _('Create index'),
        'form': form,
    }, context_instance=RequestContext(request))


def index_setup_edit(request, index_pk):
    index = get_object_or_404(Index, pk=index_pk)

    try:
        Permission.check_permissions(request.user, [permission_document_indexing_edit])
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_indexing_create, request.user, index)

    if request.method == 'POST':
        form = IndexForm(request.POST, instance=index)
        if form.is_valid():
            form.save()
            messages.success(request, _('Index edited successfully'))
            return HttpResponseRedirect(reverse('indexing:index_setup_list'))
    else:
        form = IndexForm(instance=index)

    return render_to_response('appearance/generic_form.html', {
        'title': _('Edit index: %s') % index,
        'form': form,
        'index': index,
        'navigation_object_list': ['index'],
    }, context_instance=RequestContext(request))


def index_setup_delete(request, index_pk):
    index = get_object_or_404(Index, pk=index_pk)

    try:
        Permission.check_permissions(request.user, [permission_document_indexing_delete])
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_indexing_delete, request.user, index)

    post_action_redirect = reverse('indexing:index_setup_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        try:
            index.delete()
            messages.success(request, _('Index: %s deleted successfully.') % index)
        except Exception as exception:
            messages.error(request, _('Index: %(index)s delete error: %(error)s') % {
                'index': index, 'error': exception})

        return HttpResponseRedirect(next)

    context = {
        'index': index,
        'navigation_object_list': ['index'],
        'delete_view': True,
        'previous': previous,
        'next': next,
        'title': _('Are you sure you with to delete the index: %s?') % index,
    }

    return render_to_response('appearance/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def index_setup_view(request, index_pk):
    index = get_object_or_404(Index, pk=index_pk)

    try:
        Permission.check_permissions(request.user, [permission_document_indexing_setup])
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_indexing_setup, request.user, index)

    object_list = index.template_root.get_descendants(include_self=True)

    context = {
        'object_list': object_list,
        'index': index,
        'navigation_object_list': ['index'],
        'title': _('Tree template nodes for index: %s') % index,
        'hide_object': True,
        'extra_columns': [
            {'name': _('Level'), 'attribute': encapsulate(lambda x: node_level(x))},
            {'name': _('Enabled'), 'attribute': encapsulate(lambda x: two_state_template(x.enabled))},
            {'name': _('Has document links?'), 'attribute': encapsulate(lambda x: two_state_template(x.link_documents))},
        ],
    }

    return render_to_response('appearance/generic_list.html', context,
                              context_instance=RequestContext(request))


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
        return AssignRemoveView.generate_choices(DocumentType.objects.exclude(pk__in=self.get_object().document_types.all()))

    def right_list(self):
        return AssignRemoveView.generate_choices(self.get_object().document_types.all())

    def remove(self, item):
        self.get_object().document_types.remove(item)

    def get_context_data(self, **kwargs):
        data = super(SetupIndexDocumentTypesView, self).get_context_data(**kwargs)
        data.update({
            'object': self.get_object(),
            'title': _('Document types linked to index: %s') % self.get_object()
        })

        return data


# Node views
def template_node_create(request, parent_pk):
    parent_node = get_object_or_404(IndexTemplateNode, pk=parent_pk)

    try:
        Permission.check_permissions(request.user, [permission_document_indexing_edit])
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_indexing_edit, request.user, parent_node.index)

    if request.method == 'POST':
        form = IndexTemplateNodeForm(request.POST)
        if form.is_valid():
            node = form.save()
            messages.success(request, _('Index template node created successfully.'))
            return HttpResponseRedirect(reverse('indexing:index_setup_view', args=[node.index.pk]))
    else:
        form = IndexTemplateNodeForm(initial={'index': parent_node.index, 'parent': parent_node})

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'index': parent_node.index,
        'navigation_object_list': ['index'],
        'title': _('Create child node'),
    }, context_instance=RequestContext(request))


def template_node_edit(request, node_pk):
    node = get_object_or_404(IndexTemplateNode, pk=node_pk)

    try:
        Permission.check_permissions(request.user, [permission_document_indexing_edit])
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_indexing_edit, request.user, node.index)

    if request.method == 'POST':
        form = IndexTemplateNodeForm(request.POST, instance=node)
        if form.is_valid():
            form.save()
            messages.success(request, _('Index template node edited successfully'))
            return HttpResponseRedirect(reverse('indexing:index_setup_view', args=[node.index.pk]))
    else:
        form = IndexTemplateNodeForm(instance=node)

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'index': node.index,
        'navigation_object_list': ['index', 'node'],
        'node': node,
        'title': _('Edit index template node: %s') % node,
    }, context_instance=RequestContext(request))


def template_node_delete(request, node_pk):
    node = get_object_or_404(IndexTemplateNode, pk=node_pk)

    try:
        Permission.check_permissions(request.user, [permission_document_indexing_edit])
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_indexing_edit, request.user, node.index)

    post_action_redirect = reverse('indexing:index_setup_view', args=[node.index.pk])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        try:
            node.delete()
            messages.success(request, _('Node: %s deleted successfully.') % node)
        except Exception as exception:
            messages.error(request, _('Node: %(node)s delete error: %(error)s') % {
                'node': node, 'error': exception})

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'index': node.index,
        'navigation_object_list': ['index', 'node'],
        'next': next,
        'node': node,
        'title': _('Are you sure you with to delete the index template node: %s?') % node,
        'previous': previous,
    }

    return render_to_response('appearance/generic_confirm.html', context,
                              context_instance=RequestContext(request))


class IndexListView(SingleObjectListView):
    @staticmethod
    def get_items_count(instance):
        try:
            if instance.template_root.link_documents:
                return instance.instance_root.documents.count()
            else:
                return instance.instance_root.get_children().count()
        except IndexInstanceNode.DoesNotExist:
            return 0

    queryset = Index.objects.filter(enabled=True)
    object_permission = permission_document_indexing_view

    def get_extra_context(self):
        return {
            'title': _('Indexes'),
            'hide_links': True,
            'extra_columns': [
                {'name': _('Items'), 'attribute': encapsulate(lambda instance: IndexListView.get_items_count(instance))},
                {'name': _('Document types'), 'attribute': 'get_document_types_names'},
            ],
        }


def index_instance_node_view(request, index_instance_node_pk):
    """
    Show an instance node and it's content, whether is other child nodes
    of documents
    """
    index_instance = get_object_or_404(IndexInstanceNode, pk=index_instance_node_pk)
    index_instance_list = index_instance.get_children().order_by('value')
    breadcrumbs = get_breadcrumbs(index_instance)

    try:
        Permission.check_permissions(request.user, [permission_document_indexing_view])
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_indexing_view, request.user, index_instance.index)

    title = mark_safe(_('Contents for index: %s') % breadcrumbs)

    if index_instance:
        if index_instance.index_template_node.link_documents:
            # Document list, use the document_list view for consistency
            return document_list(
                request,
                title=title,
                object_list=index_instance.documents.all(),
                extra_context={
                    'object': index_instance
                }
            )

    return render_to_response('appearance/generic_list.html', {
        'object_list': index_instance_list,
        'extra_columns': [
            {
                'name': _('Node'),
                'attribute': encapsulate(lambda x: index_instance_item_link(x))
            },
            {
                'name': _('Items'),
                'attribute': encapsulate(lambda x: x.documents.count() if x.index_template_node.link_documents else x.get_children().count())
            }
        ],
        'title': title,
        'hide_links': True,
        'hide_object': True,
        'object': index_instance

    }, context_instance=RequestContext(request))


def rebuild_index_instances(request):
    """
    Confirmation view to execute the tool: do_rebuild_all_indexes
    """
    Permission.check_permissions(request.user, [permission_document_indexing_rebuild_indexes])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method != 'POST':
        return render_to_response('appearance/generic_confirm.html', {
            'previous': previous,
            'next': next,
            'title': _('Are you sure you wish to rebuild all indexes?'),
            'message': _('On large databases this operation may take some time to execute.'),
        }, context_instance=RequestContext(request))
    else:
        task_do_rebuild_all_indexes.apply_async(queue='tools')
        messages.success(request, _('Index rebuild queued successfully.'))
        return HttpResponseRedirect(next)


def document_index_list(request, document_id):
    """
    Show a list of indexes where the current document can be found
    """
    document = get_object_or_404(Document, pk=document_id)
    object_list = []

    queryset = document.node_instances.all()
    try:
        # TODO: should be AND not OR
        Permission.check_permissions(request.user, [permission_document_view, permission_document_indexing_view])
    except PermissionDenied:
        queryset = AccessControlList.objects.filter_by_access(permission_document_indexing_view, request.user, queryset, related='index')

    for index_instance in queryset:
        object_list.append(get_breadcrumbs(index_instance, single_link=True, include_count=True))

    return render_to_response('appearance/generic_list.html', {
        'object_list': object_list,
        'object': document,
        'hide_link': True,
        'title': _('Indexes containing document: %s') % document,
    }, context_instance=RequestContext(request))
