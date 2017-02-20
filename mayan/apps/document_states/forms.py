from __future__ import absolute_import, unicode_literals

from django import forms
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from permissions import Permission

from .models import Workflow, WorkflowState, WorkflowTransition
from .permissions import permission_workflow_transition


class WorkflowForm(forms.ModelForm):
    class Meta:
        fields = ('label',)
        model = Workflow


class WorkflowStateForm(forms.ModelForm):
    class Meta:
        fields = ('initial', 'label', 'completion')
        model = WorkflowState


class WorkflowTransitionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        workflow = kwargs.pop('workflow')
        super(WorkflowTransitionForm, self).__init__(*args, **kwargs)
        self.fields['origin_state'].queryset = self.fields['origin_state'].queryset.filter(workflow=workflow)
        self.fields['destination_state'].queryset = self.fields['destination_state'].queryset.filter(workflow=workflow)

    class Meta:
        fields = ('label', 'origin_state', 'destination_state')
        model = WorkflowTransition


class WorkflowInstanceTransitionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        workflow_instance = kwargs.pop('workflow_instance')
        super(WorkflowInstanceTransitionForm, self).__init__(*args, **kwargs)
        queryset = workflow_instance.get_transition_choices().all()

        try:
            Permission.check_permissions(
                requester=user, permissions=(permission_workflow_transition,)
            )
        except PermissionDenied:
            try:
                # Check for ACL access to the workflow, if true, allow all
                # transition options.
                AccessControlList.objects.check_access(
                    permissions=permission_workflow_transition, user=user,
                    obj=workflow_instance.workflow
                )
            except PermissionDenied:
                # If not ACL access to the workflow, filter transition options
                # by each transition ACL access
                queryset = AccessControlList.objects.filter_by_access(
                    permission=permission_workflow_transition, user=user,
                    queryset=queryset
                )

        self.fields['transition'].queryset = queryset

    transition = forms.ModelChoiceField(
        label=_('Transition'), queryset=WorkflowTransition.objects.none()
    )
    comment = forms.CharField(
        label=_('Comment'), required=False, widget=forms.widgets.Textarea()
    )
