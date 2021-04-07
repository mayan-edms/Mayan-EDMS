from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.views.forms import DynamicForm
from mayan.apps.views.generics import FormView, SingleObjectListView
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..forms import WorkflowInstanceTransitionSelectForm
from ..icons import icon_workflow_instance_detail, icon_workflow_template_list
from ..links import link_workflow_instance_transition
from ..literals import FIELD_TYPE_MAPPING, WIDGET_CLASS_MAPPING
from ..models import WorkflowInstance
from ..permissions import (
    permission_workflow_instance_transition, permission_workflow_template_view
)


class WorkflowInstanceListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_permission = permission_workflow_template_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid
    object_permission = permission_workflow_template_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'no_results_icon': icon_workflow_template_list,
            'no_results_text': _(
                'Assign workflows to the document type of this document '
                'to have this document execute those workflows. '
            ),
            'no_results_title': _(
                'There are no workflows for this document'
            ),
            'object': self.external_object,
            'title': _(
                'Workflows for document: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.workflows.all()


class WorkflowInstanceDetailView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_permission = permission_workflow_template_view
    external_object_pk_url_kwarg = 'workflow_instance_id'
    object_permission = permission_workflow_template_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'navigation_object_list': ('object', 'workflow_instance'),
            'no_results_icon': icon_workflow_instance_detail,
            'no_results_main_link': link_workflow_instance_transition.resolve(
                context=RequestContext(
                    dict_={'object': self.external_object},
                    request=self.request
                )
            ),
            'no_results_text': _(
                'This view will show the state changes as a workflow '
                'instance is transitioned.'
            ),
            'no_results_title': _(
                'There are no details for this workflow instance'
            ),
            'object': self.external_object.document,
            'title': _('Detail of workflow: %(workflow)s') % {
                'workflow': self.external_object
            },
            'workflow_instance': self.external_object,
        }

    def get_external_object_queryset(self):
        document_queryset = AccessControlList.objects.restrict_queryset(
            queryset=Document.valid.all(),
            permission=permission_workflow_template_view,
            user=self.request.user
        )

        return WorkflowInstance.objects.filter(
            document_id__in=document_queryset.values('pk')
        )

    def get_source_queryset(self):
        return self.external_object.log_entries.order_by('-datetime')


class WorkflowInstanceTransitionExecuteView(ExternalObjectViewMixin, FormView):
    external_object_pk_url_kwarg = 'workflow_instance_id'
    external_object_queryset = WorkflowInstance.valid
    form_class = DynamicForm
    template_name = 'appearance/generic_form.html'

    def form_valid(self, form):
        form_data = form.cleaned_data
        comment = form_data.pop('comment')

        self.external_object.do_transition(
            comment=comment, extra_data=form_data,
            transition=self.get_workflow_template_transition(),
            user=self.request.user,
        )
        messages.success(
            message=_(
                'Document "%s" transitioned successfully'
            ) % self.external_object.document, request=self.request
        )
        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.external_object.document,
            'submit_label': _('Submit'),
            'title': _(
                'Execute transition "%(transition)s" for workflow: %(workflow)s'
            ) % {
                'transition': self.get_workflow_template_transition(),
                'workflow': self.external_object,
            },
            'workflow_instance': self.external_object,
        }

    def get_form_extra_kwargs(self):
        schema = {
            'fields': {
                'comment': {
                    'label': _('Comment'),
                    'class': 'django.forms.CharField', 'kwargs': {
                        'help_text': _(
                            'Optional comment to attach to the transition.'
                        ),
                        'required': False,
                    }
                }
            },
            'widgets': {
                'comment': {
                    'class': 'django.forms.widgets.Textarea',
                    'kwargs': {
                        'attrs': {
                            'rows': 3
                        }
                    }
                }
            }
        }

        for field in self.get_workflow_template_transition().fields.all():
            schema['fields'][field.name] = {
                'class': FIELD_TYPE_MAPPING[field.field_type],
                'help_text': field.help_text,
                'label': field.label,
                'required': field.required,
            }
            if field.widget:
                schema['widgets'][field.name] = {
                    'class': WIDGET_CLASS_MAPPING[field.widget],
                    'kwargs': field.get_widget_kwargs()
                }

        return {'schema': schema}

    def get_success_url(self):
        return self.external_object.get_absolute_url()

    def get_external_object_queryset_filtered(self):
        queryset = super().get_external_object_queryset_filtered()

        # Filter further down by document access.

        document_queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_workflow_instance_transition,
            queryset=Document.valid.all(),
            user=self.request.user
        )

        return queryset.filter(document__in=document_queryset)

    def get_workflow_template_transition(self):
        return get_object_or_404(
            klass=self.external_object.get_transition_choices(
                _user=self.request.user
            ), pk=self.kwargs['workflow_template_transition_id']
        )


class WorkflowInstanceTransitionSelectView(ExternalObjectViewMixin, FormView):
    external_object_pk_url_kwarg = 'workflow_instance_id'
    external_object_queryset = WorkflowInstance.valid
    form_class = WorkflowInstanceTransitionSelectForm
    template_name = 'appearance/generic_form.html'

    def form_valid(self, form):
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='document_states:workflow_instance_transition_execute',
                kwargs={
                    'workflow_instance_id': self.external_object.pk,
                    'workflow_template_transition_id': form.cleaned_data['transition'].pk
                }
            )
        )

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.external_object.document,
            'submit_label': _('Select'),
            'title': _(
                'Select transition for workflow "%(workflow)s" of document "%(document)s"'
            ) % {
                'document': self.external_object.document,
                'workflow': self.external_object
            },
            'workflow_instance': self.external_object
        }

    def get_external_object_queryset_filtered(self):
        queryset = super().get_external_object_queryset_filtered()

        # Filter further down by document access.

        document_queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_workflow_instance_transition,
            queryset=Document.valid.all(),
            user=self.request.user
        )

        return queryset.filter(document__in=document_queryset)

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user,
            'workflow_instance': self.external_object
        }
