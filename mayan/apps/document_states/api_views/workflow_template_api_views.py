from mayan.apps.converter.api_view_mixins import APIImageViewMixin
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import permission_document_type_view
from mayan.apps.documents.serializers.document_type_serializers import DocumentTypeSerializer
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin
from mayan.apps.rest_api import generics

from ..models.workflow_models import Workflow
from ..permissions import (
    permission_workflow_template_create, permission_workflow_template_delete,
    permission_workflow_template_edit, permission_workflow_template_view
)
from ..serializers.workflow_template_serializers import (
    WorkflowTemplateDocumentTypeAddSerializer,
    WorkflowTemplateDocumentTypeRemoveSerializer, WorkflowTemplateSerializer
)


class APIWorkflowTemplateDocumentTypeListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the document types attached to a workflow template.
    """
    external_object_class = Workflow
    external_object_pk_url_kwarg = 'workflow_template_id'
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,)
    }
    mayan_object_permissions = {
        'GET': (permission_document_type_view,)
    }
    serializer_class = DocumentTypeSerializer

    def get_queryset(self):
        """
        This view returns a list of document types that belong to a workflow template.
        """
        return self.external_object.document_types.all()


class APIWorkflowTemplateDocumentTypeAddView(generics.ObjectActionAPIView):
    """
    post: Add a document type to a workflow template.
    """
    lookup_url_kwarg = 'workflow_template_id'
    mayan_object_permissions = {
        'POST': (permission_workflow_template_edit,)
    }
    serializer_class = WorkflowTemplateDocumentTypeAddSerializer
    queryset = Workflow.objects.all()

    def object_action(self, request, serializer):
        document_type = serializer.validated_data['document_type_id']
        self.object._event_actor = self.request.user
        self.object.document_types_add(
            queryset=DocumentType.objects.filter(pk=document_type.id)
        )


class APIWorkflowTemplateDocumentTypeRemoveView(generics.ObjectActionAPIView):
    """
    post: Remove a document type from a workflow template.
    """
    lookup_url_kwarg = 'workflow_template_id'
    mayan_object_permissions = {
        'POST': (permission_workflow_template_edit,)
    }
    serializer_class = WorkflowTemplateDocumentTypeRemoveSerializer
    queryset = Workflow.objects.all()

    def object_action(self, request, serializer):
        document_type = serializer.validated_data['document_type_id']
        self.object._event_actor = self.request.user
        self.object.document_types_remove(
            queryset=DocumentType.objects.filter(pk=document_type.id)
        )


class APIWorkflowTemplateImageView(
    APIImageViewMixin, generics.RetrieveAPIView
):
    """
    get: Returns an image representation of the selected workflow template.
    """
    lookup_url_kwarg = 'workflow_template_id'
    mayan_object_permissions = {
        'GET': (permission_workflow_template_view,)
    }
    queryset = Workflow.objects.all()


class APIWorkflowTemplateListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the workflow templates.
    post: Create a new workflow template.
    """
    mayan_object_permissions = {
        'GET': (permission_workflow_template_view,)
    }
    mayan_view_permissions = {
        'POST': (permission_workflow_template_create,)
    }
    ordering_fields = ('id', 'internal_name', 'label')
    queryset = Workflow.objects.all()
    serializer_class = WorkflowTemplateSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIWorkflowTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected workflow template.
    get: Return the details of the selected workflow template.
    patch: Edit the selected workflow template.
    put: Edit the selected workflow template.
    """
    lookup_url_kwarg = 'workflow_template_id'
    mayan_object_permissions = {
        'DELETE': (permission_workflow_template_delete,),
        'GET': (permission_workflow_template_view,),
        'PATCH': (permission_workflow_template_edit,),
        'PUT': (permission_workflow_template_edit,)
    }
    queryset = Workflow.objects.all()
    serializer_class = WorkflowTemplateSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }
