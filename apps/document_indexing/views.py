from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.utils.safestring import mark_safe

from permissions.api import check_permissions
from documents.literals import PERMISSION_DOCUMENT_VIEW
from documents.models import Document
from documents.views import document_list
from common.utils import encapsulate

from document_indexing import PERMISSION_DOCUMENT_INDEXING_VIEW, \
    PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES

from document_indexing.models import IndexInstance
from document_indexing.api import get_breadcrumbs, get_instance_link, \
    do_rebuild_all_indexes
from document_indexing.widgets import index_instance_item_link


def index_instance_list(request, index_id=None):
    check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_VIEW])

    if index_id:
        index_instance = get_object_or_404(IndexInstance, pk=index_id)
        index_instance_list = [index for index in index_instance.get_children().order_by('value')]
        breadcrumbs = get_breadcrumbs(index_instance)
        if index_instance.documents.count():
            for document in index_instance.documents.all().order_by('file_filename'):
                index_instance_list.append(document)
    else:
        index_instance_list = IndexInstance.objects.filter(parent=None)
        breadcrumbs = get_instance_link()
        index_instance = None

    title = mark_safe(_(u'contents for index: %s') % breadcrumbs)

    if index_instance:
        if index_instance.index.link_documents:
            # Document list, use the document_list view for consistency
            return document_list(
                request,
                title=title,
                object_list=index_instance_list,
                extra_context={
                    'object': index_instance
                }
            )

    return render_to_response('generic_list.html', {
        'object_list': index_instance_list,
        'extra_columns_preffixed': [
            {
                'name': _(u'index'),
                'attribute': encapsulate(lambda x: index_instance_item_link(x))
            },
            {
                'name': _(u'items'),
                'attribute': encapsulate(lambda x: x.documents.count() if x.index.link_documents else x.get_children().count() )
            }
        ],
        'title': title,
        'hide_links': True,
        'hide_object': True,
        'object': index_instance

    }, context_instance=RequestContext(request))


def rebuild_index_instances(request):
    check_permissions(request.user, [PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES])

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
            messages.error(request, _(u'Index rebuild error: %s') % e)

        return HttpResponseRedirect(next)


def document_index_list(request, document_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW, PERMISSION_DOCUMENT_INDEXING_VIEW])
    document = get_object_or_404(Document, pk=document_id)

    object_list = []

    for index_instance in document.indexinstance_set.all():
        object_list.append(get_breadcrumbs(index_instance, single_link=True, include_count=True))

    return render_to_response('generic_list.html', {
        'title': _(u'indexes containing: %s') % document,
        'object_list': object_list,
        'hide_link': True,
        'object': document
    }, context_instance=RequestContext(request))
