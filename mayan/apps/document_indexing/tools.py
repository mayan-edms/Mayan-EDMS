from documents.models import Document

from .api import index_document
from .models import IndexInstanceNode


def do_rebuild_all_indexes():
    for instance_node in IndexInstanceNode.objects.all():
        instance_node.delete()

    for document in Document.objects.all():
        index_document(document)
