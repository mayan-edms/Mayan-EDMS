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

from .models import Workflow, State, WorkflowState, WorkflowNode
from .forms import (WorkflowSetupForm, StateSetupForm, 
    WorkflowStateSetupForm, WorkflowNodeSetupForm)
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
        'extra_columns': [
            {'name': _(u'Initial state'), 'attribute': encapsulate(lambda workflow: workflow.initial_state or _(u'None'))},
        ],
        'list_object_variable_name': 'workflow',
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def setup_workflow_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_CREATE])
    redirect_url = reverse('setup_workflow_list')

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
        'workflow': workflow,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
        ],
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
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'chart_organisation_delete.png',
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
        ],
    }
    if len(workflows) == 1:
        context['workflow'] = workflows[0]
        context['title'] = _(u'Are you sure you wish to delete the workflow: %s?') % ', '.join([unicode(d) for d in workflows])
        context['message'] = _('Will be removed from all documents.')
    elif len(workflows) > 1:
        context['title'] = _(u'Are you sure you wish to delete the workflows: %s?') % ', '.join([unicode(d) for d in workflows])
        context['message'] = _('Will be removed from all documents.')

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))    


def setup_workflow_states_list(request, workflow_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    workflow = get_object_or_404(Workflow, pk=workflow_pk)

    context = {
        'object_list': workflow.workflowstate_set.all(),
        'title': _(u'states for workflow: %s') % workflow,
        'hide_link': True,
        'workflow': workflow,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
        ],
        'list_object_variable_name': 'workflow_state',
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def setup_workflow_state_add(request, workflow_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    redirect_url = reverse('setup_workflow_states_list', args=[workflow_pk])
    workflow = get_object_or_404(Workflow, pk=workflow_pk)

    if request.method == 'POST':
        form = WorkflowStateSetupForm(workflow=workflow, data=request.POST)
        if form.is_valid():
            state = form.save()
            messages.success(request, _(u'worflow state created succesfully.'))
            return HttpResponseRedirect(redirect_url)
    else:
        form = WorkflowStateSetupForm(workflow=workflow)

    return render_to_response('generic_form.html', {
        'title': _(u'add worflow state'),
        'form': form,
        'workflow': workflow,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
        ],
    }, context_instance=RequestContext(request))


def setup_workflow_state_edit(request, workflow_state_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    workflow_state = get_object_or_404(WorkflowState, pk=workflow_state_pk)
    redirect_url = reverse('setup_workflow_states_list', args=[workflow_state.workflow.pk])

    if request.method == 'POST':
        form = WorkflowStateSetupForm(workflow=workflow_state.workflow, instance=workflow_state, data=request.POST)
        if form.is_valid():
            state = form.save()
            messages.success(request, _(u'worflow state edited succesfully.'))
            return HttpResponseRedirect(redirect_url)
    else:
        form = WorkflowStateSetupForm(workflow=workflow_state.workflow, instance=workflow_state)

    return render_to_response('generic_form.html', {
        'title': _(u'edit worflow state: %s') % workflow_state,
        'form': form,
        'workflow': workflow_state.workflow,
        'workflow_state': workflow_state,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
            {'object': 'workflow_state', 'name': _(u'workflow state')}
        ],
    }, context_instance=RequestContext(request))
    

def setup_workflow_state_remove(request, workflow_state_pk=None, workflow_state_pk_list=None):
    post_action_redirect = None

    if workflow_state_pk:
        workflow_states = [get_object_or_404(WorkflowState, pk=workflow_state_pk)]
        post_action_redirect = reverse('setup_workflow_states_list', args=[workflow_states[0].workflow.pk])
    elif workflow_state_pk_list:
        workflow_states = [get_object_or_404(WorkflowState, pk=workflow_state_pk) for workflow_state_pk in workflow_state_pk_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one workflow state.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    except PermissionDenied:
        workflow_states = AccessEntry.objects.filter_objects_by_access(PERMISSION_WORKFLOW_SETUP_EDIT, request.user, workflow_states)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for workflow_state in workflow_states:
            try:
                workflow_state.delete()
                messages.success(request, _(u'Workflow states "%s" removed successfully.') % workflow_state)
            except Exception, e:
                messages.error(request, _(u'Error removing workflow state "%(workflow_state)s": %(error)s') % {
                    'workflow_state': workflow_state, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'workflow state'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'transmit_delete.png',
        'workflow': workflow_states[0].workflow,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
            {'object': 'workflow_state', 'name': _(u'workflow state')}
        ],        
    }
    if len(workflow_states) == 1:
        context['title'] = _(u'Are you sure you wish to remove the workflow state: %s?') % ', '.join([unicode(d) for d in workflow_states])
        context['workflow_state'] = workflow_states[0]
    elif len(states) > 1:
        context['title'] = _(u'Are you sure you wish to remove the workflow states: %s?') % ', '.join([unicode(d) for d in workflow_states])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))    


# Nodes
def setup_workflow_node_list(request, workflow_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    workflow = get_object_or_404(Workflow, pk=workflow_pk)

    context = {
        'object_list': workflow.workflow_nodes.all(),
        'extra_columns': [
            {'name': _(u'Posible next nodes'), 'attribute': encapsulate(lambda workflow_node: workflow_node.node.possible_next_nodes() or _(u'None'))},
        ],        
        'title': _(u'nodes of workflow: %s') % workflow,
        'hide_link': True,
        'workflow': workflow,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
        ],
        'list_object_variable_name': 'workflow_node',
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def setup_workflow_node_edit(request, workflow_node_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    workflow_node = get_object_or_404(WorkflowNode, pk=workflow_node_pk)
    redirect_url = reverse('setup_workflow_node_list', args=[workflow_node.workflow.pk])

    if request.method == 'POST':
        form = WorkflowNodeSetupForm(workflow=workflow_node.workflow, instance=workflow_node, data=request.POST)
        if form.is_valid():
            state = form.save()
            messages.success(request, _(u'worflow node edited succesfully.'))
            return HttpResponseRedirect(redirect_url)
    else:
        form = WorkflowNodeSetupForm(workflow=workflow_node.workflow, instance=workflow_node)

    return render_to_response('generic_form.html', {
        'title': _(u'edit worflow node: %s') % workflow_node,
        'form': form,
        'workflow': workflow_node.workflow,
        'workflow_node': workflow_node,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
            {'object': 'workflow_node', 'name': _(u'workflow node')}
        ],
    }, context_instance=RequestContext(request))
"""
def setup_workflow_transition_list(request, state_workflow_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    workflow = get_object_or_404(Workflow, pk=workflow_pk)

    context = {
        'object_list': workflow.workflowstate_set.all(),
        'title': _(u'states for workflow: %s') % workflow,
        'hide_link': True,
        'workflow': workflow,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
        ],
        'list_object_variable_name': 'workflow_state',
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
"""
# States
def setup_state_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])

    context = {
        'object_list': State.objects.all(),
        'title': _(u'states'),
        'hide_link': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def setup_state_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    redirect_url = reverse('setup_state_list')

    if request.method == 'POST':
        form = StateSetupForm(request.POST)
        if form.is_valid():
            state = form.save()
            messages.success(request, _(u'State created succesfully.'))
            return HttpResponseRedirect(redirect_url)
    else:
        form = StateSetupForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create state'),
        'form': form,
    },
    context_instance=RequestContext(request))


def setup_state_edit(request, state_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    state = get_object_or_404(State, pk=state_pk)

    if request.method == 'POST':
        form = StateSetupForm(instance=state, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'State "%s" updated successfully.') % state)
            return HttpResponseRedirect(reverse('setup_state_list'))
    else:
        form = StateSetupForm(instance=state)

    return render_to_response('generic_form.html', {
        'title': _(u'edit state: %s') % state,
        'form': form,
        'object': state,
        'object_name': _(u'state'),
    },
    context_instance=RequestContext(request))
    
    
def setup_state_delete(request, state_pk=None, state_pk_list=None):
    post_action_redirect = None

    if state_pk:
        states = [get_object_or_404(State, pk=state_pk)]
        post_action_redirect = reverse('setup_state_list')
    elif state_pk_list:
        states = [get_object_or_404(State, pk=state_pk) for state_pk in state_pk_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one state.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    except PermissionDenied:
        states = AccessEntry.objects.filter_objects_by_access(PERMISSION_WORKFLOW_SETUP_EDIT, request.user, states)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for state in states:
            try:
                state.delete()
                messages.success(request, _(u'States "%s" deleted successfully.') % state)
            except Exception, e:
                messages.error(request, _(u'Error deleting state "%(state)s": %(error)s') % {
                    'state': state, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'state'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'transmit_delete.png',
    }
    if len(states) == 1:
        context['object'] = states[0]
        context['title'] = _(u'Are you sure you wish to delete the state: %s?') % ', '.join([unicode(d) for d in states])
        context['message'] = _('Will be removed from all documents.')
    elif len(states) > 1:
        context['title'] = _(u'Are you sure you wish to delete the states: %s?') % ', '.join([unicode(d) for d in states])
        context['message'] = _('Will be removed from all documents.')

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))

"""
# Transitions
def setup_transition_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_TRANSITION_SETUP_VIEW])

    context = {
        'object_list': Transition.objects.all(),
        'title': _(u'transitions'),
        'hide_link': True,
        'list_object_variable_name': 'transition',
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def setup_transition_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_TRANSITION_SETUP_CREATE])
    redirect_url = reverse('setup_transition_list')

    if request.method == 'POST':
        form = TransitionSetupForm(request.POST)
        if form.is_valid():
            transition = form.save()
            messages.success(request, _(u'Transition created succesfully.'))
            return HttpResponseRedirect(redirect_url)
    else:
        form = TransitionSetupForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create transition'),
        'form': form,
    },
    context_instance=RequestContext(request))


def setup_transition_edit(request, transition_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_TRANSITION_SETUP_EDIT])
    transition = get_object_or_404(Transition, pk=transition_pk)

    if request.method == 'POST':
        form = TransitionSetupForm(instance=transition, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Transition "%s" updated successfully.') % transition)
            return HttpResponseRedirect(reverse('setup_transition_list'))
    else:
        form = TransitionSetupForm(instance=transition)

    return render_to_response('generic_form.html', {
        'title': _(u'edit transition: %s') % transition,
        'form': form,
        'transition': transition,
        'navigation_object_list': [
            {'object': 'transition', 'name': _(u'transition')},
        ],
    },
    context_instance=RequestContext(request))


def setup_transition_delete(request, transition_pk=None, transition_pk_list=None):
    post_action_redirect = None

    if transition_pk:
        transitions = [get_object_or_404(Transition, pk=transition_pk)]
        post_action_redirect = reverse('setup_transition_list')
    elif transition_pk_list:
        transitions = [get_object_or_404(Transition, pk=transition_pk) for transition_pk in transition_pk_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one transition.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TRANSITION_SETUP_DELETE])
    except PermissionDenied:
        transitions = AccessEntry.objects.filter_objects_by_access(PERMISSION_TRANSITION_SETUP_DELETE, request.user, transitions)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for transition in transitions:
            try:
                transition.delete()
                messages.success(request, _(u'Transitions "%s" deleted successfully.') % transition)
            except Exception, e:
                messages.error(request, _(u'Error deleting transition "%(transition)s": %(error)s') % {
                    'transition': transition, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'transition'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'transmit_delete.png',
        'navigation_object_list': [
            {'object': 'transition', 'name': _(u'transition')},
        ],        
    }
    if len(transitions) == 1:
        context['transition'] = transitions[0]
        context['title'] = _(u'Are you sure you wish to delete the transition: %s?') % ', '.join([unicode(d) for d in transitions])
        context['message'] = _('Will be removed from all documents.')
    elif len(transitions) > 1:
        context['title'] = _(u'Are you sure you wish to delete the transitions: %s?') % ', '.join([unicode(d) for d in transitions])
        context['message'] = _('Will be removed from all documents.')

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))
"""
"""
# State transitions
def setup_workflow_state_transitions_list(request, workflow_state_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    workflow_state = get_object_or_404(WorkflowState, pk=workflow_state_pk)

    context = {
        'object_list': workflow_state.transitions.all(),
        'title': _(u'transitions for workflow state: %s') % workflow_state,
        'hide_link': True,
        'workflow_state': workflow_state,
        'workflow': workflow_state.workflow,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
            {'object': 'workflow_state', 'name': _(u'state')},
        ],
        'list_object_variable_name': 'state_transition',
        'extra_columns': [
            {'name': _(u'Destination'), 'attribute': 'workflow_state_destination'},
        ],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def setup_workflow_state_transition_add(request, workflow_state_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    workflow_state = get_object_or_404(WorkflowState, pk=workflow_state_pk)
    redirect_url = reverse('setup_workflow_state_transitions_list', args=[workflow_state_pk])

    if request.method == 'POST':
        form = WorkflowStateTransitionSetupForm(workflow_state=workflow_state, data=request.POST)
        if form.is_valid():
            workflow_state_transition = form.save()
            messages.success(request, _(u'worflow state transition created succesfully.'))
            return HttpResponseRedirect(redirect_url)
    else:
        form = WorkflowStateTransitionSetupForm(workflow_state=workflow_state)

    return render_to_response('generic_form.html', {
        'title': _(u'add transition to worflow state: %s') % workflow_state,
        'form': form,
        'workflow_state': workflow_state,
        'workflow': workflow_state.workflow,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
            {'object': 'workflow_state', 'name': _(u'state')},
        ],
    }, context_instance=RequestContext(request))


def setup_workflow_state_transition_edit(request, work_state_transition_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_SETUP_EDIT])
    workflow_state_transition = get_object_or_404(WorkflowStateTransition, pk=work_state_transition_pk)
    redirect_url = reverse('setup_workflow_state_transitions_list', args=[workflow_state_transition.workflow_state_source.pk])

    if request.method == 'POST':
        form = WorkflowStateTransitionSetupForm(workflow_state=workflow_state_transition.workflow_state_source, instance=workflow_state_transition, data=request.POST)
        if form.is_valid():
            workflow_state_transition = form.save()
            messages.success(request, _(u'worflow state transition edited succesfully.'))
            return HttpResponseRedirect(redirect_url)
    else:
        form = WorkflowStateSetupForm(workflow_state=workflow_state_transition.workflow_state_source, instance=workflow_state_transition)

    return render_to_response('generic_form.html', {
        'title': _(u'edit worflow state transition: %s') % workflow_state_transition,
        'form': form,
        'workflow_state': workflow_state_transition.workflow_state_source,
        'workflow': workflow_state_transition.workflow_state_source.workflow,
        'workflow_state_transition': workflow_state_transition,
        'navigation_object_list': [
            {'object': 'workflow', 'name': _(u'workflow')},
            {'object': 'workflow_state', 'name': _(u'state')},
            {'object': 'workflow_state_transition', 'name': _(u'transition')},
        ],
        'list_object_variable_name': 'workflow_state_transition',
    }, context_instance=RequestContext(request))
"""    
"""
def setup_state_transition_remove(request, state_transition_pk=None, state_transition_pk_list=None):
    post_action_redirect = None

    if state_transition_pk:
        state_transitions = [get_object_or_404(WorkflowState, pk=state_transition_pk)]
        post_action_redirect = reverse('setup_state_transitions_list', args=[state_transitions[0].state.pk])
    elif state_transition_pk_list:
        state_transitions = [get_object_or_404(WorkflowState, pk=state_transition_pk) for state_transition_pk in state_transition_pk_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one state state.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_STATE_SETUP_DELETE])
    except PermissionDenied:
        state_transitions = AccessEntry.objects.filter_objects_by_access(PERMISSION_STATE_SETUP_DELETE, request.user, state_transitions)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for state_transition in state_transitions:
            try:
                state_transition.delete()
                messages.success(request, _(u'Workflow states "%s" removed successfully.') % state_transition)
            except Exception, e:
                messages.error(request, _(u'Error removing state state "%(state_transition)s": %(error)s') % {
                    'state_transition': state_transition, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'state state'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'transmit_delete.png',
        'state': state_transitions[0].state,
        'navigation_object_list': [
            {'object': 'state', 'name': _(u'state')},
            {'object': 'state_transition', 'name': _(u'state state')}
        ],        
    }
    if len(state_transitions) == 1:
        context['title'] = _(u'Are you sure you wish to remove the state state: %s?') % ', '.join([unicode(d) for d in state_transitions])
        context['state_transition'] = state_transitions[0]
    elif len(states) > 1:
        context['title'] = _(u'Are you sure you wish to remove the state states: %s?') % ', '.join([unicode(d) for d in state_transitions])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))    
"""
