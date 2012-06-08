from django.shortcuts import get_object_or_404

from documents.models import Document
from acls.views import acl_list_for


def document_acl_list(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    return acl_list_for(
        request,
        document,
    )
