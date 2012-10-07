from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.utils.html import mark_safe
from django.conf import settings

from permissions.models import Permission
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from documents.models import Document
from documents.views import document_list
from common.utils import encapsulate, generate_choices_w_labels
from common.views import assign_remove
from common.widgets import two_state_template
from acls.utils import apply_default_acls
from acls.models import AccessEntry

from .forms import IndexForm, IndexTemplateNodeForm
from .models import (Index, IndexTemplateNode, IndexInstanceNode)
from .tools import do_rebuild_all_indexes
from .widgets import (index_instance_item_link, get_breadcrumbs, node_level)
from .permissions import (PERMISSION_DOCUMENT_INDEXING_VIEW,
    PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES,
    PERMISSION_DOCUMENT_INDEXING_SETUP,
    PERMISSION_DOCUMENT_INDEXING_CREATE,
    PERMISSION_DOCUMENT_INDEXING_EDIT,
    PERMISSION_DOCUMENT_INDEXING_DELETE
)


# Setup views
def index_setup_list(request):
    context = {
        'title': _(u'indexes'),
        'hide_object': True,
        'list_object_variable_name': 'index',
        'extra_columns': [
            {'name': _(u'name'), 'attribute': 'name'},
            {'name': _(u'title'), 'attribute': 'title'},
            {'name': _(u'enabled'), 'attribute': encapsulate(lambda x: two_state_template(x.enabled))},
        ]
    }

    queryset = Index.objects.all()

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_SETUP])
    except PermissionDenied:
        queryset = AccessEntry.objects.filter_objects_by_access(PERMISSION_DOCUMENT_INDEXING_SETUP, request.user, queryset)

    context['object_list'] = queryset

    return render_to_response('generic_list.html',
        context,
        context_instance=RequestContext(request)
    )


def index_setup_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_CREATE])

    if request.method == 'POST':
        form = IndexForm(request.POST)
        if form.is_valid():
            index = form.save()
            apply_default_acls(index, request.user)
            messages.success(request, _(u'Index created successfully.'))
            return HttpResponseRedirect(reverse('index_setup_list'))
    else:
        form = IndexForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create index'),
        'form': form,
    },
    context_instance=RequestContext(request))


def index_setup_edit(request, index_pk):
    index = get_object_or_404(Index, pk=index_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_INDEXING_CREATE, request.user, index)

    if request.method == 'POST':
        form = IndexForm(request.POST, instance=index)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Index edited successfully'))
            return HttpResponseRedirect(reverse('index_setup_list'))
    else:
        form = IndexForm(instance=index)

    return render_to_response('generic_form.html', {
        'title': _(u'edit index: %s') % index,
        'form': form,
        'index': index,
        'object_name': _(u'index'),
        'navigation_object_name': 'index',
    },
    context_instance=RequestContext(request))


def index_setup_delete(request, index_pk):
    index = get_object_or_404(Index, pk=index_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_DELETE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_INDEXING_DELETE, request.user, index)

    post_action_redirect = reverse('index_setup_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            index.delete()
            messages.success(request, _(u'Index: %s deleted successfully.') % index)
        except Exception, e:
            messages.error(request, _(u'Index: %(index)s delete error: %(error)s') % {
                'index': index, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'index': index,
        'object_name': _(u'index'),
        'navigation_object_name': 'index',
        'delete_view': True,
        'previous': previous,
        'next': next,
        'title': _(u'Are you sure you with to delete the index: %s?') % index,
        'form_icon': u'tab_delete.png',
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def index_setup_view(request, index_pk):
    index = get_object_or_404(Index, pk=index_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_SETUP])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_INDEXING_SETUP, request.user, index)

    object_list = index.template_root.get_descendants(include_self=True)

    context = {
        'object_list': object_list,
        'index': index,
        'object_name': _(u'index'),
        'list_object_variable_name': 'node',
        'navigation_object_name': 'index',
        'title': _(u'tree template nodes for index: %s') % index,
        'hide_object': True,
        'extra_columns': [
            {'name': _(u'level'), 'attribute': encapsulate(lambda x: node_level(x))},
            {'name': _(u'enabled'), 'attribute': encapsulate(lambda x: two_state_template(x.enabled))},
            {'name': _(u'has document links?'), 'attribute': encapsulate(lambda x: two_state_template(x.link_documents))},            
        ],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def index_setup_document_types(request, index_pk):
    index = get_object_or_404(Index, pk=index_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_INDEXING_EDIT, request.user, index)

    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(index.get_document_types_not_in_index(), display_object_type=False),
        right_list=lambda: generate_choices_w_labels(index.get_index_document_types(), display_object_type=False),
        add_method=lambda x: index.document_types.add(x),
        remove_method=lambda x: index.document_types.remove(x),
        left_list_title=_(u'document types not in index: %s') % index,
        right_list_title=_(u'document types for index: %s') % index,
        decode_content_type=True,
        extra_context={
            'navigation_object_name': 'index',
            'index': index,
            'object_name': _(u'index'),
        }
    )


# Node views
def template_node_create(request, parent_pk):
    parent_node = get_object_or_404(IndexTemplateNode, pk=parent_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_INDEXING_EDIT, request.user, parent_node.index)

    if request.method == 'POST':
        form = IndexTemplateNodeForm(request.POST)
        if form.is_valid():
            node = form.save()
            messages.success(request, _(u'Index template node created successfully.'))
            return HttpResponseRedirect(reverse('index_setup_view', args=[node.index.pk]))
    else:
        form = IndexTemplateNodeForm(initial={'index': parent_node.index, 'parent': parent_node})

    return render_to_response('generic_form.html', {
        'title': _(u'create child node'),
        'form': form,
        'index': parent_node.index,
        'object_name': _(u'index'),
        'navigation_object_name': 'index',
    },
    context_instance=RequestContext(request))


def template_node_edit(request, node_pk):
    node = get_object_or_404(IndexTemplateNode, pk=node_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_INDEXING_EDIT, request.user, node.index)

    if request.method == 'POST':
        form = IndexTemplateNodeForm(request.POST, instance=node)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Index template node edited successfully'))
            return HttpResponseRedirect(reverse('index_setup_view', args=[node.index.pk]))
    else:
        form = IndexTemplateNodeForm(instance=node)

    return render_to_response('generic_form.html', {
        'title': _(u'edit index template node: %s') % node,
        'form': form,
        'index': node.index,
        'node': node,

        'navigation_object_list': [
            {'object': 'index', 'name': _(u'index')},
            {'object': 'node', 'name': _(u'node')}
        ],
    },
    context_instance=RequestContext(request))


def template_node_delete(request, node_pk):
    node = get_object_or_404(IndexTemplateNode, pk=node_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_INDEXING_EDIT, request.user, node.index)

    post_action_redirect = reverse('index_setup_view', args=[node.index.pk])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            node.delete()
            messages.success(request, _(u'Node: %s deleted successfully.') % node)
        except Exception, e:
            messages.error(request, _(u'Node: %(node)s delete error: %(error)s') % {
                'node': node, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'next': next,
        'title': _(u'Are you sure you with to delete the index template node: %s?') % node,
        'form_icon': u'textfield_delete.png',
        'index': node.index,
        'node': node,

        'navigation_object_list': [
            {'object': 'index', 'name': _(u'index')},
            {'object': 'node', 'name': _(u'node')}
        ],
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


# User views
def index_list(request):
    """
    Show a list of enabled indexes
    """
    context = {
        'title': _(u'indexes'),
        'hide_links': True,
        'extra_columns': [
            {'name': _(u'nodes'), 'attribute': 'get_instance_node_count'},
            {'name': _(u'document types'), 'attribute': 'get_document_types_names'},
        ],
    }

    queryset = Index.objects.filter(enabled=True)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_VIEW])
    except PermissionDenied:
        queryset = AccessEntry.objects.filter_objects_by_access(PERMISSION_DOCUMENT_INDEXING_VIEW, request.user, queryset)

    context['object_list'] = queryset

    return render_to_response('generic_list.html',
        context,
        context_instance=RequestContext(request)
    )


def index_instance_node_view(request, index_instance_node_pk):
    """
    Show an instance node and it's content, whether is other child nodes
    of documents
    """
    index_instance = get_object_or_404(IndexInstanceNode, pk=index_instance_node_pk)
    index_instance_list = [index for index in index_instance.get_children().order_by('value')]
    breadcrumbs = get_breadcrumbs(index_instance)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_INDEXING_VIEW, request.user, index_instance.index)

    title = mark_safe(_(u'contents for index: %s') % breadcrumbs)

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

    return render_to_response('generic_list.html', {
        'object_list': index_instance_list,
        'extra_columns_preffixed': [
            {
                'name': _(u'node'),
                'attribute': encapsulate(lambda x: index_instance_item_link(x))
            },
            {
                'name': _(u'items'),
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
    Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))

    if request.method != 'POST':
        return render_to_response('generic_confirm.html', {
            'previous': previous,
            'next': next,
            'title': _(u'Are you sure you wish to rebuild all indexes?'),
            'message': _(u'On large databases this operation may take some time to execute.'),
            'form_icon': u'folder_page.png',
        }, context_instance=RequestContext(request))
    else:
        try:
            warnings = do_rebuild_all_indexes()
            messages.success(request, _(u'Index rebuild completed successfully.'))
            for warning in warnings:
                messages.warning(request, warning)

        except Exception, e:
            if settings.DEBUG:
                raise
            messages.error(request, _(u'Index rebuild error: %s') % e)

        return HttpResponseRedirect(next)


def document_index_list(request, document_id):
    """
    Show a list of indexes where the current document can be found
    """
    document = get_object_or_404(Document, pk=document_id)
    object_list = []

    queryset = document.indexinstancenode_set.all()
    try:
        # TODO: should be AND not OR
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW, PERMISSION_DOCUMENT_INDEXING_VIEW])
    except PermissionDenied:
        queryset = AccessEntry.objects.filter_objects_by_access(PERMISSION_DOCUMENT_INDEXING_VIEW, request.user, queryset)

    for index_instance in queryset:
        object_list.append(get_breadcrumbs(index_instance, single_link=True, include_count=True))

    return render_to_response('generic_list.html', {
        'title': _(u'indexes containing: %s') % document,
        'object_list': object_list,
        'hide_link': True,
        'object': document
    }, context_instance=RequestContext(request))
