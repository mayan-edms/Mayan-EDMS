from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Workflow, WorkflowState, WorkflowTransition


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
        workflow = kwargs.pop('workflow')
        super(WorkflowInstanceTransitionForm, self).__init__(*args, **kwargs)
        self.fields['transition'].choices = workflow.get_transition_choices().values_list('pk', 'label')

    transition = forms.ChoiceField(label=_('Transition'))
    comment = forms.CharField(
        label=_('Comment'), required=False, widget=forms.widgets.Textarea()
    )
