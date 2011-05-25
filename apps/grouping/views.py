from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from documents.literals import PERMISSION_DOCUMENT_VIEW
from documents.models import Document
from permissions.api import check_permissions

from grouping.models import DocumentGroup


def document_group_action(request):
    action = request.GET.get('action', None)

    if not action:
        messages.error(request, _(u'No action selected.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', u'/'))

    return HttpResponseRedirect(action)


def document_group_view(request, document_id, document_group_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    document = get_object_or_404(Document, pk=document_id)
    document_group = get_object_or_404(DocumentGroup, pk=document_group_id)
    object_list, errors = DocumentGroup.objects.get_groups_for(document, document_group)

    return render_to_response('generic_list.html', {
        'object_list': object_list['documents'],
        'title': _(u'documents in group: %(group)s') % {
            'group': object_list['title']
        },
        'multi_select_as_buttons': True,
        'hide_links': True,
        'ref_object': document
    }, context_instance=RequestContext(request))
