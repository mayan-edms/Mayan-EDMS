from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from acls.models import AccessEntry
from common.utils import generate_choices_w_labels
from common.views import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectEditView,
    SingleObjectListView, assign_remove
)
from documents.models import Document
from permissions.models import Permission

from .forms import (
    WorkflowForm,
    WorkflowInstanceDetailForm, WorkflowInstanceTransitionForm,
    WorkflowStateForm, WorkflowTransitionForm
)
from .models import Workflow, WorkflowInstance, WorkflowState, WorkflowTransition
from .permissions import (
    PERMISSION_WORKFLOW_CREATE, PERMISSION_WORKFLOW_DELETE,
    PERMISSION_WORKFLOW_EDIT, PERMISSION_WORKFLOW_VIEW,
    PERMISSION_DOCUMENT_WORKFLOW_VIEW, PERMISSION_DOCUMENT_WORKFLOW_TRANSITION
)


class DocumentWorkflowInstanceListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_WORKFLOW_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_WORKFLOW_VIEW, request.user, self.get_document())

        return super(DocumentWorkflowInstanceListView, self).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_document().workflows.all()

    def get_context_data(self, **kwargs):
        context = super(DocumentWorkflowInstanceListView, self).get_context_data(**kwargs)
        context.update(
            {
                'hide_link': True,
                'object': self.get_document(),
                'title': _('Workflows for document: %s') % self.get_document(),
                'list_object_variable_name': 'workflow_instance',
            }
        )

        return context


class WorkflowInstanceDetailView(SingleObjectListView):
    template_name = 'main/generic_multi_subtemplates.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_WORKFLOW_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_WORKFLOW_VIEW, request.user, self.get_workflow_instance().document)

        return super(WorkflowInstanceDetailView, self).dispatch(request, *args, **kwargs)

    def get_workflow_instance(self):
        return get_object_or_404(WorkflowInstance, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_workflow_instance().log_entries.order_by('-datetime')

    def get_context_data(self, **kwargs):
        form = WorkflowInstanceDetailForm(
            instance=self.get_workflow_instance(), extra_fields=[
                {'label': _('Current state'), 'field': 'get_current_state'},
                {'label': _('Last transition'), 'field': 'get_last_transition'},
            ]
        )

        context = {
            'object': self.get_workflow_instance().document,
            'workflow_instance': self.get_workflow_instance(),
            'navigation_object_list': [
                {'object': 'object'},
                {'object': 'workflow_instance'}
            ],
            'title': _('Detail of workflow: %(workflow)s') % {
                'workflow': self.get_workflow_instance()
            },
            'subtemplates_list': [
                {
                    'name': 'main/generic_detail_subtemplate.html',
                    'context': {
                        'form': form,
                    }
                },
                {
                    'name': 'main/generic_list_subtemplate.html',
                    'context': {
                        'object_list': self.get_queryset(),
                        'title': _('Log entries'),
                        'hide_object': True,
                    }
                }
            ]
        }

        return context


class WorkflowInstanceTransitionView(FormView):
    form_class = WorkflowInstanceTransitionForm
    template_name = 'main/generic_form.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_WORKFLOW_TRANSITION])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_WORKFLOW_TRANSITION, request.user, self.get_workflow_instance().document)

        return super(WorkflowInstanceTransitionView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        transition = self.get_workflow_instance().workflow.transitions.get(pk=form.cleaned_data['transition'])
        self.get_workflow_instance().do_transition(comment=form.cleaned_data['comment'], transition=transition, user=self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(WorkflowInstanceTransitionView, self).get_form_kwargs()
        kwargs['workflow'] = self.get_workflow_instance()
        return kwargs

    def get_workflow_instance(self):
        return get_object_or_404(WorkflowInstance, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(WorkflowInstanceTransitionView, self).get_context_data(**kwargs)

        context.update(
            {
                'object': self.get_workflow_instance().document,
                'workflow_instance': self.get_workflow_instance(),
                'navigation_object_list': [
                    {'object': 'object'},
                    {'object': 'workflow_instance'}
                ],
                'title': _('Do transition for workflow: %s') % self.get_workflow_instance(),
                'submit_label': _('Submit'),
            }
        )

        return context

    def get_success_url(self):
        return self.get_workflow_instance().get_absolute_url()


# Setup

class SetupWorkflowListView(SingleObjectListView):
    extra_context = {
        'title': _('Workflows'),
        'hide_link': True,
    }
    model = Workflow
    view_permission = PERMISSION_WORKFLOW_VIEW


class SetupWorkflowCreateView(SingleObjectCreateView):
    form_class = WorkflowForm
    model = Workflow
    view_permission = PERMISSION_WORKFLOW_CREATE
    success_url = reverse_lazy('document_states:setup_workflow_list')


class SetupWorkflowEditView(SingleObjectEditView):
    form_class = WorkflowForm
    model = Workflow
    view_permission = PERMISSION_WORKFLOW_EDIT
    success_url = reverse_lazy('document_states:setup_workflow_list')


class SetupWorkflowDeleteView(SingleObjectDeleteView):
    model = Workflow
    view_permission = PERMISSION_WORKFLOW_DELETE
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


class SetupWorkflowStateDeleteView(SingleObjectDeleteView):
    model = WorkflowState
    view_permission = PERMISSION_WORKFLOW_DELETE

    def get_context_data(self, **kwargs):
        context = super(SetupWorkflowStateDeleteView, self).get_context_data(**kwargs)

        context.update(
            {
                'object': self.get_object().workflow,
                'workflow_instance': self.get_object(),
                'navigation_object_list': [
                    {'object': 'object'},
                    {'object': 'workflow_instance'}
                ],
            }
        )

        return context

    def get_success_url(self):
        return reverse('document_states:setup_workflow_States', args=[self.get_object().workflow.pk])


class SetupWorkflowStateEditView(SingleObjectEditView):
    form_class = WorkflowStateForm
    model = WorkflowState
    view_permission = PERMISSION_WORKFLOW_EDIT

    def get_context_data(self, **kwargs):
        context = super(SetupWorkflowStateEditView, self).get_context_data(**kwargs)

        context.update(
            {
                'object': self.get_object().workflow,
                'workflow_instance': self.get_object(),
                'navigation_object_list': [
                    {'object': 'object'},
                    {'object': 'workflow_instance'}
                ],
            }
        )

        return context

    def get_success_url(self):
        return reverse('document_states:setup_workflow_states', args=[self.get_object().workflow.pk])


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

    def get_form_kwargs(self):
        kwargs = super(SetupWorkflowTransitionCreateView, self).get_form_kwargs()
        kwargs['workflow'] = self.get_workflow()
        return kwargs

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


class SetupWorkflowTransitionDeleteView(SingleObjectDeleteView):
    model = WorkflowTransition
    view_permission = PERMISSION_WORKFLOW_DELETE

    def get_context_data(self, **kwargs):
        context = super(SetupWorkflowTransitionDeleteView, self).get_context_data(**kwargs)

        context.update(
            {
                'object': self.get_object().workflow,
                'workflow_instance': self.get_object(),
                'navigation_object_list': [
                    {'object': 'object'},
                    {'object': 'workflow_instance'}
                ],
            }
        )

        return context

    def get_success_url(self):
        return reverse('document_states:setup_workflow_transitions', args=[self.get_object().workflow.pk])


class SetupWorkflowTransitionEditView(SingleObjectEditView):
    form_class = WorkflowTransitionForm
    model = WorkflowTransition
    view_permission = PERMISSION_WORKFLOW_EDIT

    def get_context_data(self, **kwargs):
        context = super(SetupWorkflowTransitionEditView, self).get_context_data(**kwargs)

        context.update(
            {
                'object': self.get_object().workflow,
                'workflow_instance': self.get_object(),
                'navigation_object_list': [
                    {'object': 'object'},
                    {'object': 'workflow_instance'}
                ],
            }
        )

        return context

    def get_form_kwargs(self):
        kwargs = super(SetupWorkflowTransitionEditView, self).get_form_kwargs()
        kwargs['workflow'] = self.get_object().workflow
        return kwargs

    def get_success_url(self):
        return reverse('document_states:setup_workflow_transitions', args=[self.get_object().workflow.pk])


def setup_workflow_document_types(request, pk):
    workflow = get_object_or_404(Workflow, pk=pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_WORKFLOW_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_WORKFLOW_EDIT, request.user, workflow)

    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(workflow.get_document_types_not_in_workflow(), display_object_type=False),
        right_list=lambda: generate_choices_w_labels(workflow.document_types.all(), display_object_type=False),
        add_method=lambda x: workflow.document_types.add(x),
        remove_method=lambda x: workflow.document_types.remove(x),
        decode_content_type=True,
        extra_context={
            'main_title': _('Document types assigned the workflow: %s') % workflow,
            'object': workflow,
        }
    )
