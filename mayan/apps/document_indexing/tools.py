from __future__ import absolute_import

from documents.models import Document

from .api import update_indexes
from .models import Index, IndexInstanceNode


def do_rebuild_all_indexes():
    for instance_node in IndexInstanceNode.objects.all():
        instance_node.delete()

    for index in Index.objects.all():
        index.delete()

    for document in Document.objects.all():
        # TODO: Launch all concurrently as background tasks
        update_indexes(document)
