from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common.utils import encapsulate
from documents.models import Document, DocumentType
from navigation.api import (register_links, register_multi_item_links,
    register_sidebar_template, register_model_list_columns)
from project_setup.api import register_setup

from .api import get_metadata_string
from .links import (metadata_edit, metadata_view, metadata_multiple_edit,
    metadata_add, metadata_multiple_add, metadata_remove, metadata_multiple_remove,
    setup_metadata_type_list, setup_metadata_type_edit, setup_metadata_type_delete,
    setup_metadata_type_create, setup_metadata_set_list, setup_metadata_set_edit,
    setup_metadata_set_members, setup_metadata_set_delete, setup_metadata_set_create,
    setup_document_type_metadata)
from .models import MetadataType, MetadataSet
from .permissions import (PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_REMOVE,
    PERMISSION_METADATA_DOCUMENT_VIEW)

register_links(['metadata_add', 'metadata_edit', 'metadata_remove', 'metadata_view'], [metadata_add, metadata_edit, metadata_remove], menu_name='sidebar')
register_links(Document, [metadata_view], menu_name='form_header')
register_multi_item_links(['document_find_duplicates', 'folder_view', 'index_instance_node_view', 'document_type_document_list', 'search', 'results', 'document_group_view', 'document_list', 'document_list_recent', 'tag_tagged_item_list'], [metadata_multiple_add, metadata_multiple_edit, metadata_multiple_remove])

register_links(MetadataType, [setup_metadata_type_edit, setup_metadata_type_delete])
register_links([MetadataType, 'setup_metadata_type_list', 'setup_metadata_type_create'], [setup_metadata_type_list, setup_metadata_type_create], menu_name='secondary_menu')

register_links(MetadataSet, [setup_metadata_set_edit, setup_metadata_set_members, setup_metadata_set_delete])
register_links([MetadataSet, 'setup_metadata_set_list', 'setup_metadata_set_create'], [setup_metadata_set_list, setup_metadata_set_create], menu_name='secondary_menu')

register_links(DocumentType, [setup_document_type_metadata])

register_sidebar_template(['setup_metadata_type_list'], 'metadata_type_help.html')
register_sidebar_template(['setup_metadata_set_list'], 'metadata_set_help.html')

register_setup(setup_metadata_type_list)
register_setup(setup_metadata_set_list)

class_permissions(Document, [
    PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_ADD,
    PERMISSION_METADATA_DOCUMENT_REMOVE,
    PERMISSION_METADATA_DOCUMENT_VIEW,
])

register_model_list_columns(Document, [
        {
            'name': _(u'metadata'), 'attribute': encapsulate(lambda x: get_metadata_string(x))
        },
    ])
