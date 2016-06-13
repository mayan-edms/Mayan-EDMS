from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from acls.models import AccessControlList
from common.views import (
    AssignRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)
from documents.models import Document
from documents.views import DocumentListView
from permissions import Permission

from .forms import (
    WorkflowForm, WorkflowInstanceTransitionForm, WorkflowStateForm,
    WorkflowTransitionForm
)
from .models import Workflow, WorkflowInstance, WorkflowState, WorkflowTransition
from .permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit, permission_workflow_transition,
    permission_workflow_view,
)


class DocumentWorkflowInstanceListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_workflow_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_workflow_view, request.user,
                self.get_document()
            )

        return super(
            DocumentWorkflowInstanceListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(Document.on_organization, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object': self.get_document(),
            'title': _(
                'Workflows for document: %s'
            ) % self.get_document(),
        }

    def get_queryset(self):
        return self.get_document().workflows.all()


class WorkflowDocumentListView(DocumentListView):
    def dispatch(self, request, *args, **kwargs):
        self.workflow = get_object_or_404(Workflow.on_organization, pk=self.kwargs['pk'])

        try:
            Permission.check_permissions(
                request.user, (permission_workflow_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_workflow_view, request.user, self.workflow
            )

        return super(
            WorkflowDocumentListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document_queryset(self):
        return Document.on_organization.filter(
            document_type__in=self.workflow.document_types.all()
        )

    def get_extra_context(self):
        return {
            'hide_links': True,
            'object': self.workflow,
            'title': _('Documents with the workflow: %s') % self.workflow
        }


class WorkflowInstanceDetailView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_workflow_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_workflow_view, request.user,
                self.get_workflow_instance().document
            )

        return super(
            WorkflowInstanceDetailView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'hide_object': True,
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_workflow_instance().document,
            'title': _('Detail of workflow: %(workflow)s') % {
                'workflow': self.get_workflow_instance()
            },
            'workflow_instance': self.get_workflow_instance(),
        }

    def get_queryset(self):
        return self.get_workflow_instance().log_entries.order_by('-datetime')

    def get_workflow_instance(self):
        return get_object_or_404(WorkflowInstance.on_organization, pk=self.kwargs['pk'])


class WorkflowInstanceTransitionView(FormView):
    form_class = WorkflowInstanceTransitionForm
    template_name = 'appearance/generic_form.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_workflow_transition,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_workflow_transition, request.user,
                self.get_workflow_instance().document
            )

        return super(
            WorkflowInstanceTransitionView, self
        ).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        transition = self.get_workflow_instance().workflow.transitions.get(
            pk=form.cleaned_data['transition']
        )
        self.get_workflow_instance().do_transition(
            comment=form.cleaned_data['comment'], transition=transition,
            user=self.request.user
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_workflow_instance().document,
            'submit_label': _('Submit'),
            'title': _(
                'Do transition for workflow: %s'
            ) % self.get_workflow_instance(),
            'workflow_instance': self.get_workflow_instance(),
        }

    def get_form_kwargs(self):
        kwargs = super(WorkflowInstanceTransitionView, self).get_form_kwargs()
        kwargs['workflow'] = self.get_workflow_instance()
        return kwargs

    def get_success_url(self):
        return self.get_workflow_instance().get_absolute_url()

    def get_workflow_instance(self):
        return get_object_or_404(WorkflowInstance.on_organization, pk=self.kwargs['pk'])


# Setup

class SetupWorkflowListView(SingleObjectListView):
    extra_context = {
        'title': _('Workflows'),
        'hide_link': True,
    }
    view_permission = permission_workflow_view

    def get_queryset(self):
        return Workflow.on_organization.all()


class SetupWorkflowCreateView(SingleObjectCreateView):
    form_class = WorkflowForm
    view_permission = permission_workflow_create
    post_action_redirect = reverse_lazy('document_states:setup_workflow_list')

    def get_queryset(self):
        return Workflow.on_organization.all()


class SetupWorkflowEditView(SingleObjectEditView):
    form_class = WorkflowForm
    view_permission = permission_workflow_edit
    post_action_redirect = reverse_lazy('document_states:setup_workflow_list')

    def get_queryset(self):
        return Workflow.on_organization.all()


class SetupWorkflowDeleteView(SingleObjectDeleteView):
    view_permission = permission_workflow_delete
    post_action_redirect = reverse_lazy('document_states:setup_workflow_list')

    def get_queryset(self):
        return Workflow.on_organization.all()


class SetupWorkflowDocumentTypesView(AssignRemoveView):
    decode_content_type = True
    object_permission = permission_workflow_edit
    left_list_title = _('Available document types')
    right_list_title = _('Document types assigned this workflow')

    def add(self, item):
        self.get_object().document_types.add(item)
        # TODO: add task launching this workflow for all the document types
        # of item

    def get_extra_context(self):
        return {
            'title': _(
                'Document types assigned the workflow: %s'
            ) % self.get_object(),
            'object': self.get_object(),
        }

    def get_object(self):
        return get_object_or_404(Workflow.on_organization, pk=self.kwargs['pk'])

    def left_list(self):
        return AssignRemoveView.generate_choices(
            self.get_object().get_document_types_not_in_workflow()
        )

    def right_list(self):
        return AssignRemoveView.generate_choices(
            self.get_object().document_types.all()
        )

    def remove(self, item):
        self.get_object().document_types.remove(item)
        # TODO: add task deleting this workflow for all the document types of
        # item


class SetupWorkflowStateListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_workflow_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_workflow_view, request.user, self.get_workflow()
            )

        return super(
            SetupWorkflowStateListView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object': self.get_workflow(),
            'title': _('States of workflow: %s') % self.get_workflow()
        }

    def get_queryset(self):
        return self.get_workflow().states.all()

    def get_workflow(self):
        return get_object_or_404(Workflow.on_organization, pk=self.kwargs['pk'])


class SetupWorkflowStateCreateView(SingleObjectCreateView):
    form_class = WorkflowStateForm
    view_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'object': self.get_workflow(),
            'title': _(
                'Create states for workflow: %s'
            ) % self.get_workflow()
        }

    def get_workflow(self):
        return get_object_or_404(Workflow.on_organization, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_workflow().states.all()

    def get_success_url(self):
        return reverse(
            'document_states:setup_workflow_states', args=(self.kwargs['pk'],)
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.workflow = self.get_workflow()
        self.object.save()
        return super(SetupWorkflowStateCreateView, self).form_valid(form)


class SetupWorkflowStateDeleteView(SingleObjectDeleteView):
    model = WorkflowState
    view_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_object(),
            'workflow_instance': self.get_object().workflow,
        }

    def get_success_url(self):
        return reverse(
            'document_states:setup_workflow_states',
            args=(self.get_object().workflow.pk,)
        )


class SetupWorkflowStateEditView(SingleObjectEditView):
    form_class = WorkflowStateForm
    model = WorkflowState
    view_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_object(),
            'workflow_instance': self.get_object().workflow,
        }

    def get_success_url(self):
        return reverse(
            'document_states:setup_workflow_states',
            args=(self.get_object().workflow.pk,)
        )


# Transitions


class SetupWorkflowTransitionListView(SingleObjectListView):
    view_permission = permission_workflow_view

    def get_workflow(self):
        return get_object_or_404(Workflow.on_organization, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_workflow().transitions.all()

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object': self.get_workflow(),
            'title': _(
                'Transitions of workflow: %s'
            ) % self.get_workflow()
        }


class SetupWorkflowTransitionCreateView(SingleObjectCreateView):
    form_class = WorkflowTransitionForm
    view_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'object': self.get_workflow(),
            'title': _(
                'Create transitions for workflow: %s'
            ) % self.get_workflow()
        }

    def get_form_kwargs(self):
        kwargs = super(
            SetupWorkflowTransitionCreateView, self
        ).get_form_kwargs()
        kwargs['workflow'] = self.get_workflow()
        return kwargs

    def get_workflow(self):
        return get_object_or_404(Workflow.on_organization, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_workflow().transitions.all()

    def get_success_url(self):
        return reverse(
            'document_states:setup_workflow_transitions',
            args=(self.kwargs['pk'],)
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.workflow = self.get_workflow()
        try:
            self.object.save()
        except IntegrityError:
            messages.error(
                self.request, _('Unable to save transition; integrity error.')
            )
            return super(
                SetupWorkflowTransitionCreateView, self
            ).form_invalid(form)
        else:
            return HttpResponseRedirect(self.get_success_url())


class SetupWorkflowTransitionDeleteView(SingleObjectDeleteView):
    model = WorkflowTransition
    view_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'navigation_object_list': ('object', 'workflow_instance'),
            'workflow_instance': self.get_object().workflow,
        }

    def get_success_url(self):
        return reverse(
            'document_states:setup_workflow_transitions',
            args=(self.get_object().workflow.pk,)
        )


class SetupWorkflowTransitionEditView(SingleObjectEditView):
    form_class = WorkflowTransitionForm
    model = WorkflowTransition
    view_permission = permission_workflow_edit

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_object(),
            'workflow_instance': self.get_object().workflow,
        }

    def get_form_kwargs(self):
        kwargs = super(
            SetupWorkflowTransitionEditView, self
        ).get_form_kwargs()
        kwargs['workflow'] = self.get_object().workflow
        return kwargs

    def get_success_url(self):
        return reverse(
            'document_states:setup_workflow_transitions',
            args=(self.get_object().workflow.pk,)
        )
