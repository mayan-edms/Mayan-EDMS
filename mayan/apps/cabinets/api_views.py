from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.rest_api import generics

from .models import Cabinet
from .permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_remove_document, permission_cabinet_view
)
from .serializers import (
    CabinetDocumentSerializer, CabinetSerializer, NewCabinetDocumentSerializer,
    WritableCabinetSerializer
)


class APIDocumentCabinetListView(generics.ListAPIView):
    """
    Returns a list of all the cabinets to which a document belongs.
    """
    mayan_object_permissions = {'GET': (permission_cabinet_view,)}
    serializer_class = CabinetSerializer

    def get_queryset(self):
        document = get_object_or_404(klass=Document, pk=self.kwargs['pk'])
        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_document_view,),
            user=self.request.user
        )

        queryset = document.document_cabinets()
        return queryset


class APICabinetListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the cabinets.
    post: Create a new cabinet
    """
    mayan_object_permissions = {'GET': (permission_cabinet_view,)}
    mayan_view_permissions = {'POST': (permission_cabinet_create,)}
    queryset = Cabinet.objects.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APICabinetListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CabinetSerializer
        elif self.request.method == 'POST':
            return WritableCabinetSerializer


class APICabinetView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected cabinet.
    get: Returns the details of the selected cabinet.
    patch: Edit the selected cabinet.
    put: Edit the selected cabinet.
    """
    mayan_object_permissions = {
        'GET': (permission_cabinet_view,),
        'PUT': (permission_cabinet_edit,),
        'PATCH': (permission_cabinet_edit,),
        'DELETE': (permission_cabinet_delete,)
    }
    queryset = Cabinet.objects.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APICabinetView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CabinetSerializer
        else:
            return WritableCabinetSerializer


class APICabinetDocumentListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the documents contained in a particular cabinet.
    post: Add a document to the selected cabinet.
    """
    mayan_object_permissions = {
        'GET': (permission_cabinet_view,),
        'POST': (permission_cabinet_add_document,)
    }

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APICabinetDocumentListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CabinetDocumentSerializer
        elif self.request.method == 'POST':
            return NewCabinetDocumentSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APICabinetDocumentListView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'cabinet': self.get_cabinet(),
                }
            )

        return context

    def get_cabinet(self):
        return get_object_or_404(klass=Cabinet, pk=self.kwargs['pk'])

    def get_queryset(self):
        cabinet = self.get_cabinet()

        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_view,
            queryset=cabinet.documents.all(), user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(cabinet=self.get_cabinet())


class APICabinetDocumentView(generics.RetrieveDestroyAPIView):
    """
    delete: Remove a document from the selected cabinet.
    get: Returns the details of the selected cabinet document.
    """
    lookup_url_kwarg = 'document_pk'
    mayan_object_permissions = {
        'GET': (permission_cabinet_view,),
        'DELETE': (permission_cabinet_remove_document,)
    }
    serializer_class = CabinetDocumentSerializer

    def get_cabinet(self):
        return get_object_or_404(klass=Cabinet, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_cabinet().documents.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APICabinetDocumentView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'cabinet': self.get_cabinet(),
                }
            )

        return context

    def perform_destroy(self, instance):
        self.get_cabinet().documents.remove(instance)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        AccessControlList.objects.check_access(
            obj=instance, permissions=(permission_document_view,),
            user=self.request.user
        )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
