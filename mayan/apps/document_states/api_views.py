from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics

from acls.models import AccessControlList
from documents.permissions import permission_document_type_view
from documents.serializers import DocumentSerializer, DocumentTypeSerializer
from permissions import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Workflow, WorkflowState
from .permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit, permission_workflow_view
)
from .serializers import (
    NewWorkflowDocumentTypeSerializer, WorkflowDocumentTypeSerializer,
    WorkflowSerializer, WorkflowStateSerializer, WritableWorkflowSerializer
)


class APIWorkflowDocumentTypeList(generics.ListCreateAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {
        'GET': (permission_document_type_view,),
    }

    def get(self, *args, **kwargs):
        """
        Returns a list of all the document types attached to a workflow.
        """

        return super(APIWorkflowDocumentTypeList, self).get(*args, **kwargs)

    def get_queryset(self):
        """
        This view returns a list of document types that belong to a workflow
        RESEARCH: Could the documents.api_views.APIDocumentTypeList class
        be subclasses for this?
        """

        return self.get_workflow().document_types.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkflowDocumentTypeSerializer
        elif self.request.method == 'POST':
            return NewWorkflowDocumentTypeSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """

        return {
            'format': self.format_kwarg,
            'request': self.request,
            'workflow': self.get_workflow(),
            'view': self
        }

    def get_workflow(self):
        """
        Retrieve the parent workflow of the workflow document type.
        Perform custom permission and access check.
        """

        if self.request.method == 'GET':
            permission_required = permission_workflow_view
        else:
            permission_required = permission_workflow_edit

        workflow = get_object_or_404(Workflow, pk=self.kwargs['pk'])

        try:
            Permission.check_permissions(
                self.request.user, (permission_required,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_required, self.request.user, workflow
            )

        return workflow

    def post(self, request, *args, **kwargs):
        """
        Attach a document type to a specified workflow.
        """

        return super(
            APIWorkflowDocumentTypeList, self
        ).post(request, *args, **kwargs)


class APIWorkflowDocumentTypeView(generics.RetrieveDestroyAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    lookup_url_kwarg = 'document_type_pk'
    mayan_object_permissions = {
        'GET': (permission_document_type_view,),
    }
    serializer_class = WorkflowDocumentTypeSerializer

    def delete(self, request, *args, **kwargs):
        """
        Remove a document type from the selected workflow.
        """

        return super(
            APIWorkflowDocumentTypeView, self
        ).delete(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Returns the details of the selected workflow document type.
        """

        return super(APIWorkflowDocumentTypeView, self).get(*args, **kwargs)

    def get_queryset(self):
        return self.get_workflow().document_types.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'format': self.format_kwarg,
            'request': self.request,
            'workflow': self.get_workflow(),
            'view': self
        }

    def get_workflow(self):
        """
        This view returns a document types that belongs to a workflow
        RESEARCH: Could the documents.api_views.APIDocumentTypeView class
        be subclasses for this?
        RESEARCH: Since this is a parent-child API view could this be made
        into a generic API class?
        RESEARCH: Reuse get_workflow method from APIWorkflowDocumentTypeList?
        """

        if self.request.method == 'GET':
            permission_required = permission_workflow_view
        else:
            permission_required = permission_workflow_edit

        workflow = get_object_or_404(Workflow, pk=self.kwargs['pk'])

        try:
            Permission.check_permissions(
                self.request.user, (permission_required,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_required, self.request.user, workflow
            )

        return workflow

    def perform_destroy(self, instance):
        """
        RESEARCH: Move this kind of methods to the serializer instead it that
        ability becomes available in Django REST framework
        """

        self.get_workflow().document_types.remove(instance)


class APIWorkflowListView(generics.ListCreateAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {
        'GET': (permission_workflow_view,),
        'POST': (permission_workflow_create,)
    }
    permission_classes = (MayanPermission,)
    queryset = Workflow.objects.all()

    def get(self, *args, **kwargs):
        """
        Returns a list of all the workflows.
        """
        return super(APIWorkflowListView, self).get(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkflowSerializer
        else:
            return WritableWorkflowSerializer

    def post(self, *args, **kwargs):
        """
        Create a new workflow.
        """
        return super(APIWorkflowListView, self).post(*args, **kwargs)


class APIWorkflowView(generics.RetrieveUpdateDestroyAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {
        'DELETE': (permission_workflow_delete,),
        'GET': (permission_workflow_view,),
        'PATCH': (permission_workflow_edit,),
        'PUT': (permission_workflow_edit,)
    }
    queryset = Workflow.objects.all()

    def delete(self, *args, **kwargs):
        """
        Delete the selected workflow.
        """

        return super(APIWorkflowView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Return the details of the selected workflow.
        """

        return super(APIWorkflowView, self).get(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkflowSerializer
        else:
            return WritableWorkflowSerializer

    def patch(self, *args, **kwargs):
        """
        Edit the selected workflow.
        """

        return super(APIWorkflowView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the selected workflow.
        """

        return super(APIWorkflowView, self).put(*args, **kwargs)


## Workflow state views


class APIWorkflowStateListView(generics.ListCreateAPIView):
    serializer_class = WorkflowStateSerializer
    queryset = WorkflowState.objects.all()

    def get(self, *args, **kwargs):
        """
        Returns a list of all the workflow states.
        """
        return super(APIWorkflowStateListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Create a new workflow state.
        """
        return super(APIWorkflowStateListView, self).post(*args, **kwargs)


class APIWorkflowStateView(generics.RetrieveAPIView):
    queryset = WorkflowState.objects.all()
    serializer_class = WorkflowStateSerializer
