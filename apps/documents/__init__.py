from __future__ import absolute_import

import tempfile

from django.utils.translation import ugettext_lazy as _

from common.utils import validate_path, encapsulate
from navigation.api import (bind_links, register_top_menu,
    register_model_list_columns,
    register_sidebar_template, Link)
from main.api import register_diagnostic, register_maintenance_links
from history.api import register_history_type
from history.permissions import PERMISSION_HISTORY_VIEW
from project_setup.api import register_setup
from acls.api import class_permissions

from .models import (Document, DocumentPage,
    DocumentPageTransformation, DocumentType, DocumentTypeFilename,
    DocumentVersion)
from .permissions import (PERMISSION_DOCUMENT_PROPERTIES_EDIT,
    PERMISSION_DOCUMENT_VIEW, PERMISSION_DOCUMENT_DELETE,
    PERMISSION_DOCUMENT_DOWNLOAD, PERMISSION_DOCUMENT_TRANSFORM,
    PERMISSION_DOCUMENT_EDIT, PERMISSION_DOCUMENT_VERSION_REVERT,
    PERMISSION_DOCUMENT_NEW_VERSION)
from .literals import (HISTORY_DOCUMENT_CREATED,
    HISTORY_DOCUMENT_EDITED, HISTORY_DOCUMENT_DELETED)
from .conf import settings as document_settings
from .widgets import document_thumbnail
from .links import (document_list, document_list_recent, document_create_multiple,
    document_create_siblings, document_view_simple, document_view_advanced,
    document_delete, document_edit, document_download, document_version_download,
    document_find_duplicates, document_find_all_duplicates,
    document_update_page_count, document_clear_transformations,
    document_print, document_history_view,
    document_missing_list)
from .links import (document_type_list, document_type_setup, document_type_document_list,
    document_type_edit, document_type_delete, document_type_create, document_type_filename_list,
    document_type_filename_create, document_type_filename_edit, document_type_filename_delete)
from .links import document_version_list, document_version_revert
from .links import (document_page_transformation_list, document_page_transformation_create,
    document_page_transformation_edit, document_page_transformation_delete,
    document_page_view, document_page_text, document_page_edit, document_page_navigation_next,
    document_page_navigation_previous, document_page_navigation_first,
    document_page_navigation_last, document_page_zoom_in, document_page_zoom_out,
    document_page_rotate_right, document_page_rotate_left, document_page_view_reset)
from .links import document_clear_image_cache

# History setup
register_history_type(HISTORY_DOCUMENT_CREATED)
register_history_type(HISTORY_DOCUMENT_EDITED)
register_history_type(HISTORY_DOCUMENT_DELETED)

# Register document type links
bind_links([DocumentType], [document_type_document_list, document_type_filename_list, document_type_edit, document_type_delete])
bind_links([DocumentTypeFilename], [document_type_filename_edit, document_type_filename_delete])

bind_links(['setup_document_type_metadata', 'document_type_filename_delete', 'document_type_create', 'document_type_filename_create', 'document_type_filename_edit', 'document_type_filename_list', 'document_type_list', 'document_type_document_list', 'document_type_edit', 'document_type_delete'], [document_type_list, document_type_create], menu_name='sidebar')
bind_links(['document_type_filename_create', 'document_type_filename_list', 'document_type_filename_edit', 'document_type_filename_delete'], [document_type_filename_create], menu_name='sidebar')

# Register document links
bind_links([Document], [document_view_simple, document_edit, document_print, document_delete, document_download, document_find_duplicates, document_clear_transformations, document_create_siblings])

# Document Version links
bind_links([DocumentVersion], [document_version_revert, document_version_download])

secondary_menu_links = [document_list_recent, document_list, document_create_multiple]

bind_links(['document_list_recent', 'document_list', 'document_create', 'document_create_multiple', 'upload_interactive', 'staging_file_delete'], secondary_menu_links, menu_name='secondary_menu')
bind_links([Document], secondary_menu_links, menu_name='secondary_menu')

# Document page links
bind_links([DocumentPage], [
    document_page_transformation_list, document_page_view,
    document_page_text, document_page_edit,
])

# Document page navigation links
bind_links([DocumentPage], [
    document_page_navigation_first, document_page_navigation_previous,
    document_page_navigation_next, document_page_navigation_last
], menu_name='sidebar')

bind_links(['document_page_view'], [document_page_rotate_left, document_page_rotate_right, document_page_zoom_in, document_page_zoom_out, document_page_view_reset], menu_name='form_header')

bind_links([DocumentPageTransformation], [document_page_transformation_edit, document_page_transformation_delete])
bind_links('document_page_transformation_list', [document_page_transformation_create], menu_name='sidebar')
bind_links('document_page_transformation_create', [document_page_transformation_create], menu_name='sidebar')
bind_links(['document_page_transformation_edit', 'document_page_transformation_delete'], [document_page_transformation_create], menu_name='sidebar')

register_diagnostic('documents', _(u'Documents'), document_missing_list)

register_maintenance_links([document_find_all_duplicates, document_update_page_count, document_clear_image_cache], namespace='documents', title=_(u'documents'))

register_model_list_columns(Document, [
        {'name':_(u'thumbnail'), 'attribute':
            encapsulate(lambda x: document_thumbnail(x, gallery_name='document_list', title=x.filename))
        },
    ])

register_top_menu(
    'documents',
    link=Link(sprite='page', text=_(u'documents'), view='document_list_recent',
    children_url_regex=[r'^documents/[^t]', r'^metadata/[^s]', r'comments', r'tags/document', r'grouping/[^s]', r'history/list/for_object/documents'],
    children_view_regex=[r'document_acl', r'smart_link_instance'],
    children_views=['document_folder_list', 'folder_add_document', 'document_index_list', 'upload_version', ]),
    position=1
)

register_sidebar_template(['document_list_recent'], 'recent_document_list_help.html')
register_sidebar_template(['document_type_list'], 'document_types_help.html')

bind_links([Document], [document_view_simple], menu_name='form_header', position=0)
bind_links([Document], [document_view_advanced], menu_name='form_header', position=1)
bind_links([Document], [document_history_view], menu_name='form_header')
bind_links([Document], [document_version_list], menu_name='form_header')

if (validate_path(document_settings.CACHE_PATH) == False) or (not document_settings.CACHE_PATH):
    setattr(document_settings, 'CACHE_PATH', tempfile.mkdtemp())

register_setup(document_type_setup)

class_permissions(Document, [
    PERMISSION_DOCUMENT_PROPERTIES_EDIT,
    PERMISSION_DOCUMENT_EDIT,
    PERMISSION_DOCUMENT_VIEW,
    PERMISSION_DOCUMENT_DELETE,
    PERMISSION_DOCUMENT_DOWNLOAD,
    PERMISSION_DOCUMENT_TRANSFORM,
    PERMISSION_DOCUMENT_NEW_VERSION,
    PERMISSION_DOCUMENT_VERSION_REVERT,
    PERMISSION_HISTORY_VIEW
])
