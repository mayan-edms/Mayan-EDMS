from __future__ import absolute_import, unicode_literals

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.rest_api import generics

from .models import DocumentCheckout
from .permissions import (
    permission_document_check_in, permission_document_check_in_override,
    permission_document_check_out_detail_view
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
        filtered_documents = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=self.request.user,
            queryset=DocumentCheckout.objects.checked_out_documents()
        )
        filtered_documents = AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_out_detail_view, user=self.request.user,
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
            filtered_documents = AccessControlList.objects.restrict_queryset(
                permission=permission_document_view,
                queryset=DocumentCheckout.objects.checked_out_documents(),
                user=self.request.user
            )
            filtered_documents = AccessControlList.objects.restrict_queryset(
                permission=permission_document_check_out_detail_view,
                queryset=filtered_documents, user=self.request.user
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

        if document.get_check_out_info().user == request.user:
            AccessControlList.objects.check_access(
                obj=document, permissions=(permission_document_check_in,),
                user=request.user
            )
        else:
            AccessControlList.objects.check_access(
                obj=document,
                permissions=(permission_document_check_in_override,),
                user=request.user
            )

        return super(
            APICheckedoutDocumentView, self
        ).delete(request, *args, **kwargs)
