from __future__ import absolute_import, unicode_literals

import pytz

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from acls.models import AccessControlList
from documents.models import Document
from documents.permissions import permission_document_view
from permissions import Permission

from .models import DocumentCheckout
from .permissions import (
    permission_document_checkout, permission_document_checkin,
    permission_document_checkin_override
)
from .serializers import (
    DocumentCheckoutSerializer, NewDocumentCheckoutSerializer
)


class APICheckedoutDocumentListView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewDocumentCheckoutSerializer
        else:
            return DocumentCheckoutSerializer

    def get_queryset(self):
        documents = DocumentCheckout.on_organization.checked_out_documents()

        try:
            Permission.check_permissions(
                self.request.user, (permission_document_view,)
            )
        except PermissionDenied:
            filtered_documents = AccessControlList.objects.filter_by_access(
                (permission_document_view,), self.request.user, documents
            )
        else:
            filtered_documents = documents

        return DocumentCheckout.on_organization.filter(
            document__pk__in=filtered_documents.values_list('pk', flat=True)
        )

    def get(self, request, *args, **kwargs):
        """
        Returns a list of all the documents that are currently checked out.
        """

        return super(
            APICheckedoutDocumentListView, self
        ).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Checkout a document.
        """

        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            document = get_object_or_404(
                Document.on_organization, pk=serializer.data['document']
            )
            try:
                Permission.check_permissions(
                    request.user, (permission_document_checkout,)
                )
            except PermissionDenied:
                AccessControlList.objects.check_access(
                    permission_document_checkout, request.user, document
                )

            timezone = pytz.utc

            try:
                DocumentCheckout.on_organization.create(
                    document=document,
                    expiration_datetime=timezone.localize(
                        serializer.data['expiration_datetime']
                    ),
                    user=request.user,
                    block_new_version=serializer.data['block_new_version']
                )
            except Exception as exception:
                return Response(
                    data={'exception': unicode(exception)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APICheckedoutDocumentView(generics.RetrieveDestroyAPIView):
    serializer_class = DocumentCheckoutSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            documents = DocumentCheckout.on_organization.checked_out_documents()

            try:
                Permission.check_permissions(
                    self.request.user, (permission_document_view,)
                )
            except PermissionDenied:
                filtered_documents = AccessControlList.objects.filter_by_access(
                    (permission_document_view,), self.request.user, documents
                )
            else:
                filtered_documents = documents

            return DocumentCheckout.on_organization.filter(
                document__pk__in=filtered_documents.values_list(
                    'pk', flat=True
                )
            )
        elif self.request.method == 'DELETE':
            return DocumentCheckout.on_organization.all()

    def get(self, request, *args, **kwargs):
        """
        Retrieve the details of the selected checked out document entry.
        """

        return super(
            APICheckedoutDocumentView, self
        ).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Checkin a document.
        """

        document = self.get_object().document

        if document.checkout_info().user == request.user:
            try:
                Permission.check_permissions(
                    request.user, (permission_document_checkin,)
                )
            except PermissionDenied:
                AccessControlList.objects.check_access(
                    permission_document_checkin, request.user, document
                )
        else:
            try:
                Permission.check_permissions(
                    request.user, (permission_document_checkin_override,)
                )
            except PermissionDenied:
                AccessControlList.objects.check_access(
                    permission_document_checkin_override, request.user,
                    document
                )

        return super(
            APICheckedoutDocumentView, self
        ).delete(request, *args, **kwargs)
