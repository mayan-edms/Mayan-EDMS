from __future__ import absolute_import

import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.exceptions import PermissionDenied

from permissions.models import Permission
from common.utils import encapsulate
#from common.widgets import two_state_template
#from acls.models import AccessEntry

from .models import Workflow
from .forms import WorkflowSetupForm
from .permissions import (PERMISSION_WORKFLOW_SETUP_VIEW,
    PERMISSION_WORKFLOW_SETUP_CREATE, PERMISSION_WORKFLOW_SETUP_EDIT,
    PERMISSION_WORKFLOW_SETUP_DELETE)


logger = logging.getLogger(__name__)


# Setup views
def setup_workflow_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_VIEW])

    context = {
        'object_list': Workflow.objects.all(),
        'title': _(u'workflows'),
        'hide_link': True,
        #'list_object_variable_name': 'source',
        #'source_type': source_type,
        'extra_columns': [
            {'name': _(u'Initial state'), 'attribute': encapsulate(lambda workflow: workflow.initial_state or _(u'None'))},
        ],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def setup_workflow_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_CREATE])
    redirect_url = reverse('setup_workflow_list')
    #previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', redirect_url)))

    if request.method == 'POST':
        form = WorkflowSetupForm(request.POST)
        if form.is_valid():
            workflow = form.save()
            messages.success(request, _(u'Workflow created succesfully.'))
            return HttpResponseRedirect(redirect_url)
    else:
        form = WorkflowSetupForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create workflow'),
        'form': form,
    },
    context_instance=RequestContext(request))


def setup_workflow_edit(request, workflow_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    workflow = get_object_or_404(Workflow, pk=workflow_pk)

    if request.method == 'POST':
        form = WorkflowSetupForm(instance=workflow, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Workflow "%s" updated successfully.') % workflow)
            return HttpResponseRedirect(reverse('setup_workflow_list'))
    else:
        form = WorkflowSetupForm(instance=workflow)

    return render_to_response('generic_form.html', {
        'title': _(u'edit workflow: %s') % workflow,
        'form': form,
        'object': workflow,
        'object_name': _(u'workflow'),
    },
    context_instance=RequestContext(request))
    
    
def setup_workflow_delete(request, workflow_pk=None, workflow_pk_list=None):
    post_action_redirect = None

    if workflow_pk:
        workflows = [get_object_or_404(Workflow, pk=workflow_pk)]
        post_action_redirect = reverse('setup_workflow_list')
    elif workflow_pk_list:
        workflows = [get_object_or_404(Workflow, pk=workflow_pk) for workflow_pk in workflow_pk_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one workflow.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_DELETE])
    except PermissionDenied:
        workflows = AccessEntry.objects.filter_objects_by_access(PERMISSION_WORKFLOW_SETUP_DELETE, request.user, workflows)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for workflow in workflows:
            try:
                workflow.delete()
                messages.success(request, _(u'Workflows "%s" deleted successfully.') % workflow)
            except Exception, e:
                messages.error(request, _(u'Error deleting workflow "%(workflow)s": %(error)s') % {
                    'workflow': workflow, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'workflow'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'chart_organisation_delete.png',
    }
    if len(workflows) == 1:
        context['object'] = workflows[0]
        context['title'] = _(u'Are you sure you wish to delete the workflow: %s?') % ', '.join([unicode(d) for d in workflows])
        context['message'] = _('Will be removed from all documents.')
    elif len(workflows) > 1:
        context['title'] = _(u'Are you sure you wish to delete the workflows: %s?') % ', '.join([unicode(d) for d in workflows])
        context['message'] = _('Will be removed from all documents.')

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))    
