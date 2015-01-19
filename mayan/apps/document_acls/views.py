from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from acls.views import acl_list_for
from documents.models import Document


def document_acl_list(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    return acl_list_for(
        request,
        document,
        extra_context={
            'object': document,
        }
    )
