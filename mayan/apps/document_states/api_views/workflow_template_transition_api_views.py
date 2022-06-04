from mayan.apps.rest_api import generics

from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)
from ..serializers.workflow_template_transition_serializers import (
    WorkflowTemplateTransitionSerializer, WorkflowTransitionFieldSerializer,
    WorkflowTemplateTransitionTriggerSerializer
)

from .api_view_mixins import (
    ParentObjectWorkflowTemplateAPIViewMixin,
    ParentObjectWorkflowTemplateTransitionAPIViewMixin
)


# Workflow transition views


class APIWorkflowTemplateTransitionListView(
    ParentObjectWorkflowTemplateAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the workflow template transitions.
    post: Create a new workflow template transition.
    """
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
        'POST': (permission_workflow_template_edit,)
    }
    ordering_fields = ('destination_state', 'id', 'label', 'origin_state')
    serializer_class = WorkflowTemplateTransitionSerializer

    def get_instance_extra_data(self):
        # This method is only called during POST, therefore filter only by
        # edit permission.
        return {
            '_event_actor': self.request.user,
            'workflow': self.workflow_template,
        }

    def get_queryset(self):
        return self.workflow_template.transitions.all()


class APIWorkflowTemplateTransitionView(
    ParentObjectWorkflowTemplateAPIViewMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected workflow template transition.
    get: Return the details of the selected workflow template transition.
    patch: Edit the selected workflow template transition.
    put: Edit the selected workflow template transition.
    """
    mayan_object_permissions = {
        'DELETE': (permission_workflow_template_edit,),
        'GET': (permission_workflow_template_view,),
        'PATCH': (permission_workflow_template_edit,),
        'PUT': (permission_workflow_template_edit,)
    }
    lookup_url_kwarg = 'workflow_template_transition_id'
    serializer_class = WorkflowTemplateTransitionSerializer

    def get_instance_extra_data(self):
        # This method is only called during POST, therefore filter only by
        # edit permission.
        return {
            '_event_actor': self.request.user,
            'workflow': self.workflow_template,
        }

    def get_queryset(self):
        return self.workflow_template.transitions.all()


# Workflow template transition fields


class APIWorkflowTemplateTransitionFieldListView(
    ParentObjectWorkflowTemplateTransitionAPIViewMixin,
    generics.ListCreateAPIView
):
    """
    get: Returns a list of all the workflow template transition fields.
    post: Create a new workflow template transition field.
    """
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
        'POST': (permission_workflow_template_edit,)
    }
    ordering_fields = ('id', 'label', 'name', 'required', 'widget_kwargs')
    serializer_class = WorkflowTransitionFieldSerializer

    def get_instance_extra_data(self):
        # This method is only called during POST, therefore filter only by
        # edit permission.
        return {
            '_event_actor': self.request.user,
            'transition': self.workflow_template_transition
        }

    def get_queryset(self):
        return self.workflow_template_transition.fields.all()


class APIWorkflowTemplateTransitionFieldDetailView(
    ParentObjectWorkflowTemplateTransitionAPIViewMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected workflow template transition field.
    get: Return the details of the selected workflow template transition field.
    patch: Edit the selected workflow template transition field.
    put: Edit the selected workflow template transition field.
    """
    mayan_object_permissions = {
        'DELETE': (permission_workflow_template_edit,),
        'GET': (permission_workflow_template_view,),
        'PATCH': (permission_workflow_template_edit,),
        'PUT': (permission_workflow_template_edit,)
    }
    lookup_url_kwarg = 'workflow_template_transition_field_id'
    serializer_class = WorkflowTransitionFieldSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_queryset(self):
        return self.workflow_template_transition.fields.all()


# Workflow template transition triggers


class APIWorkflowTemplateTransitionTriggerListView(
    ParentObjectWorkflowTemplateTransitionAPIViewMixin,
    generics.ListCreateAPIView
):
    """
    get: Returns a list of all the workflow template transition triggers.
    post: Create a new workflow template transition trigger.
    """
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
        'POST': (permission_workflow_template_edit,)
    }
    ordering_fields = ('event_type', 'id')
    serializer_class = WorkflowTemplateTransitionTriggerSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'transition': self.workflow_template_transition
        }

    def get_queryset(self):
        return self.workflow_template_transition.trigger_events.all()


class APIWorkflowTemplateTransitionTriggerDetailView(
    ParentObjectWorkflowTemplateTransitionAPIViewMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected workflow template transition trigger.
    get: Return the details of the selected workflow template transition trigger.
    patch: Edit the selected workflow template transition trigger.
    put: Edit the selected workflow template transition trigger.
    """
    mayan_object_permissions = {
        'DELETE': (permission_workflow_template_edit,),
        'GET': (permission_workflow_template_view,),
        'PATCH': (permission_workflow_template_edit,),
        'PUT': (permission_workflow_template_edit,)
    }
    lookup_url_kwarg = 'workflow_template_transition_trigger_id'
    serializer_class = WorkflowTemplateTransitionTriggerSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_queryset(self):
        return self.workflow_template_transition.trigger_events.all()
