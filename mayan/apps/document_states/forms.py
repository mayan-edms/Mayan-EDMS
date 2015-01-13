from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import WorkflowState, WorkflowTransition


class WorkflowStateForm(forms.ModelForm):
    class Meta:
        fields = ('initial', 'label')
        model = WorkflowState


class WorkflowTransitionForm(forms.ModelForm):
    class Meta:
        # TODO: restrict states to the ones of this workflow
        fields = ('label', 'origin_state', 'destination_state')
        model = WorkflowTransition
