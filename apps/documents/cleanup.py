from __future__ import absolute_import

from .models import Document, DocumentType


def cleanup():
    for document in Document.objects.all():
        document.delete()

    DocumentType.objects.all().delete()
