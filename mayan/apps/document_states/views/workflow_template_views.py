from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.views.generics import (
    AddRemoveView, ConfirmView, MultipleObjectFormActionView,
    MultipleObjectDeleteView, SingleObjectCreateView, SingleObjectDetailView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..forms import (
    WorkflowForm, WorkflowMultipleSelectionForm, WorkflowPreviewForm
)
from ..icons import icon_workflow_template_list
from ..links import link_workflow_template_create
from ..models import Workflow
from ..permissions import (
    permission_workflow_template_create, permission_workflow_template_delete,
    permission_workflow_template_edit, permission_workflow_tools,
    permission_workflow_template_view,
)
from ..tasks import (
    task_launch_all_workflows, task_launch_workflow, task_launch_workflow_for
)


class DocumentTypeWorkflowTemplatesView(AddRemoveView):
    main_object_permission = permission_document_type_edit
    main_object_model = DocumentType
    main_object_pk_url_kwarg = 'document_type_id'
    secondary_object_model = Workflow
    secondary_object_permission = permission_workflow_template_edit
    list_available_title = _('Available workflows')
    list_added_title = _('Workflows assigned this document type')
    related_field = 'workflows'

    def action_add(self, queryset, _event_actor):
        for workflow_template in queryset.all():
            workflow_template._event_actor = _event_actor
            workflow_template.document_types_add(
                queryset=DocumentType.objects.filter(pk=self.main_object.pk)
            )

    def action_remove(self, queryset, _event_actor):
        for workflow_template in queryset.all():
            workflow_template._event_actor = _event_actor
            workflow_template.document_types_remove(
                queryset=DocumentType.objects.filter(pk=self.main_object.pk)
            )

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'subtitle': _(
                'Removing a workflow from a document type will also '
                'remove all running instances of that workflow.'
            ),
            'title': _(
                'Workflows assigned the document type: %s'
            ) % self.main_object,
        }


class DocumentWorkflowTemplatesLaunchView(MultipleObjectFormActionView):
    error_message = _(
        'Error launching workflows for document "%(instance)s"; %(exception)s'
    )
    form_class = WorkflowMultipleSelectionForm
    object_permission = permission_workflow_tools
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid
    success_message_single = _('Workflows launched successfully for document "%(object)s".')
    success_message_singular = _('Workflows launched successfully for %(count)d document.')
    success_message_plural = _('Workflows launched successfully for %(count)d documents.')
    title_single = _('Launch workflow: %(object)s.')
    title_singular = _('Launch workflows for the selected %(count)d document.')
    title_plural = _('Launch workflows for the selected %(count)d documents.')

    def get_extra_context(self):
        return {
            'submit_label': _('Launch'),
            'subtitle': _(
                'Workflows already launched or workflows not applicable to '
                'some documents when multiple documents are selected, '
                'will be silently ignored.'
            ),
        }

    def get_form_extra_kwargs(self):
        workflows_union = Workflow.objects.filter(
            document_types__in=self.object_list.values('document_type')
        ).distinct()

        result = {
            'help_text': _('Workflows to be launched.'),
            'permission': permission_workflow_tools,
            'queryset': workflows_union,
            'user': self.request.user
        }

        return result

    def object_action(self, form, instance):
        workflow_queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_workflow_tools,
            queryset=form.cleaned_data['workflows'], user=self.request.user
        )

        for workflow in workflow_queryset:
            task_launch_workflow_for.apply_async(
                kwargs={
                    'document_id': instance.pk, 'workflow_id': workflow.pk
                }
            )


class WorkflowTemplateCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create workflow')}
    form_class = WorkflowForm
    model = Workflow
    post_action_redirect = reverse_lazy(
        viewname='document_states:workflow_template_list'
    )
    view_permission = permission_workflow_template_create

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class WorkflowTemplateDeleteView(MultipleObjectDeleteView):
    error_message = _('Error deleting workflow "%(instance)s"; %(exception)s')
    model = Workflow
    object_permission = permission_workflow_template_delete
    pk_url_kwarg = 'workflow_template_id'
    post_action_redirect = reverse_lazy(
        viewname='document_states:workflow_template_list'
    )
    success_message_single = _('Workflow "%(object)s" deleted successfully.')
    success_message_singular = _('%(count)d workflow deleted successfully.')
    success_message_plural = _('%(count)d workflows deleted successfully.')
    title_single = _('Delete workflow: %(object)s.')
    title_singular = _('Delete the %(count)d selected workflow.')
    title_plural = _('Delete the %(count)d selected workflows.')

    def get_extra_context(self):
        return {
            'message': _('All workflow instances will also be deleted.')
        }

    def object_action(self, instance, form=None):
        instance.delete()


class WorkflowTemplateEditView(SingleObjectEditView):
    form_class = WorkflowForm
    model = Workflow
    object_permission = permission_workflow_template_edit
    pk_url_kwarg = 'workflow_template_id'
    post_action_redirect = reverse_lazy(
        viewname='document_states:workflow_template_list'
    )

    def get_extra_context(self):
        return {
            'title': _(
                'Edit workflow: %s'
            ) % self.object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class WorkflowTemplateDocumentTypesView(AddRemoveView):
    main_object_method_add_name = 'document_types_add'
    main_object_method_remove_name = 'document_types_remove'
    main_object_model = Workflow
    main_object_permission = permission_workflow_template_edit
    main_object_pk_url_kwarg = 'workflow_template_id'
    secondary_object_model = DocumentType
    secondary_object_permission = permission_document_type_edit
    list_available_title = _('Available document types')
    list_added_title = _('Document types assigned this workflow')
    related_field = 'document_types'

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'subtitle': _(
                'Removing a document type from a workflow will also '
                'remove all running instances of that workflow for '
                'documents of the document type just removed.'
            ),
            'title': _(
                'Document types assigned the workflow: %s'
            ) % self.main_object,
        }


class WorkflowTemplateLaunchView(ExternalObjectViewMixin, ConfirmView):
    external_object_class = Workflow
    external_object_permission = permission_workflow_tools
    external_object_pk_url_kwarg = 'workflow_template_id'

    def get_extra_context(self):
        return {
            'title': _('Launch workflow?'),
            'subtitle': _(
                'This will launch the workflow for documents that have '
                'already been uploaded.'
            )
        }

    def view_action(self):
        task_launch_workflow.apply_async(
            kwargs={
                'workflow_id': self.external_object.pk,
            }
        )
        messages.success(
            message=_('Workflow launch queued successfully.'),
            request=self.request
        )


class WorkflowTemplateListView(SingleObjectListView):
    model = Workflow
    object_permission = permission_workflow_template_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_workflow_template_list,
            'no_results_main_link': link_workflow_template_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Workflows store a series of states and keep track of the '
                'current state of a document. Transitions are used to change the '
                'current state to a new one.'
            ),
            'no_results_title': _(
                'No workflows have been defined'
            ),
            'title': _('Workflows'),
        }


class WorkflowTemplatePreviewView(SingleObjectDetailView):
    form_class = WorkflowPreviewForm
    model = Workflow
    object_permission = permission_workflow_template_view
    pk_url_kwarg = 'workflow_template_id'

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.object,
            'title': _('Preview of: %s') % self.object
        }


class ToolLaunchWorkflows(ConfirmView):
    extra_context = {
        'title': _('Launch all workflows?'),
        'subtitle': _(
            'This will launch all workflows created after documents have '
            'already been uploaded.'
        )
    }
    view_permission = permission_workflow_tools

    def view_action(self):
        task_launch_all_workflows.apply_async()
        messages.success(
            message=_('Workflow launch queued successfully.'),
            request=self.request
        )
