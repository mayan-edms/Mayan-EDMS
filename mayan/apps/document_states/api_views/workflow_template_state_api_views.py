from mayan.apps.rest_api import generics

from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)
from ..serializers.workflow_template_state_serializers import (
    WorkflowTemplateStateActionSerializer, WorkflowTemplateStateSerializer
)

from .api_view_mixins import (
    ParentObjectWorkflowTemplateAPIViewMixin,
    ParentObjectWorkflowTemplateStateAPIViewMixin
)


class APIWorkflowTemplateStateListView(
    ParentObjectWorkflowTemplateAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the workflow template states.
    post: Create a new workflow template state.
    """
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
        'POST': (permission_workflow_template_edit,)
    }
    ordering_fields = ('completion', 'id', 'initial', 'label')
    serializer_class = WorkflowTemplateStateSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'workflow': self.workflow_template
        }

    def get_queryset(self):
        return self.workflow_template.states.all()


class APIWorkflowTemplateStateView(
    ParentObjectWorkflowTemplateAPIViewMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected workflow template state.
    get: Return the details of the selected workflow template state.
    patch: Edit the selected workflow template state.
    put: Edit the selected workflow template state.
    """
    mayan_object_permissions = {
        'DELETE': (permission_workflow_template_edit,),
        'GET': (permission_workflow_template_view,),
        'PATCH': (permission_workflow_template_edit,),
        'PUT': (permission_workflow_template_edit,)
    }
    lookup_url_kwarg = 'workflow_template_state_id'
    serializer_class = WorkflowTemplateStateSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_queryset(self):
        return self.workflow_template.states.all()


class APIWorkflowTemplateStateActionListView(
    ParentObjectWorkflowTemplateStateAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the workflow template state actions.
    post: Create a new workflow template state action.
    """
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
        'POST': (permission_workflow_template_edit,),
    }
    ordering_fields = ('label', 'enabled', 'id')
    serializer_class = WorkflowTemplateStateActionSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'state': self.workflow_template_state
        }

    def get_queryset(self):
        return self.workflow_template_state.actions.all()


class APIWorkflowTemplateStateActionDetailView(
    ParentObjectWorkflowTemplateStateAPIViewMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected workflow template state action.
    get: Return the details of the selected workflow template state action.
    patch: Edit the selected workflow template state action.
    put: Edit the selected workflow template state action.
    """
    mayan_object_permissions = {
        'DELETE': (permission_workflow_template_edit,),
        'GET': (permission_workflow_template_view,),
        'PATCH': (permission_workflow_template_edit,),
        'PUT': (permission_workflow_template_edit,),
    }
    lookup_url_kwarg = 'workflow_template_state_action_id'
    serializer_class = WorkflowTemplateStateActionSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_queryset(self):
        return self.workflow_template_state.actions.all()
