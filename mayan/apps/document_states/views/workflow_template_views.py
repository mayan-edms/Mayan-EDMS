from django.contrib import messages
from django.db import transaction
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.events import event_document_type_edited
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.views.generics import (
    AddRemoveView, ConfirmView, MultipleObjectFormActionView,
    MultipleObjectConfirmActionView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectDetailView, SingleObjectEditView,
    SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectMixin

from ..events import event_workflow_edited
from ..forms import (
    WorkflowForm, WorkflowMultipleSelectionForm, WorkflowPreviewForm
)
from ..icons import icon_workflow_template_list
from ..links import link_workflow_template_create
from ..models import Workflow
from ..permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit, permission_workflow_tools,
    permission_workflow_view,
)
from ..tasks import (
    task_launch_all_workflows, task_launch_workflow, task_launch_workflow_for
)


class DocumentTypeWorkflowTemplatesView(AddRemoveView):
    main_object_permission = permission_document_type_edit
    main_object_model = DocumentType
    main_object_pk_url_kwarg = 'document_type_id'
    secondary_object_model = Workflow
    secondary_object_permission = permission_workflow_edit
    list_available_title = _('Available workflows')
    list_added_title = _('Workflows assigned this document type')
    related_field = 'workflows'

    def get_actions_extra_kwargs(self):
        return {'_user': self.request.user}

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

    def action_add(self, queryset, _user):
        with transaction.atomic():
            event_document_type_edited.commit(
                actor=_user, target=self.main_object
            )

            for obj in queryset:
                self.main_object.workflows.add(obj)
                event_workflow_edited.commit(
                    action_object=self.main_object, actor=_user, target=obj
                )

    def action_remove(self, queryset, _user):
        with transaction.atomic():
            event_document_type_edited.commit(
                actor=_user, target=self.main_object
            )

            for obj in queryset:
                self.main_object.workflows.remove(obj)
                event_workflow_edited.commit(
                    action_object=self.main_object, actor=_user,
                    target=obj
                )
                obj.instances.filter(
                    document__document_type=self.main_object
                ).delete()


class DocumentWorkflowTemplatesLaunchView(MultipleObjectFormActionView):
    form_class = WorkflowMultipleSelectionForm
    model = Document
    object_permission = permission_workflow_tools
    pk_url_kwarg = 'document_id'
    success_message = _('Workflows launched for %(count)d document')
    success_message_plural = _('Workflows launched for %(count)d documents')

    def get_extra_context(self):
        result = {
            'submit_label': _('Launch'),
            'subtitle': _(
                'Workflows already launched or workflows not applicable to '
                'some documents when multiple documents are selected, '
                'will be silently ignored.'
            ),
            'title': ungettext(
                singular='Launch selected workflows for %(count)d document',
                plural='Launch selected workflows for %(count)d documents',
                number=self.object_list.count()
            ) % {
                'count': self.object_list.count(),
            }
        }

        if self.object_list.count() == 1:
            result.update(
                {
                    'object': self.object_list.first(),
                    'title': _(
                        'Launch selected workflows for document: %s'
                    ) % self.object_list.first()
                }
            )

        return result

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
    view_permission = permission_workflow_create

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class WorkflowTemplateDeleteView(MultipleObjectConfirmActionView):
    model = Workflow
    object_permission = permission_workflow_delete
    pk_url_kwarg = 'workflow_template_id'
    post_action_redirect = reverse_lazy(
        viewname='document_states:workflow_template_list'
    )
    success_message = _('Delete request performed on %(count)d workflow')
    success_message_plural = _(
        'Delete request performed on %(count)d workflows'
    )

    def get_extra_context(self):
        result = {
            'delete_view': True,
            'message': _('All workflow instances will also be deleted.'),
            'title': ungettext(
                singular='Delete the selected workflow?',
                plural='Delete the selected workflows?',
                number=self.object_list.count()
            )
        }

        if self.object_list.count() == 1:
            result.update(
                {
                    'object': self.object_list.first(),
                    'title': _('Delete workflow: %s?') % self.object_list.first()
                }
            )

        return result

    def object_action(self, instance, form=None):
        try:
            instance.delete()
            messages.success(
                message=_(
                    'Workflow "%s" deleted successfully.'
                ) % instance, request=self.request
            )
        except Exception as exception:
            messages.error(
                message=_('Error deleting workflow "%(workflow)s": %(error)s') % {
                    'workflow': instance, 'error': exception
                }, request=self.request
            )


class WorkflowTemplateEditView(SingleObjectEditView):
    form_class = WorkflowForm
    model = Workflow
    object_permission = permission_workflow_edit
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

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class WorkflowTemplateDocumentTypesView(AddRemoveView):
    main_object_permission = permission_workflow_edit
    main_object_model = Workflow
    main_object_pk_url_kwarg = 'workflow_template_id'
    secondary_object_model = DocumentType
    secondary_object_permission = permission_document_type_edit
    list_available_title = _('Available document types')
    list_added_title = _('Document types assigned this workflow')
    related_field = 'document_types'

    def get_actions_extra_kwargs(self):
        return {'_user': self.request.user}

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

    def action_add(self, queryset, _user):
        with transaction.atomic():
            event_workflow_edited.commit(
                actor=_user, target=self.main_object
            )

            for obj in queryset:
                self.main_object.document_types.add(obj)
                event_document_type_edited.commit(
                    action_object=self.main_object, actor=_user, target=obj
                )

    def action_remove(self, queryset, _user):
        with transaction.atomic():
            event_workflow_edited.commit(
                actor=_user, target=self.main_object
            )

            for obj in queryset:
                self.main_object.document_types.remove(obj)
                event_document_type_edited.commit(
                    action_object=self.main_object, actor=_user,
                    target=obj
                )
                self.main_object.instances.filter(
                    document__document_type=obj
                ).delete()


class WorkflowTemplateLaunchView(ExternalObjectMixin, ConfirmView):
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
    object_permission = permission_workflow_view

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
    object_permission = permission_workflow_view
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
