from __future__ import absolute_import, unicode_literals

from rest_framework import generics

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.permissions import permission_document_view

from .models import DocumentCheckout
from .permissions import (
    permission_document_checkin, permission_document_checkin_override,
    permission_document_checkout_detail_view
)
from .serializers import (
    DocumentCheckoutSerializer, NewDocumentCheckoutSerializer
)


class APICheckedoutDocumentListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the documents that are currently checked out.
    post: Checkout a document.
    """
    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APICheckedoutDocumentListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewDocumentCheckoutSerializer
        else:
            return DocumentCheckoutSerializer

    def get_queryset(self):
        filtered_documents = AccessControlList.objects.filter_by_access(
            permission=permission_document_view, user=self.request.user,
            queryset=DocumentCheckout.objects.checked_out_documents()
        )
        filtered_documents = AccessControlList.objects.filter_by_access(
            permission=permission_document_checkout_detail_view, user=self.request.user,
            queryset=filtered_documents
        )

        return DocumentCheckout.objects.filter(
            document__pk__in=filtered_documents.values_list('pk', flat=True)
        )


class APICheckedoutDocumentView(generics.RetrieveDestroyAPIView):
    """
    get: Retrieve the details of the selected checked out document entry.
    delete: Checkin a document.
    """
    serializer_class = DocumentCheckoutSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            filtered_documents = AccessControlList.objects.filter_by_access(
                permission=permission_document_view, user=self.request.user,
                queryset=DocumentCheckout.objects.checked_out_documents()
            )
            filtered_documents = AccessControlList.objects.filter_by_access(
                permission=permission_document_checkout_detail_view, user=self.request.user,
                queryset=filtered_documents
            )

            return DocumentCheckout.objects.filter(
                document__pk__in=filtered_documents.values_list(
                    'pk', flat=True
                )
            )
        elif self.request.method == 'DELETE':
            return DocumentCheckout.objects.all()

    def delete(self, request, *args, **kwargs):
        document = self.get_object().document

        if document.checkout_info().user == request.user:
            AccessControlList.objects.check_access(
                permissions=permission_document_checkin, user=request.user,
                obj=document
            )
        else:
            AccessControlList.objects.check_access(
                permissions=permission_document_checkin_override,
                user=request.user, obj=document
            )

        return super(
            APICheckedoutDocumentView, self
        ).delete(request, *args, **kwargs)
