import logging

from rest_framework import status

from mayan.apps.converter.api_view_mixins import APIImageViewMixin
from mayan.apps.rest_api import generics

from ..permissions import (
    permission_document_version_create, permission_document_version_delete,
    permission_document_version_edit, permission_document_version_export,
    permission_document_version_view
)
from ..serializers.document_version_serializers import (
    DocumentVersionSerializer, DocumentVersionPageSerializer
)
from ..tasks import task_document_version_export

from .mixins import (
    ParentObjectDocumentAPIViewMixin, ParentObjectDocumentVersionAPIViewMixin
)

logger = logging.getLogger(name=__name__)


class APIDocumentVersionDetailView(
    ParentObjectDocumentAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected document version.
    get: Returns the selected document version details.
    patch: Edit the properties of the selected document version.
    put: Edit the properties of the selected document version.
    """
    lookup_url_kwarg = 'document_version_id'
    mayan_object_permissions = {
        'DELETE': (permission_document_version_delete,),
        'GET': (permission_document_version_view,),
        'PATCH': (permission_document_version_edit,),
        'PUT': (permission_document_version_edit,)
    }
    serializer_class = DocumentVersionSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_queryset(self):
        return self.get_document().versions.all()


class APIDocumentVersionExportView(
    ParentObjectDocumentAPIViewMixin, generics.ObjectActionAPIView
):
    """
    post: Exports the specified document version.
    """
    action_response_status = status.HTTP_202_ACCEPTED
    lookup_url_kwarg = 'document_version_id'
    mayan_object_permissions = {
        'POST': (permission_document_version_export,),
    }

    def get_queryset(self):
        return self.get_document().versions.all()

    def object_action(self, request, serializer):
        task_document_version_export.apply_async(
            kwargs={
                'document_version_id': self.object.pk,
                'user_id': request.user.id
            }
        )


class APIDocumentVersionListView(
    ParentObjectDocumentAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Return a list of the selected document's versions.
    post: Create a new document version.
    """
    ordering_fields = ('active', 'comment', 'id')
    serializer_class = DocumentVersionSerializer

    def get_instance_extra_data(self):
        # This method is only called during POST, therefore filter only by
        # edit permission.
        return {
            '_event_actor': self.request.user,
            'document': self.get_document(
                permission=permission_document_version_create
            )
        }

    def get_queryset(self):
        # This method is only called during GET, therefore filter only by
        # the view permission.
        return self.get_document(
            permission=permission_document_version_view
        ).versions.all()


class APIDocumentVersionPageDetailView(
    ParentObjectDocumentVersionAPIViewMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected document version page.
    get: Returns the selected document version page details.
    patch: Edit the properties of the selected document version page.
    put: Edit the properties of the selected document version page.
    """
    lookup_url_kwarg = 'document_version_page_id'
    mayan_object_permissions = {
        'DELETE': (permission_document_version_edit,),
        'GET': (permission_document_version_view,),
        'PATCH': (permission_document_version_edit,),
        'PUT': (permission_document_version_edit,)
    }
    serializer_class = DocumentVersionPageSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.get_document_version().pages.all()


class APIDocumentVersionPageImageView(
    APIImageViewMixin, ParentObjectDocumentVersionAPIViewMixin,
    generics.RetrieveAPIView
):
    """
    get: Returns an image representation of the selected document version page.
    """
    lookup_url_kwarg = 'document_version_page_id'
    mayan_object_permissions = {
        'GET': (permission_document_version_view,),
    }

    def get_queryset(self):
        return self.get_document_version().pages.all()


class APIDocumentVersionPageListView(
    ParentObjectDocumentVersionAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns an list of the pages for the selected document version.
    post: Create a new document version page.
    """
    lookup_url_kwarg = 'document_version_page_id'
    serializer_class = DocumentVersionPageSerializer

    def get_instance_extra_data(self):
        # This method is only called during POST, therefore filter only by
        # edit permission.
        return {
            '_event_actor': self.request.user,
            'document_version': self.get_document_version(
                permission=permission_document_version_edit
            )
        }

    def get_queryset(self):
        # This method is only called during GET, therefore filter only by
        # the view permission.
        return self.get_document_version(
            permission=permission_document_version_view
        ).pages.all()
