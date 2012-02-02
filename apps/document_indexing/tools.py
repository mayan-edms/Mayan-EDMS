from __future__ import absolute_import

from documents.models import Document

from .models import IndexInstanceNode, DocumentRenameCount
from .filesystem import fs_delete_directory_recusive
from .api import update_indexes


def do_rebuild_all_indexes():
    fs_delete_directory_recusive()
    IndexInstanceNode.objects.delete()
    DocumentRenameCount.objects.delete()
    for document in Document.objects.all():
        update_indexes(document)

    return []  # Warnings - None
