from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from documents.models import Document
from documents.views import document_list

from grouping.models import DocumentGroup


def document_group_action(request):
    action = request.GET.get('action', None)

    if not action:
        messages.error(request, _(u'No action selected.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', u'/'))

    return HttpResponseRedirect(action)


def document_group_view(request, document_id, document_group_id):
    document = get_object_or_404(Document, pk=document_id)
    document_group = get_object_or_404(DocumentGroup, pk=document_group_id)
    object_list, errors = DocumentGroup.objects.get_groups_for(document, document_group)

    return document_list(
        request,
        title=_(u'documents in group: %(group)s') % {
            'group': object_list['title']
        },
        object_list=object_list['documents'],
        extra_context={
            'object': document
        }
    )
