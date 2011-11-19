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

from grouping.models import DocumentGroup, DocumentGroupItem
from grouping.conf.settings import SHOW_EMPTY_GROUPS
from grouping.forms import (SmartLinkInstanceForm, SmartLinkForm,
    SmartLinkConditionForm)
from grouping import smart_link_instance_view_link
from grouping import (PERMISSION_SMART_LINK_VIEW,
    PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_DELETE,
    PERMISSION_SMART_LINK_EDIT)


def smart_link_action(request):
    check_permissions(request.user, [PERMISSION_SMART_LINK_VIEW])
    
    action = request.GET.get('action', None)

    if not action:
        messages.error(request, _(u'No action selected.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', u'/'))

    return HttpResponseRedirect(action)


def smart_link_instance_view(request, document_id, smart_link_pk):
    check_permissions(request.user, [PERMISSION_SMART_LINK_VIEW])

    document = get_object_or_404(Document, pk=document_id)
    smart_link = get_object_or_404(DocumentGroup, pk=smart_link_pk)
    object_list, errors = DocumentGroup.objects.get_groups_for(document, smart_link)

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


def smart_link_instances_for_document(request, document_id):
    check_permissions(request.user, [PERMISSION_SMART_LINK_VIEW])

    subtemplates_list = []
    document = get_object_or_404(Document, pk=document_id)
    smart_links, errors = DocumentGroup.objects.get_groups_for(document)
    if (request.user.is_staff or request.user.is_superuser) and errors:
        for error in errors:
            messages.warning(request, _(u'Smart link query error: %s' % error))

    if not SHOW_EMPTY_GROUPS:
        #If GROUP_SHOW_EMPTY is False, remove empty groups from
        #dictionary
        document_groups = dict([(group, data) for group, data in document_groups.items() if data['documents']])

    if smart_links:
        subtemplates_list = [{
            'name': 'generic_form_subtemplate.html',
            'context': {
                'title': _(u'smart links (%s)') % len(smart_links.keys()),
                'form': SmartLinkInstanceForm(
                    groups=smart_links, current_document=document,
                    links=[smart_link_instance_view_link]
                ),
                'form_action': reverse('smart_link_action'),
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
    check_permissions(request.user, [PERMISSION_SMART_LINK_CREATE])
    
    return render_to_response('generic_list.html', {
        'title': _(u'smart links'),
        'object_list': DocumentGroup.objects.all(),
        'extra_columns': [
            {'name': _(u'dynamic title'), 'attribute': 'dynamic_title'},
            {'name': _(u'enabled'), 'attribute': encapsulate(lambda x: two_state_template(x.enabled))},
        ],        
        'hide_link': True,
        'list_object_variable_name': 'smart_link',

        }, context_instance=RequestContext(request))
        
        
def document_group_create(request):
    check_permissions(request.user, [PERMISSION_SMART_LINK_CREATE])

    if request.method == 'POST':
        form = SmartLinkForm(request.POST)
        if form.is_valid():
            document_group = form.save()
            messages.success(request, _(u'Smart link: %s created successfully.') % document_group)
            return HttpResponseRedirect(reverse('document_group_list'))
    else:
        form = SmartLinkForm()

    return render_to_response('generic_form.html', {
        'form': form,
        'title': _(u'Create new smart link')
    }, context_instance=RequestContext(request))    
    
    
def document_group_edit(request, smart_link_pk):
    check_permissions(request.user, [PERMISSION_SMART_LINK_EDIT])
    
    smart_link = get_object_or_404(DocumentGroup, pk=smart_link_pk)

    if request.method == 'POST':
        form = SmartLinkForm(request.POST, instance=smart_link)
        if form.is_valid():
            smart_link = form.save()
            messages.success(request, _(u'Smart link: %s edited successfully.') % smart_link)
            return HttpResponseRedirect(reverse('document_group_list'))
    else:
        form = SmartLinkForm(instance=smart_link)

    return render_to_response('generic_form.html', {
        'navigation_object_name': 'smart_link',
        'smart_link': smart_link,
        'form': form,
        'title': _(u'Edit smart link: %s') % smart_link
    }, context_instance=RequestContext(request))    
        
    
def document_group_delete(request, smart_link_pk):
    check_permissions(request.user, [PERMISSION_SMART_LINK_DELETE])
    
    smart_link = get_object_or_404(DocumentGroup, pk=smart_link_pk)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', '/')))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            smart_link.delete()
            messages.success(request, _(u'Smart link: %s deleted successfully.') % smart_link)
        except Exception, error:
            messages.error(request, _(u'Error deleting smart link: %(smart_link)s; %(error)s.') % {
                'smart_link': smart_link,
                'error': error
            })
        return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'delete_view': True,
        'navigation_object_name': 'smart_link',
        'smart_link': smart_link,
        'title': _(u'Are you sure you wish to delete smart link: %s?') % smart_link,
        'next': next,
        'previous': previous,
        'form_icon': u'link_delete.png',
    }, context_instance=RequestContext(request))    
       

def smart_link_condition_list(request, smart_link_pk):
    check_permissions(request.user, [PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT])
    
    smart_link = get_object_or_404(DocumentGroup, pk=smart_link_pk)
    
    return render_to_response('generic_list.html', {
        'title': _(u'conditions for smart link: %s') % smart_link,
        'object_list': smart_link.documentgroupitem_set.all(),
        'extra_columns': [
            {'name': _(u'enabled'), 'attribute': encapsulate(lambda x: two_state_template(x.enabled))},
        ],        
        'hide_link': True,
        'smart_link': smart_link,
        'navigation_object_name': 'smart_link',
        'list_object_variable_name': 'condition',        
        }, context_instance=RequestContext(request))


def smart_link_condition_create(request, smart_link_pk):
    check_permissions(request.user, [PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT])

    smart_link = get_object_or_404(DocumentGroup, pk=smart_link_pk)

    if request.method == 'POST':
        form = SmartLinkConditionForm(request.POST, initial={'document_group': smart_link})
        if form.is_valid():
            smart_link_condition = form.save()
            messages.success(request, _(u'Smart link condition: "%s" created successfully.') % smart_link_condition)
            return HttpResponseRedirect(reverse('smart_link_condition_list', args=[smart_link.pk]))
    else:
        form = SmartLinkConditionForm(initial={'document_group': smart_link})

    return render_to_response('generic_form.html', {
        'form': form,
        'title': _(u'Add new conditions to smart link: "%s"') % smart_link,
        'navigation_object_name': 'smart_link',
        'smart_link': smart_link,        
    }, context_instance=RequestContext(request))    


def smart_link_condition_edit(request, smart_link_condition_pk):
    check_permissions(request.user, [PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT])

    smart_link_condition = get_object_or_404(DocumentGroupItem, pk=smart_link_condition_pk)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', '/')))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = SmartLinkConditionForm(request.POST, instance=smart_link_condition)
        if form.is_valid():
            smart_link_condition = form.save()
            messages.success(request, _(u'Smart link condition: "%s" created successfully.') % smart_link_condition)
            return HttpResponseRedirect(next)
    else:
        form = SmartLinkConditionForm(instance=smart_link_condition)

    return render_to_response('generic_form.html', {
        'form': form,
        'title': _(u'Edit smart link condition'),
        'next': next,
        'previous': previous,
        'condition': smart_link_condition,
        'smart_link': smart_link_condition.document_group,
        'navigation_object_list': [
            {'object': 'smart_link', 'name': _(u'smart link')},
            {'object': 'condition', 'name': _(u'condition')}
        ],
        
    }, context_instance=RequestContext(request))    


def smart_link_condition_delete(request, smart_link_condition_pk):
    check_permissions(request.user, [PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT])

    smart_link_condition = get_object_or_404(DocumentGroupItem, pk=smart_link_condition_pk)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', '/')))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            smart_link_condition.delete()
            messages.success(request, _(u'Smart link condition: "%s" deleted successfully.') % smart_link_condition)
        except Exception, error:
            messages.error(request, _(u'Error deleting smart link condition: %(smart_link_condition)s; %(error)s.') % {
                'smart_link_condition': smart_link_condition,
                'error': error
            })
        return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'delete_view': True,
        'condition': smart_link_condition,
        'smart_link': smart_link_condition.document_group,
        'navigation_object_list': [
            {'object': 'smart_link', 'name': _(u'smart link')},
            {'object': 'condition', 'name': _(u'condition')}
        ],
        'title': _(u'Are you sure you wish to delete smart link condition: "%s"?') % smart_link_condition,
        'next': next,
        'previous': previous,
        'form_icon': u'cog_delete.png',
    }, context_instance=RequestContext(request))    
