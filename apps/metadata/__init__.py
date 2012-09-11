from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common.utils import encapsulate
from documents.models import Document, DocumentType
from navigation.api import (bind_links, register_sidebar_template,
    register_model_list_columns, register_multi_item_links)

from .api import get_metadata_string
from .links import (metadata_edit, metadata_view, metadata_add, metadata_remove,
    setup_metadata_type_list, setup_metadata_type_edit, setup_metadata_type_delete,
    setup_metadata_type_create, setup_metadata_set_list, setup_metadata_set_edit,
    setup_metadata_set_delete, setup_metadata_set_create, setup_metadata_set_members,
    setup_document_type_metadata, metadata_multiple_add, metadata_multiple_edit,
    metadata_multiple_remove)
from .models import MetadataType, MetadataSet
from .permissions import (PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_REMOVE,
    PERMISSION_METADATA_DOCUMENT_VIEW)

bind_links(['metadata_add', 'metadata_edit', 'metadata_remove', 'metadata_view'], [metadata_add, metadata_edit, metadata_remove], menu_name='sidebar')
bind_links([Document], [metadata_view], menu_name='form_header')

bind_links([MetadataType], [setup_metadata_type_edit, setup_metadata_type_delete])
bind_links([MetadataType, 'setup_metadata_type_list', 'setup_metadata_type_create'], [setup_metadata_type_list, setup_metadata_type_create], menu_name='secondary_menu')

bind_links([MetadataSet], [setup_metadata_set_edit, setup_metadata_set_members, setup_metadata_set_delete])
bind_links([MetadataSet, 'setup_metadata_set_list', 'setup_metadata_set_create'], [setup_metadata_set_list, setup_metadata_set_create], menu_name='secondary_menu')

bind_links([DocumentType], [setup_document_type_metadata])

register_multi_item_links(['folder_view', 'search', 'results', 'index_instance_node_view', 'document_find_duplicates', 'document_type_document_list', 'document_group_view', 'document_list', 'document_list_recent'], [metadata_multiple_add, metadata_multiple_edit, metadata_multiple_remove])

metadata_type_setup_views = ['setup_metadata_type_list', 'setup_metadata_type_edit', 'setup_metadata_type_delete', 'setup_metadata_type_create']
metadata_set_setup_views = ['setup_metadata_set_list', 'setup_metadata_set_edit', 'setup_metadata_set_members', 'setup_metadata_set_delete', 'setup_metadata_set_create']

register_sidebar_template(['setup_metadata_type_list'], 'metadata_type_help.html')
register_sidebar_template(['setup_metadata_set_list'], 'metadata_set_help.html')

class_permissions(Document, [
    PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_ADD,
    PERMISSION_METADATA_DOCUMENT_REMOVE,
    PERMISSION_METADATA_DOCUMENT_VIEW,
])

register_model_list_columns(Document, [
        {'name':_(u'metadata'), 'attribute':
            encapsulate(lambda x: get_metadata_string(x))
        },
    ])
