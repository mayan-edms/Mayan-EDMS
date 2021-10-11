from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models.document_models import Document
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

        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewDocumentCheckoutSerializer
        else:
            return DocumentCheckoutSerializer

    def get_queryset(self):
        valid_document_queryset = Document.valid.all()

        filtered_documents = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view,
            queryset=DocumentCheckout.objects.checked_out_documents(),
            user=self.request.user,
        )
        filtered_documents = AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_out_detail_view,
            queryset=filtered_documents,
            user=self.request.user,
        )

        return DocumentCheckout.objects.filter(
            document__pk__in=filtered_documents.filter(
                pk__in=valid_document_queryset.values('pk')
            ).values('pk')
        )


class APICheckedoutDocumentView(generics.RetrieveDestroyAPIView):
    """
    get: Retrieve the details of the selected checked out document entry.
    delete: Checkin a document.
    """
    lookup_url_kwarg = 'checkout_id'
    serializer_class = DocumentCheckoutSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            '_event_keep_attributes': ('_event_actor',)
        }

    def get_queryset(self):
        valid_document_queryset = Document.valid.all()

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
                document__pk__in=filtered_documents.filter(
                    pk__in=valid_document_queryset.values('pk')
                ).values('pk')
            )
        elif self.request.method == 'DELETE':
            check_in_queryset = AccessControlList.objects.restrict_queryset(
                permission=permission_document_check_in,
                queryset=DocumentCheckout.objects.filter(user_id=self.request.user.pk),
                user=self.request.user
            )
            check_in_override_queryset = AccessControlList.objects.restrict_queryset(
                permission=permission_document_check_in_override,
                queryset=DocumentCheckout.objects.exclude(
                    user_id=self.request.user.pk
                ),
                user=self.request.user
            )

            return (check_in_queryset | check_in_override_queryset).filter(
                document_id__in=valid_document_queryset.values('pk')
            )
