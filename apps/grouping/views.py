from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext

from documents.models import Document
from documents.views import document_list

from grouping.models import DocumentGroup
from grouping.conf.settings import SHOW_EMPTY_GROUPS
from grouping.forms import DocumentDataGroupForm
from grouping import document_group_link


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


def groups_for_document(request, document_id):
    subtemplates_list = []
    document = get_object_or_404(Document, pk=document_id)
    document_groups, errors = DocumentGroup.objects.get_groups_for(document)
    if (request.user.is_staff or request.user.is_superuser) and errors:
        for error in errors:
            messages.warning(request, _(u'Document group query error: %s' % error))

    if not SHOW_EMPTY_GROUPS:
        #If GROUP_SHOW_EMPTY is False, remove empty groups from
        #dictionary
        document_groups = dict([(group, data) for group, data in document_groups.items() if data['documents']])

    if document_groups:
        subtemplates_list = [{
            'name': 'generic_form_subtemplate.html',
            'context': {
                'title': _(u'document groups (%s)') % len(document_groups.keys()),
                'form': DocumentDataGroupForm(
                    groups=document_groups, current_document=document,
                    links=[document_group_link]
                ),
                'form_action': reverse('document_group_action'),
                'submit_method': 'GET',
            }
        }]
    else:
        # If there are not group display a placeholder messages saying so
        subtemplates_list = [{
            'name': 'generic_subtemplate.html',
            'context': {
                'content': _(u'There no defined groups for the current document.'),
            }
        }]

    return render_to_response('generic_detail.html', {
        'object': document,
        'document': document,
        'subtemplates_list': subtemplates_list,
    }, context_instance=RequestContext(request))        
