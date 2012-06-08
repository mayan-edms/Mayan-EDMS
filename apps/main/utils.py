from navigation.api import register_multi_item_links

from documents.links import document_multiple_clear_transformations, document_multiple_delete, document_multiple_download
from metadata import metadata_multiple_add, metadata_multiple_edit, metadata_multiple_remove
from ocr import submit_document_multiple


def register_multi_items_links():
    view = [
        # folders
        'folder_view',

        # search
        'search', 'results',

        # document_indexing
        'index_instance_node_view',

        # documents
        'document_find_duplicates', 'document_type_document_list', 'document_group_view', 'document_list', 'document_list_recent',
    ]
    register_multi_item_links(view, [submit_document_multiple, metadata_multiple_add, metadata_multiple_edit, metadata_multiple_remove, document_multiple_clear_transformations, document_multiple_delete, document_multiple_download])
