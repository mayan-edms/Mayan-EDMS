from mayan.apps.rest_api import generics

from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)
from ..serializers.workflow_template_state_escalation_serializers import WorkflowTemplateStateEscalationSerializer

from .api_view_mixins import ParentObjectWorkflowTemplateStateAPIViewMixin


class APIWorkflowTemplateStateEscalationListView(
    ParentObjectWorkflowTemplateStateAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the workflow template state escalations.
    post: Create a new workflow template state escalation.
    """
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
        'POST': (permission_workflow_template_edit,)
    }
    ordering_fields = ('priority', 'id')
    serializer_class = WorkflowTemplateStateEscalationSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'state': self.workflow_template_state
        }

    def get_queryset(self):
        return self.workflow_template_state.escalations.all()


class APIWorkflowTemplateStateEscalationDetailView(
    ParentObjectWorkflowTemplateStateAPIViewMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected workflow template state escalation.
    get: Return the details of the selected workflow template state escalation.
    patch: Edit the selected workflow template state escalation.
    put: Edit the selected workflow template state escalation.
    """
    mayan_object_permissions = {
        'DELETE': (permission_workflow_template_edit,),
        'GET': (permission_workflow_template_view,),
        'PATCH': (permission_workflow_template_edit,),
        'PUT': (permission_workflow_template_edit,)
    }
    lookup_url_kwarg = 'workflow_template_state_escalation_id'
    serializer_class = WorkflowTemplateStateEscalationSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_queryset(self):
        return self.workflow_template_state.escalations.all()
