from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext

from common.utils import generate_choices_w_labels, encapsulate
from common.widgets import two_state_template

from documents.models import Document
from documents.views import document_list

from permissions.api import check_permissions

from grouping.models import DocumentGroup
from grouping.conf.settings import SHOW_EMPTY_GROUPS
from grouping.forms import DocumentDataGroupForm, DocumentGroupForm
from grouping import document_group_link
from grouping import PERMISSION_SMART_LINK_VIEW, \
    PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_DELETE


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
        title=_(u'documents in smart link: %(group)s') % {
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
            messages.warning(request, _(u'Smart link query error: %s' % error))

    if not SHOW_EMPTY_GROUPS:
        #If GROUP_SHOW_EMPTY is False, remove empty groups from
        #dictionary
        document_groups = dict([(group, data) for group, data in document_groups.items() if data['documents']])

    if document_groups:
        subtemplates_list = [{
            'name': 'generic_form_subtemplate.html',
            'context': {
                'title': _(u'smart links (%s)') % len(document_groups.keys()),
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
                'content': _(u'There no defined smart links for the current document.'),
            }
        }]

    return render_to_response('generic_detail.html', {
        'object': document,
        'document': document,
        'subtemplates_list': subtemplates_list,
    }, context_instance=RequestContext(request))
    
    
def document_group_list(request):
    check_permissions(request.user, [PERMISSION_SMART_LINK_VIEW])
    
    return render_to_response('generic_list.html', {
        'title': _(u'smart links'),
        'object_list': DocumentGroup.objects.all(),
        'extra_columns': [
            {'name': _(u'dynamic title'), 'attribute': 'dynamic_title'},
            {'name': _(u'enabled'), 'attribute': encapsulate(lambda x: two_state_template(x.enabled))},
        ],        
        'hide_link': True,
        }, context_instance=RequestContext(request))
        
        
def document_group_create(request):
    check_permissions(request.user, [PERMISSION_SMART_LINK_CREATE])

    if request.method == 'POST':
        form = DocumentGroupForm(request.POST)
        if form.is_valid():
            document_group = form.save()
            messages.success(request, _(u'Smart link: %s created successfully.') % document_group)
            return HttpResponseRedirect(reverse('document_group_list'))
    else:
        form = DocumentGroupForm()

    return render_to_response('generic_form.html', {
        'form': form,
        'title': _(u'Create new smart link')
    }, context_instance=RequestContext(request))    
    
    
def document_group_delete(request, document_group_id):
    check_permissions(request.user, [PERMISSION_SMART_LINK_DELETE])
    
    document_group = get_object_or_404(DocumentGroup, pk=document_group_id)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', '/')))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            document_group.delete()
            messages.success(request, _(u'Smart link: %s deleted successfully.') % document_group)
        except Exception, error:
            messages.error(request, _(u'Error deleting smart link: %(document_group)s; %(error)s.') % {
                'document_group': document_group,
                'error': error
            })
        return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'delete_view': True,
        'object': document_group,
        'next': next,
        'previous': previous,
        'form_icon': u'link_delete.png',
        #'temporary_navigation_links': {'form_header': {'staging_file_delete': {'links': results['tab_links']}}},
    }, context_instance=RequestContext(request))    
       
