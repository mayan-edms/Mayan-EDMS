from __future__ import absolute_import

from documents.models import Document

from .api import update_indexes
from .filesystem import fs_delete_directory_recusive
from .models import Index, IndexInstanceNode, DocumentRenameCount


def do_rebuild_all_indexes():
    for index in Index.objects.all():
        fs_delete_directory_recusive(index)

    IndexInstanceNode.objects.all().delete()
    DocumentRenameCount.objects.all().delete()
    for document in Document.objects.all():
        update_indexes(document)

    return []  # Warnings - None
