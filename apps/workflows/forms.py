from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Workflow, State, WorkflowState, WorkflowNode


class NodeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        #workflow = kwargs.pop('workflow')
        super(WorkflowStateSetupForm, self).__init__(*args, **kwargs)
        #self.fields['workflow'].initial = workflow
        #self.fields['workflow'].widget = forms.widgets.HiddenInput()

    #def choices(self, workflow):
    #    return {
    ##        'next_node': workflow.nodes.all()
    #    }    
    

class WorkflowSetupForm(forms.ModelForm):
    class Meta:
        exclude = ('initial_node,')
        model = Workflow


class StateSetupForm(forms.ModelForm):
    class Meta:
        model = State


class WorkflowStateSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        workflow = kwargs.pop('workflow')
        super(WorkflowStateSetupForm, self).__init__(*args, **kwargs)
        self.fields['workflow'].initial = workflow
        self.fields['workflow'].widget = forms.widgets.HiddenInput()
    
    class Meta:
        model = WorkflowState


class WorkflowNodeSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        workflow = kwargs.pop('workflow')
        super(WorkflowNodeSetupForm, self).__init__(*args, **kwargs)
        self.fields['workflow'].initial = workflow
        self.fields['workflow'].widget = forms.widgets.HiddenInput()
    
    class Meta:
        model = WorkflowNode

#class TransitionSetupForm(forms.ModelForm):
#    class Meta:
#        model = Transition
        

#class WorkflowStateTransitionSetupForm(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        workflow_state = kwargs.pop('workflow_state')
#        super(WorkflowStateTransitionSetupForm, self).__init__(*args, **kwargs)
#        self.fields['workflow_state_source'].initial = workflow_state
#        self.fields['workflow_state_source'].widget = forms.widgets.HiddenInput()
#    
#    class Meta:
#        model = WorkflowStateTransition
        
        
