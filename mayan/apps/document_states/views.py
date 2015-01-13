from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _, ungettext

from acls.models import AccessEntry
from common.views import (SingleObjectCreateView, SingleObjectDeleteView,
                          SingleObjectEditView, SingleObjectListView)
from permissions.models import Permission

from .forms import WorkflowStateForm, WorkflowTransitionForm
from .models import Workflow
from .permissions import PERMISSION_WORKFLOW_CREATE, PERMISSION_WORKFLOW_DELETE, PERMISSION_WORKFLOW_EDIT, PERMISSION_WORKFLOW_VIEW


class SetupWorkflowListView(SingleObjectListView):
    extra_context = {
        'title': _('Workflows'),
        'hide_link': True,
    }
    model = Workflow
    view_permission = PERMISSION_WORKFLOW_VIEW


class SetupWorkflowCreateView(SingleObjectCreateView):
    model = Workflow
    view_permission = PERMISSION_WORKFLOW_CREATE
    success_url = reverse_lazy('document_states:setup_workflow_list')


class SetupWorkflowEditView(SingleObjectEditView):
    model = Workflow
    object_permission = PERMISSION_WORKFLOW_EDIT
    success_url = reverse_lazy('document_states:setup_workflow_list')


class SetupWorkflowDeleteView(SingleObjectDeleteView):
    model = Workflow
    object_permission = PERMISSION_WORKFLOW_DELETE
    success_url = reverse_lazy('document_states:setup_workflow_list')


# States

class SetupWorkflowStateListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_EDIT])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_WORKFLOW_EDIT, request.user, self.get_workflow())

        return super(SetupWorkflowStateListView, self).dispatch(request, *args, **kwargs)

    def get_workflow(self):
        return get_object_or_404(Workflow, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_workflow().states.all()

    def get_context_data(self, **kwargs):
        context = super(SetupWorkflowStateListView, self).get_context_data(**kwargs)
        context.update(
            {
                'hide_link': True,
                'object': self.get_workflow(),
                'title': _('States of workflow: %s') % self.get_workflow()
            }
        )

        return context


class SetupWorkflowStateCreateView(SingleObjectCreateView):
    form_class = WorkflowStateForm

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_EDIT])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_WORKFLOW_EDIT, request.user, self.get_workflow())

        return super(SetupWorkflowStateCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SetupWorkflowStateCreateView, self).get_context_data(**kwargs)
        context.update(
            {
                'object': self.get_workflow(),
                'title': _('Create states for workflow: %s') % self.get_workflow()
            }
        )
        return context

    def get_workflow(self):
        return get_object_or_404(Workflow, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_workflow().states.all()

    def get_success_url(self):
        return reverse('document_states:setup_workflow_states', args=[self.kwargs['pk']])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.workflow = self.get_workflow()
        self.object.save()
        return super(SetupWorkflowStateCreateView, self).form_valid(form)


# Transitions

class SetupWorkflowTransitionListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_EDIT])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_WORKFLOW_EDIT, request.user, self.get_workflow())

        return super(SetupWorkflowTransitionListView, self).dispatch(request, *args, **kwargs)

    def get_workflow(self):
        return get_object_or_404(Workflow, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_workflow().transitions.all()

    def get_context_data(self, **kwargs):
        context = super(SetupWorkflowTransitionListView, self).get_context_data(**kwargs)
        context.update(
            {
                'hide_link': True,
                'object': self.get_workflow(),
                'title': _('Transitions of workflow: %s') % self.get_workflow()
            }
        )

        return context


class SetupWorkflowTransitionCreateView(SingleObjectCreateView):
    form_class = WorkflowTransitionForm

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_EDIT])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_WORKFLOW_EDIT, request.user, self.get_workflow())

        return super(SetupWorkflowTransitionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SetupWorkflowTransitionCreateView, self).get_context_data(**kwargs)
        context.update(
            {
                'object': self.get_workflow(),
                'title': _('Create transitions for workflow: %s') % self.get_workflow()
            }
        )
        return context

    def get_workflow(self):
        return get_object_or_404(Workflow, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_workflow().transitions.all()

    def get_success_url(self):
        return reverse('document_states:setup_workflow_transitions', args=[self.kwargs['pk']])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.workflow = self.get_workflow()
        try:
            self.object.save()
        except IntegrityError:
            messages.error(self.request, _('Unable to save transition; integrity error.'))
            return super(SetupWorkflowTransitionCreateView, self).form_invalid(form)
        else:
            return HttpResponseRedirect(self.get_success_url())
